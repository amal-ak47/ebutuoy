import os
import sys
from urllib.request import urlopen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QRadioButton, QButtonGroup

from utils.custom_exception import InvalidURLError, DownloadFailedError, MetadataError, NoStreamsError, \
    FileOperationError
from utils.single_downloader import SingleDownloader


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ebutouy")
        self.resize(600, 600)
        self.center()

        self.main_layout = QVBoxLayout()
        self.text_box_layout = QHBoxLayout()
        self.text_box_layout.setSpacing(20)
        self.main_layout.setSpacing(20)
        self.video_box_layout = QHBoxLayout()
        self.video_box_layout.setSpacing(10)

        self.video_description_layout = QVBoxLayout()
        self.format_btn_layout = QVBoxLayout()

        heading = QLabel("Ebutouy")
        heading.setAlignment(Qt.AlignCenter)
        self.url_box = QLineEdit()
        search_btn = QPushButton("Get video")
        search_btn.clicked.connect(self.search_function)


        self.main_layout.addWidget(heading)
        self.text_box_layout.addWidget(self.url_box)
        self.text_box_layout.addWidget(search_btn)
        self.main_layout.addLayout(self.text_box_layout)

        self.main_layout.addLayout(self.video_box_layout)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def search_function(self):
        while self.video_box_layout.count():
            widget = self.video_box_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        while self.video_description_layout.count():
            widget = self.video_description_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        while self.format_btn_layout.count():
            widget = self.format_btn_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        self.url_text = self.url_box.text()
        self.url_box.clear()
        if "list=" in self.url_text:
            ...
        elif "v=" in self.url_text or "shorts/" in self.url_text:
            try:
                self.downloader = SingleDownloader(self.url_text)

                vid_thumbnail = QLabel(self)
                url = str(self.downloader.thumbnail)
                thumbnail_data = urlopen(url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(thumbnail_data)
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.resolution_combo_box = QComboBox()
                self.resolutions = self.downloader.get_resolutions_video()
                self.resolution_combo_box.addItems(self.resolutions)
                vid_thumbnail.setPixmap(pixmap)
                vid_title = QLabel(f"Title: {self.downloader.yt.title}")
                vid_views = QLabel(f"Views: {self.downloader.yt.views}")
                vid_author = QLabel(f"Channel: {self.downloader.yt.author}")
                self.mp3_radio_btn = QRadioButton("Mp3")
                self.mp4_radio_btn = QRadioButton("Mp4")
                format_btn_group = QButtonGroup()
                format_btn_group.addButton(self.mp3_radio_btn)
                format_btn_group.addButton(self.mp4_radio_btn)
                self.mp4_radio_btn.setChecked(True)
                download_btn = QPushButton("Download")
                download_btn.clicked.connect(self.download_vid)

                self.mp3_radio_btn.toggled.connect(self.on_format_changed)
                self.mp4_radio_btn.toggled.connect(self.on_format_changed)

                self.video_box_layout.addWidget(vid_thumbnail)
                self.video_box_layout.addLayout(self.video_description_layout)
                self.video_box_layout.addLayout(self.format_btn_layout)
                self.video_description_layout.addWidget(vid_title)
                self.video_description_layout.addWidget(vid_views)
                self.video_description_layout.addWidget(vid_author)
                self.video_description_layout.addWidget(self.resolution_combo_box)
                self.format_btn_layout.addWidget(self.mp4_radio_btn)
                self.format_btn_layout.addWidget(self.mp3_radio_btn)
                self.video_box_layout.addWidget(download_btn)
            except (InvalidURLError, DownloadFailedError, NoStreamsError, MetadataError, FileOperationError) as e:
                error_label = QLabel(e)
                error_label.setAlignment(Qt.AlignCenter)
                self.video_box_layout.addWidget(error_label)
        else:
            error_label = QLabel("Not Valid URL")
            error_label.setAlignment(Qt.AlignCenter)
            self.video_box_layout.addWidget(error_label)

    def download_vid(self):
        if self.mp4_radio_btn.isChecked():
            self.downloader.single_video_download(self.resolution_combo_box.currentText())
            self.downloader.video_meta()
        elif self.mp3_radio_btn.isChecked():
            self.downloader.single_audio_download(self.resolution_combo_box.currentText())
            self.downloader.audio_meta()

    def on_format_changed(self):
        if self.mp3_radio_btn.isChecked():
            self.resolution_combo_box.clear()
            self.resolutions = self.downloader.get_resolutions_audio()
            self.resolution_combo_box.addItems(self.resolutions)
        elif self.mp4_radio_btn.isChecked():
            self.resolution_combo_box.clear()
            self.resolutions = self.downloader.get_resolutions_video()
            self.resolution_combo_box.addItems(self.resolutions)

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