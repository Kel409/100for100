#configuration for application
import os #self-explanatory
from pathlib import Path #path to items

from PySide6.QtCore import QSize #GUI module

APP_NAME = "QuickBar"

# --- FEEL FREE TO CHANGE ANYTHING ---
HOTKEY = "<ctrl>+<alt>+i"
HOTKEY_LABEL = "Ctrl+Alt+I" #human-readable

THUMB = QSize(160, 160)
# ------------------------------------

#Storage for user, copied so library persists after resets
APP_DIR = Path(os.getenv("APPDATA", str(Path.home()))) / "QuickBar" 
IMAGES_DIR = APP_DIR / "images"
LIBRARY_JSON = APP_DIR / "library.json"
