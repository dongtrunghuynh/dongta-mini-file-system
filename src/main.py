
from gui_os import OSSelectionGUI
from gui_main import FileSystemGUI

def start_app():
    # Launch OS selection window
    user_os = OSSelectionGUI().run()  # Returns 'Windows' or 'Mac'
    
    # Launch main file system GUI with selected OS
    FileSystemGUI(user_os).run()

if __name__ == "__main__":
    start_app()

