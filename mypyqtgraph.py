import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
import time

class Main(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time(초)', units=None)
        self.enableAutoSIPrefix(False)
