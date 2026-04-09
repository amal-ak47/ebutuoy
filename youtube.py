import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, List
from pytubefix import YouTube
from mutagen.mp4 import MP4, MP4Cover
import urllib.request
import re
from custom_exception import FileOperationError, InvalidURLError, NoStreamsError, DownloadFailedError, MetadataError

# Class for downloading single video as mp3 or mp4 in available
class SingleDownloader:
    def __init__(self, link: str, path: str = str(Path.home() / "Downloads")):
        self.link = str(link).strip()
        self.path = path
        self.yt: Optional[YouTube] = None
        self.channel: Optional[str] = None
        self.thumbnail: Optional[str] = None

        try:
            Path(self.path).mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError):
            raise FileOperationError(f"Cannot access directory '{self.path}'")

        self._initialize_youtube()

    # Initialize YouTube object
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
            stream = self.yt.streams.filter(progressive=True, res=resolution, file_extension='mp4').first()
            if not stream:
                raise NoStreamsError(f"No stream available for {resolution}")
            stream.download(output_path=self.path)
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
            streams = self.yt.streams.filter(progressive=True, file_extension='mp4')
            resolutions = [x.resolution for x in streams if x.resolution]
            return sorted(set(resolutions), reverse=True) or None
        except Exception:
            return None

    # getting abr of audio as a list
    def get_resolutions_audio(self) -> Optional[List[str]]:
        if not self.yt:
            return None
        try:
            streams = self.yt.streams.filter(only_audio=True)
            audio_bitrates = [s.abr for s in streams if s.abr and s.abr not in ('160kbps', '50kbps')]
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
            stream = self.yt.streams.filter(only_audio=True, abr=bitrate).first()
            if not stream:
                return False
            stream.download(output_path=self.path)
            return True
        except Exception as e:
            raise DownloadFailedError(str(e))

    # changing meta tags of the audio file
    def audio_meta(self) -> None:
        if not self.yt:
            raise InvalidURLError("YouTube object not initialized")
        try:
            m4a_path = f"{self.path}/{self.yt.title}.m4a"
            try:
                MP4(m4a_path)
            except FileNotFoundError:
                safe_title = re.sub(r'[/\\:<>"|?*]', '', self.yt.title)
                m4a_path = f"{self.path}/{safe_title}.m4a"
                MP4(m4a_path)

            try:
                if self.thumbnail and self.channel:
                    thumb_path = f"{self.path}/temp_thumb.jpg"
                    temp_output = f"{self.path}/.temp_audio.mp3"
                    mp3_path = m4a_path.replace(".m4a", ".mp3")
                    urllib.request.urlretrieve(self.thumbnail, thumb_path)
                    command = [
                        "ffmpeg",
                        "-y",
                        "-i", m4a_path,
                        "-i", thumb_path,
                        "-map", "0:a",
                        "-map", "1:v",
                        "-c:a", "libmp3lame",
                        "-q:a", "4",
                        "-c:v", "copy",
                        "-metadata", f"artist={self.channel}",
                        "-metadata:s:v", "title=Album cover",
                        "-metadata:s:v", "comment=Cover (front)",
                        "-id3v2_version", "3",
                        temp_output
                    ]
                    subprocess.run(command)
                    os.remove(thumb_path)
                    os.replace(temp_output, mp3_path)
                    os.remove(m4a_path)

            except Exception:
                pass

        except FileNotFoundError:
            raise MetadataError("Audio file not found")
        except Exception as e:
            raise MetadataError(str(e))

    # changing meta tags of the video file
    def video_meta(self) -> None:
        if not self.yt:
            raise InvalidURLError("YouTube object not initialized")
        try:
            mp4_path = f"{self.path}/{self.yt.title}.mp4"
            try:
                MP4(mp4_path)
            except FileNotFoundError:
                safe_title = re.sub(r'[/\\:<>"|?*]', '', self.yt.title)
                mp4_path = f"{self.path}/{safe_title}.mp4"
                MP4(mp4_path)
            try:
                if self.thumbnail and self.yt.title and self.channel:
                    thumb_path = f"{self.path}/temp_thumb.jpg"
                    temp_output = f"{self.path}/.temp_video.mp4"
                    urllib.request.urlretrieve(self.thumbnail, thumb_path)
                    command = [
                        "ffmpeg",
                        "-y",
                        "-i", mp4_path,
                        "-i", thumb_path,
                        "-metadata", f"artist={self.channel}",
                        "-map", "0",
                        "-map", "1",
                        "-c", "copy",
                        "-disposition:v:1", "attached_pic",
                        temp_output
                    ]
                    subprocess.run(command)
                    os.remove(thumb_path)
                    os.replace(temp_output, mp4_path)
            except Exception:
                pass
        except FileNotFoundError:
            raise MetadataError("Audio file not found")
        except Exception as e:
            raise MetadataError(str(e))

# main function just for testing
def main():
    try:
        downloader = SingleDownloader("https://www.youtube.com/watch?v=NE6FcGcnvcA")

        usr_choice = ""
        try:
            usr_choice = int(input("Download audio (1)\nDownload Video(2)\nExit (3)\nChoice: "))
        except ValueError:
            print("Choose the correct option (1 or 2)")

        if usr_choice == 1:
            audio_options = downloader.get_resolutions_audio()

            if audio_options:
                print("Available abr:", audio_options)
            bitrate_input = input("Enter abr (or leave empty to skip): ").strip()

            if bitrate_input:
                if downloader.single_audio_download(bitrate_input):
                    downloader.audio_meta()
                    print("Audio downloaded successfully")
                else:
                    print("Failed to download audio")
            else:
                print("Audio download skipped")

        elif usr_choice == 2:
            video_options = downloader.get_resolutions_video()
            if video_options:
                print("Available video resolutions:", video_options)
            resolution_input = input("Enter resolution (or leave empty to skip): ").strip()

            if resolution_input:
                if downloader.video_download(resolution_input):
                    downloader.video_meta()
                    print("Video downloaded successfully")
                else:
                    print("Failed to download Video")
            else:
                print("Video download skipped")
        elif usr_choice == 3:
            sys.exit("Bye...")

    except (InvalidURLError, DownloadFailedError, NoStreamsError, MetadataError, FileOperationError) as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()