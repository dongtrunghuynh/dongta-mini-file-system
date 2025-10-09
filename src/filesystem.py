class File:
    def __init__(self, content=""):
        self.content = content

class Directory:
    def __init__(self):
        self.children = {}  # name -> File or Directory

class InMemoryFileSystem:
    def __init__(self):
        self.root = Directory()

    def _get_node(self, path):
        """Traverse the path and return node (Directory or File), or None if missing"""
        current = self.root
        for p in path:
            if not isinstance(current, Directory):
                return None
            if p not in current.children:
                return None
            current = current.children[p]
        return current

    def mkdir(self, path):
        """Create a directory at the given path, without overwriting files"""
        if not path:
            return False, "Path cannot be empty"
        current = self.root
        for p in path:
            if p in current.children:
                if isinstance(current.children[p], File):
                    return False, f"Cannot create folder, file exists at {p}"
                # already exists as folder → continue
            else:
                current.children[p] = Directory()
            current = current.children[p]
        return True, "Directory created"

    def create_file(self, path, name, content=""):
        """Create a file with content under the given path"""
        folder = self._get_node(path)
        if folder is None:
            return False, "Parent path does not exist"
        if name in folder.children:
            if isinstance(folder.children[name], Directory):
                return False, "Cannot overwrite directory with file"
        folder.children[name] = File(content)
        return True, "File created"

    def read_file(self, path, name):
        folder = self._get_node(path)
        if folder is None or name not in folder.children:
            return False, "File not found"
        node = folder.children[name]
        if isinstance(node, File):
            return True, node.content
        return False, "Path is a directory"

    def delete_file(self, path, name):
        folder = self._get_node(path)
        if folder is None or name not in folder.children:
            return False, "File not found"
        if isinstance(folder.children[name], Directory):
            return False, "Cannot DELETE a directory"
        del folder.children[name]
        return True, "File deleted"

    def rmdir(self, path, recursive=False):
        """Remove directory at path; recursive deletes children if recursive=True"""
        if not path:
            return False, "Cannot delete root"
        parent_path = path[:-1]
        dir_name = path[-1]
        parent = self._get_node(parent_path)
        if parent is None or dir_name not in parent.children:
            return False, "Directory not found"
        node = parent.children[dir_name]
        if not isinstance(node, Directory):
            return False, "Path is not a directory"
        if node.children and not recursive:
            return False, "Directory not empty"
        del parent.children[dir_name]
        return True, "Directory deleted"

    def list_items(self, path):
        folder = self._get_node(path)
        if folder is None or not isinstance(folder, Directory):
            return []
        return folder.children.keys()


