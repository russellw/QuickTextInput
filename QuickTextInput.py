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
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys=ON")

# Initialize tables
with conn:
    cursor = conn.cursor()
    try:
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
    finally:
        cursor.close()

# Read word frequencies
word_freq = {}
prefix_dict = defaultdict(list)
with conn:
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT word, count FROM words")
        rs = cursor.fetchall()
        for r in rs:
            word = r[0]
            n = r[1]
            word_freq[word] = n

            # For each prefix in a word, add the word to the prefix dictionary
            for i in range(1, len(word) + 1):
                prefix = word[:i]
                prefix_dict[prefix].append(word)
    finally:
        cursor.close()

# Limit each prefix entry to the 10 most frequent words
for prefix in prefix_dict:
    prefix_dict[prefix] = sorted(prefix_dict[prefix], key=lambda w: -word_freq[w])[:10]


def copy_to_clipboard():
    # Get the text from the text field
    text = text_field.get("1.0", tk.END)
    # Clear the clipboard
    root.clipboard_clear()
    # Append the text to the clipboard
    root.clipboard_append(text)
    # Update the clipboard
    root.update()

    with conn:
        cursor = conn.cursor()
        try:
            for s in split_alnum_words(text):
                if s in words:
                    words[s] += 1
                    cursor.execute(
                        "UPDATE words SET count = count + 1 WHERE word = ?", (s,)
                    )
                else:
                    words[s] = 1
                    cursor.execute(
                        "INSERT INTO words (word, count) VALUES (?, 1)", (s,)
                    )
        finally:
            cursor.close()


def get_last_line():
    # Get the end position index of the text widget
    end_index = text_field.index(tk.END)
    # Extract the line number from the end index
    last_line_num = int(end_index.split(".")[0]) - 1
    # Get the text of the last line
    return text_field.get(f"{last_line_num}.0", f"{last_line_num}.end")


def on_key_release(event):
    c = event.keysym

    if c.isalpha():
        # Get the position of the cursor
        cursor_index = text_field.index(tk.INSERT)
        x, y, _, _ = text_field.bbox(cursor_index)

        # Convert the text box coordinates to root window coordinates
        x_root = x + text_field.winfo_rootx()
        y_root = y + text_field.winfo_rooty()

        suggestions = ["1. Lenovo", "2. HP", "3. Dell", "4. Apple", "5. Asus"]
        for suggestion in suggestions:
            label = tk.Label(suggestion_box, text=suggestion, anchor="w")
            label.pack(fill=tk.BOTH)

        suggestion_box.wm_geometry(f"+{x_root}+{y_root + 20}")
        suggestion_box.deiconify()


def split_alnum_words(s):
    # Split the string by any non-alphanumeric character
    words = re.split(r"\W+", s)
    # Remove empty strings from the result
    return [word for word in words if word]


# Create the main window
root = tk.Tk()
root.title("QuickTextInput")

# Create a Text widget
text_field = tk.Text(root, height=30, width=80, wrap=tk.WORD, insertofftime=0)
text_field.pack()
text_field.focus_set()

# Bind the key release event to show the suggestion box
text_field.bind("<KeyRelease>", on_key_release)

# Create the suggestion box
suggestion_box = tk.Toplevel(root)
suggestion_box.wm_overrideredirect(True)
suggestion_box.withdraw()

# Create the copy button with internal padding and align it to the right side
copy_button = tk.Button(
    root, text="Copy to Clipboard (F12)", command=copy_to_clipboard, padx=10, pady=10
)
copy_button.pack(padx=5, pady=5, anchor="e")

# Bind the F12 key to the copy_to_clipboard function
root.bind("<F12>", lambda event: copy_to_clipboard())

# Run the Tkinter event loop
root.mainloop()
