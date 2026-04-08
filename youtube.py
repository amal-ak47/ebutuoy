import collections
from pathlib import Path
from typing import Union

from pytubefix import YouTube, Stream
from mutagen.mp4 import MP4, MP4Cover
import urllib.request
import re

# Class for downloading single video as mp3 or mp4 in available resolutions or abr
class SingleDownloader:
    def __init__(self, link: str, path: str = str(Path.home() / "Downloads")):
        self.link: str = str(link)
        self.path: str = path
        self.streams: collections.Iterable = []
        self.stream: Union[Stream, None] = None
        self.yt: YouTube = YouTube(self.link)
        self.channel: str = self.yt.author
        self.thumbnail: str = self.yt.thumbnail_url

    # video downloading using desired resolution as mp4 format
    def video_download(self, resolution: str) -> bool:
        self.stream = self.yt.streams.filter(progressive=True, res=resolution, file_extension='mp4').first()

        if self.stream  is None:
            return False

        self.stream.download(output_path=self.path)
        return True

    # getting resolution for video as a list
    def get_resolutions_video(self):
        if self.yt:
            self.streams = self.yt.streams.filter(progressive=True, file_extension='mp4')
            res: list = [x.resolution for x in self.streams if x.resolution]
            return sorted(set(res), reverse=True)
        return None

    # getting abr of audio as a list
    def get_resolutions_audio(self) -> Union[list, bool]:
        if self.yt:
            self.streams = self.yt.streams.filter(only_audio=True)
            abrr: list = [stream.abr for stream in self.streams if stream.abr is not None and stream.abr != '160kbps' and stream.abr != '50kbps']
            return sorted(set(abrr), reverse=True)
        return False

    # audio downloading using desired abr
    def single_audio_download(self, abrr: str) -> bool:
        if self.yt:
            self.stream  = self.yt.streams.filter(only_audio=True, abr=abrr).first()
            if self.stream is None:
                return False
            self.stream.download(output_path=self.path)
            return True
        return False

    # changing meta tags of the audio file
    def meta(self) -> None:
        try:
            m4a_path: str = f"{self.path}/{self.yt.title}.m4a"
            audio: MP4 = MP4(m4a_path)
        except Exception:
            safe_title: str = re.sub(r'[/\\:<>"|?*]', '', self.yt.title)
            m4a_path = f"{self.path}/{safe_title}.m4a"
            audio = MP4(m4a_path)

        thumb_data: bytes = urllib.request.urlopen(self.thumbnail).read()
        audio["covr"]: MP4Cover = [MP4Cover(thumb_data, imageformat=MP4Cover.FORMAT_JPEG)]
        audio["\xa9nam"]: MP4.MP4Tags = [self.yt.title]
        audio["\xa9ART"]: MP4.MP4Tags = [self.channel]
        audio.save()


# main function just for testing
def main():
    downloader = SingleDownloader("https://www.youtube.com/watch?v=NE6FcGcnvcA")
    print(downloader.get_resolutions_audio())
    print(downloader.get_resolutions_video())

    res = input("Enter resolution: ")
    downloader.single_audio_download(res)
    downloader.meta()

if __name__ == "__main__":
    main()