import os
import re
import sqlite3
import tkinter as tk
from collections import defaultdict

# File path
user_profile = os.environ["USERPROFILE"]
documents_dir = os.path.join(user_profile, "Documents")
db_path = os.path.join(documents_dir, "QuickTextInput.db")

# Connect to database
conn = sqlite3.connect(db_path, autocommit=True)
conn.execute("PRAGMA foreign_keys=ON")

# Initialize tables
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
if len(tables) == 0:
    cursor.execute(
        """
    CREATE TABLE words (
        word TEXT PRIMARY KEY,
        count INTEGER DEFAULT 0
    ) STRICT;
    """
    )

# Read word frequencies
word_freq = {}
prefix_dict = defaultdict(list)

cursor = conn.cursor()
cursor.execute("SELECT word, count FROM words")
rs = cursor.fetchall()
for r in rs:
    word = r[0]
    count = r[1]
    word_freq[word] = count

    # For each prefix in a word, add the word to the prefix dictionary
    for i in range(1, len(word) + 1):
        prefix = word[:i]
        prefix_dict[prefix].append(word)

# Limit each prefix entry to the 20 most frequent words
for prefix in prefix_dict:
    prefix_dict[prefix] = sorted(prefix_dict[prefix], key=lambda w: -word_freq[w])[:20]


def copy_to_clipboard():
    # Get the text from the text field
    text = text_widget.get("1.0", tk.END)

    # Clear the clipboard
    root.clipboard_clear()

    # Append the text to the clipboard
    root.clipboard_append(text)

    # Update the clipboard
    root.update()

    cursor = conn.cursor()
    for word in split_alnum_words(text):
        if word in words:
            words[word] += 1
            cursor.execute("UPDATE words SET count = count + 1 WHERE word = ?", (word,))
        else:
            words[word] = 1
            cursor.execute("INSERT INTO words (word, count) VALUES (?, 1)", (word,))


def last_word(s):
    # Split the string by any non-alphanumeric character
    words = re.split(r"\W+", s)

    # Remove empty strings from the result
    words = [word for word in words if word]

    # Last word
    return words[-1]


def on_key_release(event):
    # Check if cursor is at the end
    end_index = text_widget.index("end-1c")
    if text_widget.index("insert") != end_index:
        suggest()
        return

    c = event.char

    # Only letters trigger suggestions
    if c.isalpha():
        last_line_num = int(end_index.split(".")[0])
        last_line = text_widget.get(f"{last_line_num}.0", f"{last_line_num}.end")
        prefix = last_word(last_line)
        suggest(prefix_dict[prefix])
        return

    # Suggestions never just hang around
    # they are either updated or cleared
    suggest()

    # Space after punctuation
    # The disjunction is because the empty string is considered to be in all strings
    if c and c in ",.;:":
        text_widget.insert("insert", " ")
        return

    # Digit picks suggestion
    k = event.keycode
    if k == 48:
        pick(9)
        return
    if 49 <= k <= 57:
        pick(k - 49)
        return


def pick(i):
    if len(suggestions) <= i:
        return
    end_index = text_widget.index("end-1c")
    last_line_num = int(end_index.split(".")[0])
    last_line = text_widget.get(f"{last_line_num}.0", f"{last_line_num}.end")
    n = len(last_word(last_line))
    start_index = f"{end_index} - {n} chars"
    text_widget.delete(start_index, end_index)
    text_widget.insert("insert", suggestions[i] + " ")


def suggest(suggestions1=[]):
    global suggestions
    suggestions = suggestions1
    for i in range(len(suggestions)):
        suggestion_cells[i].config(text=suggestions[i])
    for i in range(len(suggestions), 20):
        suggestion_cells[i].config(text="")


# Initialize the main window and maximize it
root = tk.Tk()
root.state("zoomed")  # Maximize window
root.title("Text Editor with Read-Only Info Cells")

# Configure the main window's layout
root.grid_rowconfigure(0, weight=1)  # Text widget should expand
root.grid_rowconfigure(1, weight=0)  # First row of cells
root.grid_rowconfigure(2, weight=0)  # Second row of cells
root.grid_columnconfigure(0, weight=1)

# Create the main text widget that occupies most of the screen
text_widget = tk.Text(root)
text_widget.grid(row=0, column=0, sticky="nsew")
text_widget.focus_set()

# Frame to hold the cells below the text widget
cell_frame = tk.Frame(root)
cell_frame.grid(row=1, column=0, sticky="ew", rowspan=2)

# Set equal weight for each column in the cell frame to ensure uniform widths
for col in range(20):
    cell_frame.grid_columnconfigure(col, weight=1)

# Store read-only label references for programmatic updates
suggestion_cells = []

# Helper function to create a row of read-only cells
def create_cell_row(row, prefix):
    for i in range(10):
        # Create label for the identifier (e.g., 'F1', 'F2', etc.)
        label_id = tk.Label(cell_frame, text=f"{prefix}{i+1}")
        label_id.grid(row=row, column=i * 2, sticky="e", padx=2, pady=2)

        # Create read-only text label with consistent width and relief for clarity
        read_only_text = tk.Label(
            cell_frame, text="", anchor="w", relief="sunken", width=10
        )
        read_only_text.grid(row=row, column=i * 2 + 1, sticky="ew", padx=2, pady=2)

        # Store the label for programmatic access
        suggestion_cells.append(read_only_text)


# First row with 'F1' to 'F10'
create_cell_row(0, "F")

# Second row with '1' to '10'
create_cell_row(1, "")

# Second row corresponds to first suggestions
suggestion_cells = suggestion_cells[10:] + suggestion_cells[:10]


# Suggestions
suggestions = []

"""

# Create the copy button with internal padding and align it to the right side
copy_button = tk.Button(
    root, text="Copy to Clipboard (F12)", command=copy_to_clipboard, padx=10, pady=10
)
copy_button.pack(padx=5, pady=5, anchor="e")
"""

# Bind events
text_widget.bind("<KeyRelease>", on_key_release)

# Root.bind("<F12>", lambda event: copy_to_clipboard())

# Run the Tkinter event loop
root.mainloop()
