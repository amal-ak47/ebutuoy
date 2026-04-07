import time
from pathlib import Path

from pydub import AudioSegment
from pytubefix import YouTube
from pytubefix import Playlist
import os
from mutagen.mp4 import MP4, MP4Cover
import urllib.request
import re

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
        if self.yt:
            self.streams = self.yt.streams.filter(progressive=True, res=resolution, file_extension='mp4').first()

            if self.streams  is None:
                return False
            self.streams .download(output_path=self.path)
            return True
        return None

    def get_resolutions_video(self):
        if self.yt:
            self.streams = self.yt.streams.filter(progressive=True, file_extension='mp4')
            res = [x.resolution for x in self.streams if x.resolution]
            return sorted(set(res), reverse=True)
        return None

    def get_resolutions_audio(self):
        if self.yt:
            self.streams = self.yt.streams.filter(only_audio=True)
            res = [stream.abr for stream in self.streams if stream.abr is not None and stream.abr != '160kbps' and stream.abr != '50kbps']
            return sorted(set(res), reverse=True)
        return None

    def single_audio_download(self, res):
        if self.yt:
            self.streams  = self.yt.streams.filter(only_audio=True, abr=res).first()
            if self.streams is None:
                return False
            self.streams.download(output_path=self.path)
            return True
        return None

    def meta(self):
        try:
            m4a_path = f"{self.path}/{self.yt.title}.m4a"
            audio = MP4(m4a_path)

        except Exception:
            safe_title = re.sub(r'[/\\:<>"|?*]', '', self.yt.title)
            m4a_path = f"{self.path}/{safe_title}.m4a"
            audio = MP4(m4a_path)

        thumb_data = urllib.request.urlopen(self.thumbnail).read()
        audio["covr"] = [MP4Cover(thumb_data, imageformat=MP4Cover.FORMAT_JPEG)]
        audio["\xa9nam"] = [self.yt.title]
        audio["\xa9ART"] = [self.channel]
        audio.save()
    def playlist_download(self):
        ...


def main():
    downloader = EbutouyDownloader("https://www.youtube.com/watch?v=NE6FcGcnvcA")
    print(downloader.get_resolutions_audio())
    print(downloader.get_resolutions_video())

    res = input("Enter resolution: ")
    downloader.single_audio_download(res)
    downloader.meta()


if __name__ == "__main__":
    main()