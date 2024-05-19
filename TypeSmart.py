import tkinter as tk


def copy_to_clipboard():
    # Get the text from the text field
    text = text_field.get("1.0", tk.END)
    # Clear the clipboard
    root.clipboard_clear()
    # Append the text to the clipboard
    root.clipboard_append(text)
    # Update the clipboard
    root.update()


# Create the main window
root = tk.Tk()
root.title("TypeSmart")

# Create a larger Text widget
text_field = tk.Text(root, height=20, width=80, wrap=tk.WORD)
text_field.pack(pady=10)
text_field.focus_set()

# Create the copy button
copy_button = tk.Button(root, text="Copy (F12)", command=copy_to_clipboard)
copy_button.pack(pady=10, anchor="e")

# Bind the F12 key to the copy_to_clipboard function
root.bind("<F12>", lambda event: copy_to_clipboard())

# Run the Tkinter event loop
root.mainloop()
