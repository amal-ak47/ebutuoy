from pytubefix import YouTube
from pytubefix import Playlist


class EbutouyDownloader():
    def __init__(self, link: str, path: str):
        self.link = str(link)
        self.channel = None
        self.thumbnail = None
        self.head = None
        self.path = path

        self.streams = None

        if "playlist" in self.link:
            self.plst = Playlist(self.link)
            self.yt = None
        else:
            self.yt = YouTube(self.link)
            self.plst = None


    def video_download(self, resolution):
        self.head = self.yt.title
        self.channel = self.yt.author
        self.thumbnail = self.yt.thumbnail_url




    def get_resolutions_video(self):
        if self.yt:
            self.streams = self.yt.streams.filter(file_extension='mp4')
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
    downloader = EbutouyDownloader("https://www.youtube.com/watch?v=MPTBT4-r4Fs", "/path")
    print(downloader.get_resolutions_audio())
    print(downloader.get_resolutions_video())

if __name__ == "__main__":
    main()