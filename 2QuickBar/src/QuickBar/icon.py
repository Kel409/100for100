# this is to have an icon in the taskbar
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap

from .config import APP_DIR

#to get repository root in src/image_library/icon.py
ASSETS = Path(__file__).resolve().parents[2] / "assets" #goes up 2 files

def app_icon():
    for candidate in (APP_DIR / "icon.ico", ASSETS / "icon.ico"):
        if candidate.exists():
            return QIcon(str(candidate))
    return _placeholder_icon()

def _placeholder_icon():
    pm = QPixmap(64, 64)    #icon size
    pm.fill(Qt.transparent) #transparent bg
    p = QPainter(pm)        #highkey I think the rest is just a generic icon
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor("#4c6ef5"))
    p.drawRoundedRect(4, 4, 56, 56, 14, 14)
    p.setBrush(QColor("white"))
    p.drawRect(16, 22, 32, 22)
    p.setBrush(QColor("#4c6ef5"))
    p.drawEllipse(22, 27, 8, 8)
    p.end()
    return QIcon(pm)