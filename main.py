import sys
from urllib.request import urlopen
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, \
    QRadioButton, QButtonGroup, QScrollArea, QFrame, QDialog
from utils.custom_exception import InvalidURLError, DownloadFailedError, MetadataError, NoStreamsError, \
    FileOperationError
from utils.playlist import PlaylistDownloader
from utils.single_downloader import SingleDownloader

# Main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.apply_styles()

# For the styles
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0d0d0d;
            }

            QLabel {
                color: #ffffff;
            }

            QLineEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #333333;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
            }

            QLineEdit:focus {
                border: 2px solid #ffffff;
            }

            QPushButton {
                background-color: #ffffff;
                color: #0d0d0d;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 12px;
                font-family: Arial;
            }

            QPushButton:hover {
                background-color: #e0e0e0;
            }

            QPushButton:pressed {
                background-color: #c0c0c0;
            }

            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }

            QRadioButton {
                color: #ffffff;
                spacing: 5px;
            }

            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }

            QRadioButton::indicator:unchecked {
                background-color: #1a1a1a;
                border: 2px solid #666666;
                border-radius: 9px;
            }

            QRadioButton::indicator:checked {
                background-color: #ffffff;
                border: 2px solid #ffffff;
                border-radius: 9px;
            }

            QComboBox {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #333333;
                border-radius: 8px;
                padding: 8px;
            }

            QComboBox::drop-down {
                border: none;
            }

            QComboBox QAbstractItemView {
                background-color: #1a1a1a;
                color: #ffffff;
                selection-background-color: #333333;
            }

            QScrollArea {
                background-color: #0d0d0d;
                border: 2px solid #333333;
                border-radius: 8px;
            }

            QScrollBar:vertical {
                background-color: #1a1a1a;
                width: 10px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #777777;
            }
        """)

# UI initializing
    def initUI(self):
        self.setWindowTitle("Ebutouy")
        self.setWindowIcon(QIcon('logo.png'))
        self.setFixedSize(600, 600)
        self.center()

    # Layouts
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        self.text_box_layout = QHBoxLayout()
        self.text_box_layout.setSpacing(15)

    # Widgets
        heading = QLabel("Ebutouy")
        heading.setAlignment(Qt.AlignCenter)
        heading.setFont(QFont("Arial", 28, QFont.Bold))

        self.url_box = QLineEdit()
        self.url_box.setPlaceholderText("Enter YouTube URL...")
        self.url_box.setMinimumHeight(45)

        search_btn = QPushButton("Get Video")
        search_btn.setMinimumHeight(45)
        search_btn.setMinimumWidth(120)
        search_btn.clicked.connect(self.search_function)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFixedHeight(300)
        scroll_widget = QWidget()
        self.video_box_layout = QVBoxLayout(scroll_widget)
        self.video_box_layout.setSpacing(15)
        self.video_box_layout.setContentsMargins(15, 15, 15, 15)
        scroll_area.setWidget(scroll_widget)

        self.main_layout.addWidget(heading)
        self.text_box_layout.addWidget(self.url_box)
        self.text_box_layout.addWidget(search_btn)
        self.main_layout.addLayout(self.text_box_layout)
        self.main_layout.addWidget(scroll_area)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

# Method for clearing the screen
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

# For getting the video and the details
    def search_function(self):
        while self.video_box_layout.count():
            item = self.video_box_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
        self.url_text = self.url_box.text()
        self.url_box.clear()

        # For playlists
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
                    vid_title.setFont(QFont("Arial", 10, QFont.Bold))

                    vid_views = QLabel(f"Views: {vid.views}")
                    vid_views.setWordWrap(True)
                    vid_views.setStyleSheet("color: #cccccc;")

                    vid_author = QLabel(f"Channel: {vid.author}")
                    vid_author.setWordWrap(True)
                    vid_author.setStyleSheet("color: #cccccc;")

                    video_description_layout.addWidget(vid_title)
                    video_description_layout.addWidget(vid_views)
                    video_description_layout.addWidget(vid_author)

                    thumbnail_layout = QVBoxLayout()
                    thumbnail_layout.setContentsMargins(0, 0, 0, 0)
                    thumbnail_layout.addWidget(vid_thumbnail)

                    video_item_layout = QHBoxLayout()
                    video_item_layout.setSpacing(15)
                    video_item_layout.setContentsMargins(15, 15, 15, 15)
                    video_item_layout.addLayout(thumbnail_layout)
                    video_item_layout.addLayout(video_description_layout, 1)
                    video_item_layout.addStretch()

                    self.video_box_layout.addLayout(video_item_layout)

                self.format_btn_layout = QVBoxLayout()
                self.format_btn_layout.setContentsMargins(15, 15, 15, 15)
                self.format_btn_layout.setSpacing(10)

                self.mp3_radio_btn = QRadioButton("Mp3")
                self.mp4_radio_btn = QRadioButton("Mp4")
                self.format_btn_group = QButtonGroup()
                self.format_btn_group.addButton(self.mp3_radio_btn)
                self.format_btn_group.addButton(self.mp4_radio_btn)
                self.mp4_radio_btn.setChecked(True)

                self.download_btn = QPushButton("Download")
                self.download_btn.setMinimumHeight(45)
                self.download_btn.clicked.connect(self.download_playlist)

                self.format_btn_layout.addWidget(self.mp4_radio_btn)
                self.format_btn_layout.addWidget(self.mp3_radio_btn)
                self.format_btn_layout.addWidget(self.download_btn)

                self.main_layout.addLayout(self.format_btn_layout)

            except (InvalidURLError, DownloadFailedError, NoStreamsError, MetadataError, FileOperationError) as e:
                error_label = QLabel(str(e))
                error_label.setAlignment(Qt.AlignCenter)
                error_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                self.video_box_layout.addWidget(error_label)

        # For videos and shorts
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
                self.resolution_combo_box.setMinimumHeight(40)
                self.resolutions = self.downloader.get_resolutions_video()
                self.resolution_combo_box.addItems(self.resolutions)
                vid_thumbnail.setPixmap(pixmap)

                vid_title = QLabel(f"Title: {self.downloader.yt.title}")
                vid_title.setWordWrap(True)
                vid_title.setFont(QFont("Arial", 10, QFont.Bold))

                vid_views = QLabel(f"Views: {self.downloader.yt.views}")
                vid_views.setWordWrap(True)
                vid_views.setStyleSheet("color: #cccccc;")

                vid_author = QLabel(f"Channel: {self.downloader.yt.author}")
                vid_author.setWordWrap(True)
                vid_author.setStyleSheet("color: #cccccc;")

                self.mp3_radio_btn = QRadioButton("Mp3")
                self.mp4_radio_btn = QRadioButton("Mp4")
                self.format_btn_group = QButtonGroup()
                self.format_btn_group.addButton(self.mp3_radio_btn)
                self.format_btn_group.addButton(self.mp4_radio_btn)
                self.mp4_radio_btn.setChecked(True)
                self.download_btn = QPushButton("Download")
                self.download_btn.setMinimumHeight(45)
                self.download_btn.clicked.connect(self.download_vid)
                self.mp3_radio_btn.toggled.connect(self.on_format_changed)
                self.mp4_radio_btn.toggled.connect(self.on_format_changed)

                self.video_description_layout.addWidget(vid_title)
                self.video_description_layout.addWidget(vid_views)
                self.video_description_layout.addWidget(vid_author)
                self.video_description_layout.addWidget(self.resolution_combo_box)
                self.format_btn_layout.addWidget(self.mp4_radio_btn)
                self.format_btn_layout.addWidget(self.mp3_radio_btn)

                video_item_layout = QHBoxLayout()
                video_item_layout.setContentsMargins(15, 15, 15, 15)
                video_item_layout.setSpacing(15)
                video_item_layout.addWidget(vid_thumbnail)
                video_item_layout.addLayout(self.video_description_layout)
                video_item_layout.addLayout(self.format_btn_layout)
                video_item_layout.addWidget(self.download_btn)

                self.video_box_layout.addLayout(video_item_layout)
            except (InvalidURLError, DownloadFailedError, NoStreamsError, MetadataError, FileOperationError) as e:
                error_label = QLabel(str(e))
                error_label.setAlignment(Qt.AlignCenter)
                error_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                self.video_box_layout.addWidget(error_label)

        # Error Handling
        else:
            error_label = QLabel("Not Valid URL")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
            self.video_box_layout.addWidget(error_label)

# For downloading playlist as mp3 or mp4
    def download_playlist(self):
        if self.mp4_radio_btn.isChecked():
            try:
                self.downloader.video_download()
                self.downloader.change_video_meta()
                self.show_popup()
            except (FileOperationError, Exception) as e:
                error_label = QLabel(f"Download failed: {str(e)}\nTry again later")
                error_label.setAlignment(Qt.AlignCenter)
                error_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                self.video_box_layout.addWidget(error_label)
        elif self.mp3_radio_btn.isChecked():
            try:
                self.downloader.audio_download()
                self.downloader.change_audio_meta()
                self.show_popup()
            except (FileOperationError, Exception) as e:
                error_label = QLabel(f"Download failed: {str(e)}\nTry again later")
                error_label.setAlignment(Qt.AlignCenter)
                error_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                self.video_box_layout.addWidget(error_label)

# For downloading videos as mp3 or mp4
    def download_vid(self):
        if self.mp4_radio_btn.isChecked():
            try:
                self.downloader.single_video_download(self.resolution_combo_box.currentText())
                self.downloader.video_meta()
                self.show_popup()
            except (FileOperationError, Exception) as e:
                error_label = QLabel(f"Download failed: {str(e)}\nTry again later")
                error_label.setAlignment(Qt.AlignCenter)
                error_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                self.video_box_layout.addWidget(error_label)
        elif self.mp3_radio_btn.isChecked():
            try:
                self.downloader.single_audio_download(self.resolution_combo_box.currentText())
                self.downloader.audio_meta()
                self.show_popup()
            except (FileOperationError, Exception) as e:
                error_label = QLabel(f"Download failed: {str(e)}\nTry again later")
                error_label.setAlignment(Qt.AlignCenter)
                error_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                self.video_box_layout.addWidget(error_label)

# Download complete confirmation
    def show_popup(self):
        self.popup_label = QLabel("✓ Download Complete")
        self.popup_label.setAlignment(Qt.AlignCenter)
        self.popup_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.popup_label.setStyleSheet("""
            background-color: #1a1a1a;
            color: #ffffff;
            border: 2px solid #ffffff;
            border-radius: 15px;
            padding: 20px;
        """)
        self.video_box_layout.addWidget(self.popup_label)
        QTimer.singleShot(3000, self.remove_popup)

# For removing the confirmation after 3 seconds
    def remove_popup(self):
        if hasattr(self, 'popup_label'):
            self.video_box_layout.removeWidget(self.popup_label)
            self.popup_label.deleteLater()

# Checking if user changed the format
    def on_format_changed(self):
        if self.mp3_radio_btn.isChecked():
            try:
                self.resolution_combo_box.clear()
                self.resolutions = self.downloader.get_resolutions_audio()
                self.resolution_combo_box.addItems(self.resolutions)
            except Exception as e:
                error_label = QLabel(f"Initializer failed: {str(e)}\nReopen the app")
                error_label.setAlignment(Qt.AlignCenter)
                error_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                self.video_box_layout.addWidget(error_label)

        elif self.mp4_radio_btn.isChecked():
            try:
                self.resolution_combo_box.clear()
                self.resolutions = self.downloader.get_resolutions_video()
                self.resolution_combo_box.addItems(self.resolutions)
            except Exception as e:
                error_label = QLabel(f"Initializer failed: {str(e)}\nReopen the app")
                error_label.setAlignment(Qt.AlignCenter)
                error_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                self.video_box_layout.addWidget(error_label)

# For centering the window
    def center(self) -> None:
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)



app = QApplication([])
win = MainWindow()
win.show()
sys.exit(app.exec_())
