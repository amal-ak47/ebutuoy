import os
import sys
from urllib.request import urlopen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QRadioButton, QButtonGroup


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ebutouy")
        self.resize(600, 600)
        self.center()

        main_layout = QVBoxLayout()
        text_box_layout = QHBoxLayout()
        video_box_layout = QHBoxLayout()
        video_description_layout = QVBoxLayout()
        format_btn_layout = QVBoxLayout()

        heading = QLabel("Ebutouy")
        url_box = QLineEdit()
        search_btn = QPushButton("Get video")
        download_btn = QPushButton("Download")


        vid_thumbnail = QLabel(self)
        url = 'https://static1.squarespace.com/static/5ceafa407824f80001793b84/5ceafcab6e9a7f68cda0e90b/5e3b3db0620bc34f20b7f7a4/1697669435090/some-any.jpg?format=1500w'
        thumbnail_data = urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(thumbnail_data)
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        resolution_combo_box = QComboBox()
        resolution_combo_box.addItems(["360p", "480p"])
        vid_thumbnail.setPixmap(pixmap)
        vid_title = QLabel("Some vid")
        vid_views = QLabel("1000")
        vid_author = QLabel("AK")
        mp3_radio_btn = QRadioButton("Mp3")
        mp4_radio_btn = QRadioButton("Mp4")
        format_btn_group = QButtonGroup()
        format_btn_group.addButton(mp3_radio_btn)
        format_btn_group.addButton(mp4_radio_btn)
        mp4_radio_btn.setChecked(True)

        video_box_layout.addWidget(vid_thumbnail)
        video_box_layout.addLayout(video_description_layout)
        video_box_layout.addLayout(format_btn_layout)
        video_description_layout.addWidget(vid_title)
        video_description_layout.addWidget(vid_views)
        video_description_layout.addWidget(vid_author)
        video_description_layout.addWidget(resolution_combo_box)
        format_btn_layout.addWidget(mp4_radio_btn)
        format_btn_layout.addWidget(mp3_radio_btn)
        video_box_layout.addWidget(download_btn)

        main_layout.addWidget(heading)
        text_box_layout.addWidget(url_box)
        text_box_layout.addWidget(search_btn)
        main_layout.addLayout(text_box_layout)
        main_layout.addLayout(video_box_layout)
        self.setLayout(main_layout)

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