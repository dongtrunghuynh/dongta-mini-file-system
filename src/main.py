
from gui_os import OSSelectionGUI
from gui_main import FileSystemGUI

def start_app():
    user_os = OSSelectionGUI().run()  # Windows or Mac
    FileSystemGUI(user_os).run()

if __name__ == "__main__":
    start_app()

