# connects everything basically
import sys #access to system specific parameters

from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

#calls other files
from .config import APP_NAME, HOTKEY_LABEL
from .hotkey import HotkeyBridge, start_hotkey
from .icon import app_icon
from .manager import Manager
from .sidebar import Sidebar
from .storage import ensure_dirs


def run():
    ensure_dirs()

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setQuitOnLastWindowClosed(False)    #bound to tray not window

    sidebar = Sidebar()
    manager = Manager()
    manager.library_changed.connect(    #opens one if close other
        lambda: sidebar.reload() if sidebar.isVisible() else None
    )

    tray = QSystemTrayIcon(app_icon())
    tray.setToolTip(f"{APP_NAME} ({HOTKEY_LABEL})")
    menu = QMenu()
    menu.addAction("Open Manager", manager.show_window)
    menu.addAction("Toggle Sidebar", sidebar.toggle)
    menu.addSeparator()
    menu.addAction("Exit", app.quit)
    tray.setContextMenu(menu)
    tray.activated.connect(
        lambda reason: manager.show_window()
        if reason == QSystemTrayIcon.Trigger else None
    )
    tray.show()

    bridge = HotkeyBridge()                                 #command to toggle sidebar
    bridge.triggered.connect(sidebar.toggle)
    listener = start_hotkey(bridge)

    exit_code = app.exec()
    listener.stop()
    sys.exit(exit_code)