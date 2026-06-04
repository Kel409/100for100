# manager window to add, remove, reorder, exit application
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import(
    QApplication, QFileDialog, QHBoxLayout, QLabel, QListWidget, QPushButton,
    QVBoxLayout, QWidget, #WHY IS THERE THIRTY IMPORTS
)

from .common import make_item                                   # function to add to library
from .config import APP_NAME, THUMB                             # appname and thumbail
from .storage import import_image, load_library, save_library   # what do you think man

_IMAGE_FILTER = "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"


class Manager(QWidget):
    library_changed = Signal()

    def __init__(self):
        super().__init__()                  #creating window and size
        self.setWindowTitle(APP_NAME)
        self.resize(420, 560)

        self.list = QListWidget()           #browsing (?)
        self.list.setIconSize(THUMB)
        self.list.setDragDropMode(QListWidget.InternalMove)
        self.list.model().rowsMoved.connect(self.persist)

        add_btn = QPushButton("Add Images") #buttons
        rm_btn = QPushButton("Remove Selected")
        add_btn.clicked.connect(self.add_images)
        rm_btn.clicked.connect(self.remove_selected)

        exit_btn = QPushButton("Exit Application")
        exit_btn.clicked.connect(QApplication.instance().quit)

        actions = QHBoxLayout()             #shows buttons
        actions.addWidget(add_btn) 
        actions.addWidget(rm_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Drag to reorder. Order saves automatically."))
        layout.addWidget(self.list)
        layout.addLayout(actions)
        layout.addWidget(exit_btn)

        self.reload()

    def reload(self):   #refresh
        self.list.clear()
        for path in load_library():
            self.list.addItem(make_item(path, with_text=True))

    def current_paths(self):
        return [self.list.item(i).data(Qt.UserRole) for i in range(self.list.count())]

    def persist(self, *_):
        save_library(self.current_paths())
        self.library_changed.emit()

    def add_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Add Images", "", _IMAGE_FILTER)
        for f in files:
            self.list.addItem(make_item(import_image(f), with_text=True))
        if files:
            self.persist()

    def remove_selected(self):
        for item in self.list.selectedItems():
            self.list.takeItem(self.list.row(item))
        self.persist()

    def show_window(self):
        self.reload()
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, e):
        #close window to tray
        e.ignore()
        self.hide()