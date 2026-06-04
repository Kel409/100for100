#global hotkey

from PySide6.QtCore import QObject, Signal #GUI module
from pynput import keyboard #keyboard module

from .config import HOTKEY


class HotkeyBridge(QObject):
    triggered = Signal()

def start_hotkey(bridge):
    #starts listening to stop() on exit
    listener = keyboard.GlobalHotKeys({HOTKEY: bridge.triggered.emit})
    listener.start()
    return listener