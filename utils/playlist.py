import sys
from pathlib import Path
from typing import Optional
from pytubefix import Playlist
from single_downloader import SingleDownloader
from custom_exception import FileOperationError, InvalidURLError, MetadataError


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
        try:
            for video in self.playlist.videos:
                ys = video.streams.get_highest_resolution(progressive=True)
                ys.download(output_path=self.path)
        except Exception as e:
            raise FileOperationError(f"Video download failed: {str(e)}")

    def audio_download(self):
        try:
            for audio in self.playlist.videos:
                ys = audio.streams.get_audio_only()
                ys.download(output_path=self.path)
        except Exception as e:
            raise FileOperationError(f"Audio download failed: {str(e)}")

    def change_audio_meta(self):
        try:
            for link in self.playlist.video_urls:
                SingleDownloader(link, self.path).audio_meta()
        except Exception as e:
            raise MetadataError(f"Failed to change audio metadata: {str(e)}")

    def change_video_meta(self):
        try:
            for link in self.playlist.video_urls:
                SingleDownloader(link, self.path).video_meta()
        except Exception as e:
            raise MetadataError(f"Failed to change video metadata: {str(e)}")

def main():
    try:
        downloader: PlaylistDownloader = PlaylistDownloader("https://www.youtube.com/playlist?list=PLQWraVTLRsSl9xzha46s9K-LEbIG8UlNo")

        usr_choice: int = 0
        try:
            usr_choice = int(input("Download audio (1)\nDownload Video (2)\nAdd audio metadata (3)\nAdd video metadata (4)\nExit (5)\nChoice: "))
        except ValueError:
            print("Choose the correct option (1, 2, 3, 4, or 5)")
            return

        if usr_choice == 1:
            downloader.audio_download()
            print("Audio downloaded successfully")

        elif usr_choice == 2:
            downloader.video_download()
            print("Video downloaded successfully")

        elif usr_choice == 3:
            downloader.change_audio_meta()
            print("Audio metadata added successfully")

        elif usr_choice == 4:
            downloader.change_video_meta()
            print("Video metadata added successfully")

        elif usr_choice == 5:
            sys.exit("Bye...")
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5")

    except (InvalidURLError, FileOperationError, MetadataError) as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()