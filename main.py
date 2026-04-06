import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QListView, \
    QListWidget, QComboBox, QFileDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ebutouy")
        self.resize(600, 600)
        self.center()

    def center(self) -> None:
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)


def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()