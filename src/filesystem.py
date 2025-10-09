class InMemoryFileSystem:
    def __init__(self):
        # root is a dict: folder_name -> dict (subfolders/files)
        self.fs = {"root": {}}

    def list_items(self, path=["root"]):
        """Return items at a given path."""
        folder = self._get_folder(path)
        return folder.keys() if folder else []

    def create_file(self, path, file_name):
        folder = self._get_folder(path)
        if folder is not None:
            folder[file_name] = None  # Files are None, folders are dicts

    def create_folder(self, path, folder_name):
        folder = self._get_folder(path)
        if folder is not None:
            folder[folder_name] = {}  # New folder is empty dict

    def _get_folder(self, path):
        """Traverse nested folders by path list."""
        current = self.fs
        for p in path:
            if p in current and isinstance(current[p], dict):
                current = current[p]
            else:
                return None
        return current


