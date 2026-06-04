# self-explanatory
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QGuiApplication, QPixmap
from PySide6. QtWidgets import(
    QApplication, QListWidget, QListWidgetItem, QVBoxLayout, QWidget,
)

from .common import make_item       # creates file
from .config import THUMB           #Thumbnail (?)
from .storage import load_library   #gets library

_LIST_STYLE = ( #format of list
    "QListWidget{background:#1e1e1e;border:none;}"
    "QListWidget::item{padding:4px;}"
    "QListWidget::item:selected{background:#4c6ef5;border-radius:6px;}"
)


class KeyList(QListWidget):
    #List that emits on Enter and Escape
    activatedItem = Signal(QListWidgetItem)
    escaped = Signal()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            item = self.currentItem()
            if item:
                self.activatedItem.emit(item)
        elif e.key() == Qt.Key_Escape:
            self.escaped.emit()
        else:
            super().keyPressEvent(e)

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.list = KeyList()
        self.list.setIconSize(THUMB)
        self.list.setSpacing(4)
        self.list.setStyleSheet(_LIST_STYLE)
        

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.list)

        self.list.activatedItem.connect(self.copy_item)
        self.list.itemDoubleClicked.connect(self.copy_item)
        self.list.escaped.connect(self.hide)

    def reload(self):
        self.list.clear()
        for path in load_library():
            self.list.addItem(make_item(path))

    def position(self):
        g = QGuiApplication.primaryScreen().availableGeometry()
        self.setGeometry(g.x(), g.y(), 190, g.height())

    def copy_item(self, item):
        pm = QPixmap(item.data(Qt.UserRole))
        if not pm.isNull():
            QApplication.clipboard().setPixmap(pm)
        self.hide()

    def toggle(self):
        if self.isVisible():
            self.hide()
            return
        self.reload()
        self.position()
        self.show()
        self.raise_()
        self.activateWindow()
        self.list.setFocus()
        if self.list.count():
            self.list.setCurrentRow(0)