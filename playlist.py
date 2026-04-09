from pathlib import Path
from typing import Optional
from pytubefix import Playlist
from single_downloader import SingleDownloader
from custom_exception import FileOperationError, InvalidURLError


class PlaylistDownloader():
    def __init__(self, link: str, path: str = str(Path.home() / "Downloads")):
        self.link: str = link
        self.path: str = path
        self.playlist: Optional[Playlist] = None

        try:
            Path(self.path).mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError):
            raise FileOperationError(f"Cannot access directory '{self.path}'")

        self._playlist_initializer()

    def _playlist_initializer(self):
        if not self.link:
            raise InvalidURLError("YouTube link cannot be empty")
        try:
            self.playlist = Playlist(self.link)
        except Exception as e:
            raise InvalidURLError(f"Failed to load video: {str(e)}")

    def video_download(self):
        for video in self.playlist.videos:
            ys = video.streams.get_highest_resolution(progressive=True)
            ys.download(output_path=self.path)

    def audio_download(self):
        for audio in self.playlist.videos:
            ys = audio.streams.get_audio_only()
            ys.download(output_path=self.path)

    def change_audio_meta(self):
        for link in self.playlist.video_urls:
            SingleDownloader(link, self.path).audio_meta()

    def change_video_meta(self):
        for link in self.playlist.video_urls:
            SingleDownloader(link, self.path).video_meta()



if __name__ == "__main__":
    downloader = PlaylistDownloader("https://www.youtube.com/playlist?list=PLQWraVTLRsSl9xzha46s9K-LEbIG8UlNo")
    downloader.video_download()
    downloader.change_video_meta()
    print("Done")