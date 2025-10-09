import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from filesystem import InMemoryFileSystem, Directory, File

class FileSystemGUI:
    def __init__(self, user_os):
        self.user_os = user_os
        self.root = tk.Tk()
        self.root.title(f"Mini File System - {self.user_os}")
        self.fs = InMemoryFileSystem()
        self.current_path = []

        # Treeview
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.open_folder)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Create File", command=self.create_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Create Folder", command=self.create_folder).pack(side=tk.LEFT, padx=5)
        self.btn_go_up = tk.Button(btn_frame, text="Go Up", command=self.go_up)
        self.btn_go_up.pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_item).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_tree).pack(side=tk.LEFT, padx=5)

        self.refresh_tree()

    def run(self):
        self.root.mainloop()

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        items = self.fs.list_items(self.current_path)
        for item in items:
            node = self.fs._get_node(self.current_path + [item])
            if isinstance(node, Directory):
                self.tree.insert("", "end", text=f"[Folder] {item}", open=True)
            else:
                self.tree.insert("", "end", text=item)
        self.btn_go_up.config(state=tk.DISABLED if not self.current_path else tk.NORMAL)

    def create_folder(self):
        name = simpledialog.askstring("Create Folder", "Enter folder name:")
        if not name:
            return

        node = self.fs._get_node(self.current_path)
        if node is None:
            messagebox.showerror("Error", "Current folder does not exist.")
            return

        # Check if a file with the same name exists
        if name in node.children and isinstance(node.children[name], File):
            messagebox.showwarning(
                "Cannot Create Folder",
                f"A file with the name '{name}' already exists in this directory."
            )
            return

        # Check if a folder with the same name exists
        if name in node.children and isinstance(node.children[name], Directory):
            messagebox.showwarning(
                "Cannot Create Folder",
                f"A folder with the name '{name}' already exists in this directory."
            )
            return

        # Create the folder
        success, msg = self.fs.mkdir(self.current_path + [name])
        if not success:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Success", f"Folder '{name}' created successfully.")

        self.refresh_tree()


    def create_file(self):
        name = simpledialog.askstring("Create File", "Enter file name:")
        if not name:
            return

        node = self.fs._get_node(self.current_path)
        if node is None:
            messagebox.showerror("Error", "Current folder does not exist.")
            return

        # Prevent file creation if a folder with the same name exists
        if name in node.children and isinstance(node.children[name], Directory):
            messagebox.showwarning(
                "Cannot Create File",
                f"A folder with the name '{name}' already exists in this directory."
            )
            return

        # Prevent file creation if a file with the same name exists
        if name in node.children and isinstance(node.children[name], File):
            messagebox.showwarning(
                "Cannot Create File",
                f"A file with the name '{name}' already exists in this directory."
            )
            return

        content = simpledialog.askstring("File Content", "Enter content for the file:")
        success, msg = self.fs.create_file(self.current_path, name, content or "")
        if not success:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Success", f"File '{name}' created successfully.")
        self.refresh_tree()

    def open_folder(self, event):
        selected = self.tree.selection()
        if selected:
            text = self.tree.item(selected[0])["text"]
            if text.startswith("[Folder] "):
                folder_name = text.replace("[Folder] ", "")
                self.current_path.append(folder_name)
                self.refresh_tree()

    def go_up(self):
        if self.current_path:
            self.current_path.pop()
            self.refresh_tree()

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No item selected")
            return

        text = self.tree.item(selected[0])["text"]

        if text.startswith("[Folder] "):
            folder_name = text.replace("[Folder] ", "")
            node = self.fs._get_node(self.current_path + [folder_name])

            # Check if folder is non-empty
            if isinstance(node, Directory) and node.children:
                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    f"The folder '{folder_name}' is not empty.\n"
                    "Deleting it will also delete all its contents.\n"
                    "Do you want to proceed?"
                )
                if not confirm:
                    return  # User cancelled deletion

            success, msg = self.fs.rmdir(self.current_path + [folder_name], recursive=True)
        else:
            file_name = text
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete the file '{file_name}'?"
            )
            if not confirm:
                return
            success, msg = self.fs.delete_file(self.current_path, file_name)

        if not success:
            messagebox.showerror("Error", msg)
        self.refresh_tree()
