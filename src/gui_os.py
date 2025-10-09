import tkinter as tk
from tkinter import ttk, simpledialog
from filesystem import InMemoryFileSystem

class FileSystemGUI:
    def __init__(self, user_os):
        self.user_os = user_os
        self.root = tk.Tk()
        self.root.title(f"Mini File System - {self.user_os}")
        self.fs = InMemoryFileSystem()
        self.current_path = ["root"]

        # Treeview
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.open_folder)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Create File", command=self.create_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Create Folder", command=self.create_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Go Up", command=self.go_up).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_tree).pack(side=tk.LEFT, padx=5)

        self.refresh_tree()

    def run(self):
        self.root.mainloop()

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        items = self.fs.list_items(self.current_path)
        for item in items:
            if isinstance(self.fs._get_folder(self.current_path + [item]), dict):
                # Folder
                self.tree.insert("", "end", text=item, open=True)
            else:
                # File
                self.tree.insert("", "end", text=item)

    def create_file(self):
        name = simpledialog.askstring("Create File", "Enter file name:")
        if name:
            self.fs.create_file(self.current_path, name)
            self.refresh_tree()

    def create_folder(self):
        name = simpledialog.askstring("Create Folder", "Enter folder name:")
        if name:
            self.fs.create_folder(self.current_path, name)
            self.refresh_tree()

    def open_folder(self, event):
        selected = self.tree.selection()
        if selected:
            folder_name = self.tree.item(selected[0])["text"]
            # Only open if it's a folder
            if isinstance(self.fs._get_folder(self.current_path + [folder_name]), dict):
                self.current_path.append(folder_name)
                self.refresh_tree()

    def go_up(self):
        if len(self.current_path) > 1:
            self.current_path.pop()
            self.refresh_tree()

