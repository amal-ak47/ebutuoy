import sys
from urllib.request import urlopen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, \
    QRadioButton, QButtonGroup, QScrollArea

from utils.custom_exception import InvalidURLError, DownloadFailedError, MetadataError, NoStreamsError, \
    FileOperationError
from utils.playlist import PlaylistDownloader
from utils.single_downloader import SingleDownloader


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ebutouy")
        self.setFixedSize(600, 600)
        self.center()

        self.main_layout = QVBoxLayout()
        self.text_box_layout = QHBoxLayout()
        self.text_box_layout.setSpacing(20)
        self.main_layout.setSpacing(20)

        heading = QLabel("Ebutouy")
        heading.setAlignment(Qt.AlignCenter)
        self.url_box = QLineEdit()
        search_btn = QPushButton("Get video")
        search_btn.clicked.connect(self.search_function)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFixedHeight(300)
        scroll_widget = QWidget()
        self.video_box_layout = QVBoxLayout(scroll_widget)
        self.video_box_layout.setSpacing(20)
        scroll_area.setWidget(scroll_widget)

        self.main_layout.addWidget(heading)
        self.text_box_layout.addWidget(self.url_box)
        self.text_box_layout.addWidget(search_btn)
        self.main_layout.addLayout(self.text_box_layout)
        self.main_layout.addWidget(scroll_area)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def search_function(self):
        while self.video_box_layout.count():
            item = self.video_box_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
        self.url_text = self.url_box.text()
        self.url_box.clear()
        if "list=" in self.url_text:
            try:
                self.downloader = PlaylistDownloader(self.url_text)
                for vid in self.downloader.playlist.videos:
                    video_description_layout = QVBoxLayout()

                    vid_thumbnail = QLabel(self)
                    url = str(vid.thumbnail_url)
                    thumbnail_data = urlopen(url).read()
                    pixmap = QPixmap()
                    pixmap.loadFromData(thumbnail_data)
                    pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    vid_thumbnail.setPixmap(pixmap)
                    vid_title = QLabel(f"Title: {vid.title}")
                    vid_title.setWordWrap(True)
                    vid_views = QLabel(f"Views: {vid.views}")
                    vid_views.setWordWrap(True)
                    vid_author = QLabel(f"Channel: {vid.author}")
                    vid_author.setWordWrap(True)

                    video_description_layout.addWidget(vid_title)
                    video_description_layout.addWidget(vid_views)
                    video_description_layout.addWidget(vid_author)

                    thumbnail_layout = QVBoxLayout()
                    thumbnail_layout.setContentsMargins(0, 0, 0, 0)
                    thumbnail_layout.addWidget(vid_thumbnail)

                    video_item_layout = QHBoxLayout()
                    video_item_layout.setSpacing(15)
                    video_item_layout.setContentsMargins(0, 0, 0, 0)
                    video_item_layout.addLayout(thumbnail_layout)
                    video_item_layout.addLayout(video_description_layout, 1)
                    video_item_layout.addStretch()

                    self.video_box_layout.addLayout(video_item_layout)

                self.format_btn_layout = QVBoxLayout()
                self.mp3_radio_btn = QRadioButton("Mp3")
                self.mp4_radio_btn = QRadioButton("Mp4")
                self.format_btn_group = QButtonGroup()
                self.format_btn_group.addButton(self.mp3_radio_btn)
                self.format_btn_group.addButton(self.mp4_radio_btn)
                self.mp4_radio_btn.setChecked(True)
                download_btn = QPushButton("Download")
                download_btn.clicked.connect(self.download_playlist)

                self.format_btn_layout.addWidget(self.mp4_radio_btn)
                self.format_btn_layout.addWidget(self.mp3_radio_btn)
                self.format_btn_layout.addWidget(download_btn)

                self.main_layout.addLayout(self.format_btn_layout)

            except (InvalidURLError, DownloadFailedError, NoStreamsError, MetadataError, FileOperationError) as e:
                error_label = QLabel(str(e))
                error_label.setAlignment(Qt.AlignCenter)
                self.video_box_layout.addWidget(error_label)

        elif "v=" in self.url_text or "shorts/" in self.url_text:
            try:
                self.downloader = SingleDownloader(self.url_text)
                self.video_description_layout = QVBoxLayout()
                self.format_btn_layout = QVBoxLayout()

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
                vid_title.setWordWrap(True)
                vid_views = QLabel(f"Views: {self.downloader.yt.views}")
                vid_views.setWordWrap(True)
                vid_author = QLabel(f"Channel: {self.downloader.yt.author}")
                vid_author.setWordWrap(True)

                self.mp3_radio_btn = QRadioButton("Mp3")
                self.mp4_radio_btn = QRadioButton("Mp4")
                self.format_btn_group = QButtonGroup()
                self.format_btn_group.addButton(self.mp3_radio_btn)
                self.format_btn_group.addButton(self.mp4_radio_btn)
                self.mp4_radio_btn.setChecked(True)
                download_btn = QPushButton("Download")
                download_btn.clicked.connect(self.download_vid)
                self.mp3_radio_btn.toggled.connect(self.on_format_changed)
                self.mp4_radio_btn.toggled.connect(self.on_format_changed)

                self.video_description_layout.addWidget(vid_title)
                self.video_description_layout.addWidget(vid_views)
                self.video_description_layout.addWidget(vid_author)
                self.video_description_layout.addWidget(self.resolution_combo_box)
                self.format_btn_layout.addWidget(self.mp4_radio_btn)
                self.format_btn_layout.addWidget(self.mp3_radio_btn)

                video_item_layout = QHBoxLayout()
                video_item_layout.addWidget(vid_thumbnail)
                video_item_layout.addLayout(self.video_description_layout)
                video_item_layout.addLayout(self.format_btn_layout)
                video_item_layout.addWidget(download_btn)

                self.video_box_layout.addLayout(video_item_layout)
            except (InvalidURLError, DownloadFailedError, NoStreamsError, MetadataError, FileOperationError) as e:
                error_label = QLabel(str(e))
                error_label.setAlignment(Qt.AlignCenter)
                self.video_box_layout.addWidget(error_label)
        else:
            error_label = QLabel("Not Valid URL")
            error_label.setAlignment(Qt.AlignCenter)
            self.video_box_layout.addWidget(error_label)

    def download_playlist(self):
        if self.mp4_radio_btn.isChecked():
            try:
                self.downloader.video_download()
                self.downloader.change_video_meta()
            except (FileOperationError, Exception) as e:
                error_label = QLabel(f"Download failed: {str(e)}\nTry again later")
                error_label.setAlignment(Qt.AlignCenter)
                self.video_box_layout.addWidget(error_label)
        elif self.mp3_radio_btn.isChecked():
            try:
                self.downloader.audio_download()
                self.downloader.change_audio_meta()
            except (FileOperationError, Exception) as e:
                error_label = QLabel(f"Download failed: {str(e)}\nTry again later")
                error_label.setAlignment(Qt.AlignCenter)
                self.video_box_layout.addWidget(error_label)

    def download_vid(self):
        if self.mp4_radio_btn.isChecked():
            try:
                self.downloader.single_video_download(self.resolution_combo_box.currentText())
                self.downloader.video_meta()
            except (FileOperationError, Exception) as e:
                error_label = QLabel(f"Download failed: {str(e)}\nTry again later")
                error_label.setAlignment(Qt.AlignCenter)
                self.video_box_layout.addWidget(error_label)
        elif self.mp3_radio_btn.isChecked():
            try:
                self.downloader.single_audio_download(self.resolution_combo_box.currentText())
                self.downloader.audio_meta()
            except (FileOperationError, Exception) as e:
                error_label = QLabel(f"Download failed: {str(e)}\nTry again later")
                error_label.setAlignment(Qt.AlignCenter)
                self.video_box_layout.addWidget(error_label)


    def on_format_changed(self):
        if self.mp3_radio_btn.isChecked():
            try:
                self.resolution_combo_box.clear()
                self.resolutions = self.downloader.get_resolutions_audio()
                self.resolution_combo_box.addItems(self.resolutions)
            except Exception as e:
                error_label = QLabel(f"Initializer failed: {str(e)}\nReopen the app")
                error_label.setAlignment(Qt.AlignCenter)
                self.video_box_layout.addWidget(error_label)

        elif self.mp4_radio_btn.isChecked():
            try:
                self.resolution_combo_box.clear()
                self.resolutions = self.downloader.get_resolutions_video()
                self.resolution_combo_box.addItems(self.resolutions)
            except Exception as e:
                error_label = QLabel(f"Initializer failed: {str(e)}\nReopen the app")
                error_label.setAlignment(Qt.AlignCenter)
                self.video_box_layout.addWidget(error_label)

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