import tkinter as tk
from tkinter import ttk

class OSSelectionGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Select OS")
        self.os_var = tk.StringVar(value="Windows")
        self.selection = None

    def run(self):
        ttk.Label(self.root, text="Select your OS:").pack(pady=10)
        ttk.Radiobutton(self.root, text="Windows", variable=self.os_var, value="Windows").pack()
        ttk.Radiobutton(self.root, text="Mac OS", variable=self.os_var, value="Mac").pack()
        ttk.Button(self.root, text="Confirm", command=self.confirm).pack(pady=10)
        self.root.mainloop()
        return self.selection

    def confirm(self):
        self.selection = self.os_var.get()
        self.root.destroy()

