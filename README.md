# Ebutouy - YouTube Downloader

Download YouTube videos and playlists as MP3 or MP4 with ease.

## Features
- Download single videos/shorts as MP3 or MP4
- Download entire playlists
- Choose video resolution and audio bitrate
- Automatic metadata tagging (title, artist, thumbnail)
- Black and white modern UI
- Cross-platform (Windows, macOS, Linux)

## System Requirements
- Windows 10+ / macOS 10.14+ / Linux (Ubuntu/Fedora/Arch)
- Internet connection
- 100MB free disk space

## Installation & Usage

### Windows

1. Download `Ebutouy.exe` from [mediafire](https://www.mediafire.com/file/wkgebczqwxwa1qz/Ebutouy.exe/file)
2. Run the executable
3. No installation needed - FFmpeg is bundled

### macOS

1. Download `Ebutouy.app.zip` from the [latest release](../../releases/latest)
2. Unzip the file
3. Drag `Ebutouy.app` to your Applications folder
4. Run from Applications
5. FFmpeg is bundled - no installation needed

### Linux

1. Install dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt5 ffmpeg python3-pip

# Fedora
sudo dnf install python3-pyqt5 ffmpeg python3-pip

# Arch
sudo pacman -S python-pyqt5 ffmpeg
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/ebutouy.git
cd ebutouy
```

3. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install PyQt5 pytubefix mutagen unidecode
```

5. Run the app:
```bash
python3 main.py
```

## How to Use

1. Paste a YouTube URL (video, short, or playlist)
2. Click "Get Video"
3. Select MP3 or MP4 format
4. Choose quality/resolution (for videos) or bitrate (for audio)
5. Click "Download"
6. Files are saved to your Downloads folder

## Troubleshooting

### "FFmpeg not found" error
- **Windows/Mac**: FFmpeg is bundled. This shouldn't happen. Reinstall the app.
- **Linux**: Install FFmpeg: `sudo apt-get install ffmpeg` (Ubuntu) or `sudo dnf install ffmpeg` (Fedora)

### Downloads not working
- Check your internet connection
- Make sure the YouTube URL is valid
- Try a different video

### Permission denied on Linux
```bash
chmod +x Ebutouy
```

## Project Structure

```ebutouy/
├── main.py                 # Main application
├── utils/
│   ├── single_downloader.py
│   ├── playlist.py
│   └── custom_exception.py
├── icons/
│   ├── logo.ico
│   └── logo.icns
└── README.md
```

## Development

### Setup development environment:
```bash
git clone https://github.com/yourusername/ebutouy.git
cd ebutouy
python3 -m venv venv
source venv/bin/activate
pip install PyQt5 pytubefix mutagen unidecode pyinstaller
```

### Build for distribution:
```bash
pyinstaller main.spec
```

## License
MIT License - See LICENSE file for details

## Support
For issues, questions, or suggestions, please open a [GitHub issue](../../issues)

## Credits
- Built with PyQt5
- Uses pytubefix for YouTube downloads
- FFmpeg for audio/video processing
