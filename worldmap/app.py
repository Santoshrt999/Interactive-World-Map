import sys
from PyQt6.QtWidgets import QApplication

from .controller import MapController
from .model import MapModel
from .view import MainWindow


class WorldAtlasApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")
        self.model = MapModel()
        self.window = MainWindow(self.model)
        self.controller = MapController(self.model, self.window)

    def run(self):
        self.window.show()
        return self.app.exec()
