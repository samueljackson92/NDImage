import os.path
from PyQt4 import uic


def get_ui_file(file_name):
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "ui")
    path = os.path.join(path, file_name)
    return uic.loadUiType(path)[0]

import main_window
