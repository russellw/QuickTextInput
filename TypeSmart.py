import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("TypeSmart")

# Create a larger Text widget
text_field = tk.Text(root, height=20, width=80, wrap=tk.WORD)
text_field.pack(pady=10)
