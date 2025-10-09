import tkinter as tk
from tkinter import ttk

def select_os():
    selected = os_var.get()
    print(f"User selected OS: {selected}")

root = tk.Tk()
root.title("Mini File System - OS Selection")

os_var = tk.StringVar(value="Windows")  # default

ttk.Label(root, text="Select your OS:").pack(pady=10)

ttk.Radiobutton(root, text="Windows", variable=os_var, value="Windows").pack()
ttk.Radiobutton(root, text="Mac OS", variable=os_var, value="Mac").pack()

ttk.Button(root, text="Confirm", command=select_os).pack(pady=10)

root.mainloop()

