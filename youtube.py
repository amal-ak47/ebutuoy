from pathlib import Path

from pytubefix import YouTube
from pytubefix import Playlist
import os

class EbutouyDownloader():
    def __init__(self, link: str, path: str = str(Path.home() / "Downloads")):
        self.link = str(link)
        self.path = path

        self.channel = None
        self.thumbnail = None
        self.head = None
        self.streams = None

        if "playlist" in self.link:
            self.plst = Playlist(self.link)
            self.yt = None

        else:
            self.yt = YouTube(self.link)
            self.plst = None
            self.head = self.yt.title
            self.channel = self.yt.author
            self.thumbnail = self.yt.thumbnail_url


    def video_download(self, resolution):
        stream = self.yt.streams.filter(progressive=True, res=resolution, file_extension='mp4').first()

        if stream is None:
            return False
        stream.download(output_path=self.path)
        return True


    def get_resolutions_video(self):
        if self.yt:
            self.streams = self.yt.streams.filter(progressive=True, file_extension='mp4')
            res = [x.resolution for x in self.streams if x.resolution]
            return sorted(set(res), reverse=True)
        return None

    def get_resolutions_audio(self):
        if self.yt:
            self.streams = self.yt.streams.filter(only_audio=True)
            res = [stream.abr for stream in self.streams if stream.abr is not None]
            return sorted(set(res), reverse=True)
        return None

    def audio_download(self):
        ...

    def playlist_download(self):
        ...


def main():
    downloader = EbutouyDownloader("https://www.youtube.com/watch?v=MPTBT4-r4Fs")
    print(downloader.get_resolutions_audio())
    print(downloader.get_resolutions_video())

    res = input("Enter resolution: ")
    downloader.video_download(res)


if __name__ == "__main__":
    main()