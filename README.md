# Mini File System

A Python GUI tool that simulates a simple file system with **nested folders and files**, built using **Tkinter**.  
Users can select their OS (Windows or Mac) and interact with an **in-memory file system**, including creating files/folders, navigating nested directories, and using a "Go Up" button to move to parent folders.

---

## Features

- OS selection: Windows or Mac  
- Nested folders support  
- Create files and folders in any directory  
- Navigate into folders by double-clicking  
- "Go Up" button to move to parent folder  
- Visual distinction between files and folders  
- Entirely in-memory, no disk changes (safe sandbox)  

---

## Folder Structure

dongta-mini-file-system/
- └── src/
- ├── main.py # Entry point
- ├── gui_os.py # OS selection window
- ├── gui_main.py # Main GUI with Treeview
- └── filesystem.py # In-memory file system backend