# tools used by both sidebar and manager
from pathlib import Path #module for system paths

from PySide6.QtCore import Qt #PySide6 basically for building GUIs
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QListWidgetItem

from .config import THUMB


def make_item(path, with_text=False):
    # build list item w thumbnail, stored in UserRole
    thumb = QPixmap(path).scaled(THUMB, Qt.KeepAspectRatio, Qt.SmoothTransformation) #thumbnail
    item = QListWidgetItem(QIcon(thumb), Path(path).name if with_text else "")       #add text (tentatitve) 
    item.setData(Qt.UserRole, path)                                                  #set data
    return item