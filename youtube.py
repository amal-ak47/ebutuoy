import collections
import logging
from pathlib import Path
from typing import Union, Optional, List
from pytubefix import YouTube, Stream
from mutagen.mp4 import MP4, MP4Cover
import urllib.request
import re
from custom_exception import FileOperationError, InvalidURLError, NoStreamsError, DownloadFailedError, MetadataError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Class for downloading single video as mp3 or mp4 in available
class SingleDownloader:
    def __init__(self, link: str, path: str = str(Path.home() / "Downloads")):
        self.link: str = str(link).strip()
        self.path: str = path
        self.streams: collections.Iterable = []
        self.stream: Union[Stream, None] = None
        self.yt: Optional[YouTube] = None
        self.channel: Optional[str] = None
        self.thumbnail: Optional[str] = None

        try:
            download_path = Path(self.path)
            download_path.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            raise FileOperationError(f"Cannot access directory '{self.path}'")

        self._initialize_youtube()

    def _initialize_youtube(self) -> None:
        if not self.link:
            raise InvalidURLError("YouTube link cannot be empty")
        try:
            self.yt = YouTube(self.link)
            _ = self.yt.title
            self.channel = self.yt.author
            self.thumbnail = self.yt.thumbnail_url
        except Exception as e:
            raise InvalidURLError(f"Failed to load video: {str(e)}")

    # video downloading using desired resolution as mp4 format
    def video_download(self, resolution: str) -> bool:
        if not self.yt:
            raise InvalidURLError("YouTube object not initialized")
        try:
            self.stream = self.yt.streams.filter(progressive=True,res=resolution,file_extension='mp4').first()
            if self.stream is None:
                raise NoStreamsError(f"No stream available for {resolution}")
            self.stream.download(output_path=self.path)
            return True
        except NoStreamsError:
            raise
        except Exception as e:
            raise DownloadFailedError(str(e))

    # getting resolution for video as a list
    def get_resolutions_video(self) -> Optional[List[str]]:
        if not self.yt:
            return None
        try:
            self.streams = self.yt.streams.filter(progressive=True, file_extension='mp4')
            resolutions: list = [x.resolution for x in self.streams if x.resolution]
            return sorted(set(resolutions), reverse=True) or None
        except Exception:
            return None

    # getting abr of audio as a list
    def get_resolutions_audio(self) -> Optional[List[str]]:
        if not self.yt:
            return None
        try:
            self.streams = self.yt.streams.filter(only_audio=True)
            audio_bitrates = [
                stream.abr for stream in self.streams
                if stream.abr and stream.abr not in ('160kbps', '50kbps')
            ]
            return sorted(set(audio_bitrates), reverse=True) or None
        except Exception:
            return None

    # audio downloading using desired abr
    def single_audio_download(self, bitrate: str) -> bool:
        if not self.yt:
            raise InvalidURLError("YouTube object not initialized")
        if not bitrate:
            return False
        try:
            self.stream = self.yt.streams.filter(only_audio=True, abr=bitrate).first()
            if self.stream is None:
                return False
            self.stream.download(output_path=self.path)
            return True
        except Exception as e:
            raise DownloadFailedError(str(e))

    # changing meta tags of the audio file
    def meta(self) -> None:
        if not self.yt:
            raise InvalidURLError("YouTube object not initialized")
        try:
            m4a_path: str = f"{self.path}/{self.yt.title}.m4a"

            try:
                audio: MP4 = MP4(m4a_path)
            except FileNotFoundError:
                safe_title: str = re.sub(r'[/\\:<>"|?*]', '', self.yt.title)
                m4a_path = f"{self.path}/{safe_title}.m4a"
                audio = MP4(m4a_path)
            try:
                if self.thumbnail:
                    thumb_data: bytes = urllib.request.urlopen(self.thumbnail, timeout=10).read()
                    audio["covr"] = [MP4Cover(thumb_data, imageformat=MP4Cover.FORMAT_JPEG)]
            except Exception:
                pass
            if self.yt.title:
                audio["\xa9nam"] = [self.yt.title]
            if self.channel:
                audio["\xa9ART"] = [self.channel]

            audio.save()
        except FileNotFoundError:
            raise MetadataError("Audio file not found")
        except Exception as e:
            raise MetadataError(str(e))

# main function just for testing
def main():
    try:
        downloader = SingleDownloader("https://www.youtube.com/watch?v=NE6FcGcnvcA")

        audio_options = downloader.get_resolutions_audio()
        video_options = downloader.get_resolutions_video()

        if audio_options:
            print("Available abr:", audio_options)
        if video_options:
            print("Available video resolutions:", video_options)

        bitrate_input = input("Enter abr (or leave empty to skip): ").strip()

        if bitrate_input:
            if downloader.single_audio_download(bitrate_input):
                downloader.meta()
                print("Audio downloaded successfully")
            else:
                print("Failed to download audio")
        else:
            print("Audio download skipped")

    except InvalidURLError as e:
        print(e)
    except DownloadFailedError as e:
        print(e)
    except NoStreamsError as e:
        print(e)
    except MetadataError as e:
        print(e)
    except FileOperationError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()