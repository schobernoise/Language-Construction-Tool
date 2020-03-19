from PyQt5.QtCore import QObject, pyqtSignal
from controllers import utils
from controllers import log

import sqlite3
from sqlite3 import Error

class start_info(QObject):
    
    def __init__(self):
        super().__init__()