import argparse
import inspect
import os
import re
import string
import tkinter as tk
from collections import defaultdict
from tkinter import font, messagebox

from PIL import ImageTk

import common


def about():
    messagebox.showinfo(
        "About QuickTextInput",
        "Efficient keyboard text input\n\nDesigned and implemented\nby Russell Wallace\n\nVersion 0.1",
    )


def bold():
    pass


def correct_grammar(text):
    # Split text into lines
    lines = text.splitlines()

    # Process each line through the correct_line helper function
    corrected_lines = [correct_line(line) for line in lines]

    # Join the corrected lines back into a single text string
    corrected_text = "\n".join(corrected_lines).strip()

    # Add a period at the end if there's no terminal punctuation and no URL at the end
    if not end_sentence(corrected_text) and not re.search(
        r"\bhttps?://\S*$", corrected_text
    ):
        corrected_text += "."

    return corrected_text


def correct_line(line):
    # Check if the line contains a URL. If so, return the line unchanged.
    if re.search(r"\bhttps?://", line):
        return line

    # Variables to help build the corrected line
    r = [" "]
    inside_quotes = False  # Track whether we're inside quotation marks

    for c in line:
        # Handle opening and closing quotes
        if c == '"':
            if inside_quotes:
                # No space before closing quote
                while r[-1] == " ":
                    r.pop()
                r.append(c)

                # Space after closing quote
                r.append(" ")
            else:
                # Space before opening quote
                r.append(" ")
                r.append(c)
            inside_quotes = not inside_quotes
            continue

        # Space before opening bracket
        if c == "(":
            r.append(" ")
            r.append(c)
            continue

        # Space after some punctuation
        if has_space_after(r[-1]) and c.isalnum():
            r.append(" ")

        # No space before punctuation
        if c in string.punctuation:
            while r[-1] == " ":
                r.pop()

        # Capitalize the first letter of each sentence
        if c.islower() and end_sentence(r):
            c = c.upper()

        r.append(c)

    r = "".join(r)

    # Skip extra spaces
    r = r.strip()
    r = re.sub(r"\s{2,}", " ", r)

    if not end_sentence(r):
        r += "."
    if inside_quotes:
        r += '"'

    return r


def create_button(image_name, tooltip_text, command):
    image = ImageTk.PhotoImage(file=f"baseline_{image_name}_black_24.png")
    button = tk.Button(toolbar_frame, image=image, command=command, relief="flat")
    button.image = image  # Keep a reference to the image
    button.bind("<Enter>", lambda e: show_tooltip(e, tooltip_text))
    button.bind("<Leave>", hide_tooltip)
    button.pack(side=tk.LEFT)
    return button


def dbg(a):
    info = inspect.getframeinfo(inspect.currentframe().f_back)
    print(f"{info.filename}:{info.function}:{info.lineno}: {a}")


def done():
    # Get the text from the text field
    text = text_widget.get("1.0", tk.END)

    # Fix up punctuation etc
    text = correct_grammar(text)

    # Clear the clipboard
    root.clipboard_clear()

    # Append the text to the clipboard
    root.clipboard_append(text)

    # Update the clipboard
    root.update()

    # Clear
    text_widget.delete("1.0", tk.END)

    # Update the database
    word_counts = defaultdict(int)
    for word in re.findall(r"\b\w+\b", text):
        if not word.isalpha():
            continue
        if len(word) == 1 and word.islower():
            continue
        word_counts[word] += 1
    with conn:
        cursor = conn.cursor()
        for word, count in word_counts.items():
            cursor.execute(
                """
                INSERT INTO words (word, count)
                VALUES (?, ?)
                ON CONFLICT(word) DO UPDATE SET count = count + ?
                """,
                (word, count, count),
            )


def end_sentence(s):
    for c in reversed(s):
        if is_terminal(c):
            return True
        if c in ' "':
            continue
        return False
    return True


def has_space_after(c):
    return is_terminal(c) or c in ",;:)"


def hide_tooltip(event):
    if event.widget.tooltip:
        event.widget.tooltip.destroy()


def is_terminal(c):
    return c in ".?!"


def last_word(s):
    # Split the string by any non-alphanumeric character
    words = re.split(r"\W+", s)

    # Remove empty strings from the result
    words = [word for word in words if word]

    # Last word, if any
    if words:
        return words[-1]
    return ""


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

    # Digit picks suggestion
    k = event.keycode
    if k == 48:
        pick(9)
    elif 49 <= k <= 57:
        pick(k - 49)
    elif 112 <= k <= 121:
        pick(k - 102)

    # Suggestions never just hang around
    # they are either updated or cleared
    suggest()


def pick(i):
    if i < len(suggestions):
        end_index = text_widget.index("end-1c")
        last_line_num = int(end_index.split(".")[0])
        last_line = text_widget.get(f"{last_line_num}.0", f"{last_line_num}.end")
        n = len(last_word(last_line))
        start_index = f"{end_index} - {n} chars"
        text_widget.delete(start_index, end_index)
        text_widget.insert("insert", suggestions[i] + " ")


def separator():
    separator = tk.Label(toolbar_frame, text="|", fg="light gray")
    separator.pack(side="left", padx=5)


def show_tooltip(event, text):
    # Calculate the widget's position relative to the root window
    widget_x = event.widget.winfo_rootx() - root.winfo_rootx()
    widget_y = event.widget.winfo_rooty() - root.winfo_rooty()

    # Calculate tooltip position based on widget's position in root and mouse event offset
    x = widget_x + event.x + 10  # Offset to position it slightly away from the mouse
    y = widget_y + event.y + 10

    tooltip = tk.Label(root, text=text, background="#FFFFE0", relief="solid")
    tooltip.place(x=x, y=y)
    event.widget.tooltip = tooltip


def suggest(suggestions1=[]):
    global suggestions
    suggestions = suggestions1
    for i in range(len(suggestions)):
        suggestion_cells[i].config(text=suggestions[i])
    for i in range(len(suggestions), 20):
        suggestion_cells[i].config(text="")


if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db",
        type=str,
        default=None,
        help="Path to the SQLite database file (default: ~/Documents/QuickTextInput.db)",
    )
    args = parser.parse_args()

    # Determine the database path
    if args.db:
        db_path = args.db
    else:
        # Default file path
        user_profile = os.environ["USERPROFILE"]
        documents_dir = os.path.join(user_profile, "Documents")
        db_path = os.path.join(documents_dir, "QuickTextInput.db")

    # Connect to database
    conn = common.init_db(db_path)

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
        prefix_dict[prefix] = sorted(prefix_dict[prefix], key=lambda w: -word_freq[w])[
            :20
        ]

    # Initialize the main window and maximize it
    root = tk.Tk()
    root.state("zoomed")  # Maximize window
    root.title("QuickTextInput")

    # Define a base font
    default_font = font.nametofont("TkDefaultFont")

    # Update the base font size
    default_font.configure(size=12)

    # Configure the main window's layout
    root.grid_rowconfigure(0, weight=0)  # Toolbar row
    root.grid_rowconfigure(1, weight=1)  # Empty space above suggestions to stretch
    for i in range(2, 21):
        root.grid_rowconfigure(i, weight=0)  # Suggestion rows (1 to 20)

    root.grid_columnconfigure(0, weight=0)  # Label column
    root.grid_columnconfigure(1, weight=0)  # Suggestion column
    root.grid_columnconfigure(2, weight=1)  # Text widget column (expands)

    # Create the menu bar
    menu_bar = tk.Menu(root)

    # Add "File" menu
    menu = tk.Menu(menu_bar, tearoff=0)
    menu.add_command(
        label="New", underline=0, command=lambda: text_widget.delete("1.0", tk.END)
    )
    menu.add_command(label="Open", underline=0, command=lambda: print("Open file"))
    menu.add_command(label="Save", underline=0, command=lambda: print("Save file"))
    menu.add_command(label="Save As", underline=5, command=lambda: print("Save file"))
    menu.add_command(label="Print", underline=0, command=lambda: print("Print file"))
    menu.add_separator()
    menu.add_command(label="Exit", underline=1, command=root.quit)
    menu_bar.add_cascade(label="File", menu=menu)

    # Add "Edit" menu
    menu = tk.Menu(menu_bar, tearoff=0)
    menu.add_command(
        label="Undo",
        underline=0,
        command=lambda: root.focus_get().event_generate("<<Undo>>"),
    )
    menu.add_command(
        label="Redo",
        underline=0,
        command=lambda: root.focus_get().event_generate("<<Redo>>"),
    )
    menu.add_separator()
    menu.add_command(
        label="Cut",
        underline=0,
        command=lambda: root.focus_get().event_generate("<<Cut>>"),
    )
    menu.add_command(
        label="Copy",
        underline=3,
        command=lambda: root.focus_get().event_generate("<<Copy>>"),
    )
    menu.add_command(
        label="Paste",
        underline=0,
        command=lambda: root.focus_get().event_generate("<<Paste>>"),
    )
    menu_bar.add_cascade(label="Edit", menu=menu)

    # Add "Help" menu
    menu = tk.Menu(menu_bar, tearoff=0)
    menu.add_command(label="About", underline=0, command=about)
    menu_bar.add_cascade(label="Help", menu=menu)

    # Configure the menu bar in the root window
    root.config(menu=menu_bar)

    # Create a toolbar frame
    toolbar_frame = tk.Frame(root, bd=1, relief="raised")
    toolbar_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

    # Add buttons to the toolbar
    create_button("add", "New", lambda: text_widget.delete("1.0", tk.END))
    create_button("folder_open", "Open", lambda: print())
    create_button("save", "Save", lambda: print())
    create_button("print", "Print", lambda: print())
    separator()
    create_button(
        "content_cut", "Cut", lambda: root.focus_get().event_generate("<<Cut>>")
    )
    create_button(
        "content_copy", "Copy", lambda: root.focus_get().event_generate("<<Copy>>")
    )
    create_button(
        "content_paste", "Paste", lambda: root.focus_get().event_generate("<<Paste>>")
    )
    separator()
    create_button("undo", "Undo", lambda: root.focus_get().event_generate("<<Undo>>"))
    create_button("redo", "Redo", lambda: root.focus_get().event_generate("<<Redo>>"))
    separator()
    create_button("format_bold", "Bold", bold)
    create_button("format_italic", "Italic", bold)
    create_button("format_strikethrough", "Strikethrough", bold)
    separator()
    create_button("insert_link", "Insert link", bold)
    separator()
    create_button("done", "Move finished text to clipboard", done)

    # Create a custom font for the Text widget
    text_font = font.Font(family="Consolas", size=12)

    # Create the main text widget that occupies most of the screen
    text_widget = tk.Text(root, font=text_font, undo=True)
    text_widget.grid(row=1, column=2, rowspan=21, sticky="nsew")
    text_widget.focus_set()

    # Stop the cursor from blinking
    text_widget.config(insertontime=0, insertofftime=0)

    # Frame to hold the cells on the left side of the text widget
    cell_frame = tk.Frame(root)
    cell_frame.grid(row=2, column=0, columnspan=2, rowspan=20, sticky="ns")

    # Configure the left column layout for 20 rows
    for row in range(20):
        cell_frame.grid_rowconfigure(row, weight=1)

    # Store read-only label references for programmatic updates
    suggestion_cells = []

    for i in range(20):
        # Create label for the identifier (e.g., 'F1', 'F2', etc.)
        if i < 9:
            label_text = str(i + 1)
        elif i == 9:
            label_text = "0"
        else:
            label_text = f"F{i-9}"
        label_id = tk.Label(cell_frame, text=label_text, anchor="e")
        label_id.grid(row=21 - i, column=0, sticky="e", padx=2, pady=2)

        # Create read-only suggestion label
        read_only_text = tk.Label(
            cell_frame, text="", anchor="w", relief="sunken", width=20
        )
        read_only_text.grid(row=21 - i, column=1, sticky="ew", padx=2, pady=2)

        # Store the label for programmatic access
        suggestion_cells.append(read_only_text)

    # Suggestions
    suggestions = []

    # Bind key events
    root.bind("<F12>", lambda event: done())
    text_widget.bind("<KeyRelease>", on_key_release)

    # Run the Tkinter event loop
    root.mainloop()
