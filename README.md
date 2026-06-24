# Kirinuki Script: YouTube Clip Downloader

A lightweight, hybrid CLI/GUI Python script designed to batch-download specific timestamped segments from YouTube videos using `yt-dlp`. Works cross-platform across all major operating systems, supporting macOS, Windows, and Linux.

Perfect for editors, clippers, and archivists who need to extract multiple specific moments from a long VOD or stream without downloading the entire video, or saves you having to manually input commands for each clip.

## Features
* **Time-saving:** Only downloads the exact sections you need using `yt-dlp`'s `--download-sections` argument.
* **Hybrid Interface:** Uses a terminal prompt for the URL, but native OS pop-up windows (via `tkinter`) for selecting your timestamps file and output folder.
* **Automatic File Naming:** Automatically numbers your clips sequentially (`1.mp4`, `2.mp4`, etc.) in the destination folder.
* **PO Token Support:** Built-in configuration for YouTube PO Tokens to bypass modern bot-detection blocks.

## 🛠 Prerequisites

1. **Python 3.6+**: Ensure Python is installed on your system.
2. **yt-dlp**: You must have the `yt-dlp` executable. 
   * Download the latest release from the [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp/releases).
   * **Important:** This script expects the `yt-dlp` executable (`yt-dlp.exe` on Windows, `yt-dlp` on Mac/Linux) to be located *inside* the folder where you want your clips to be saved. Just drag it inside the folder.

## Usage

### 1. Prepare your Timestamps File
Create a simple `.txt` file containing the start and end times in seconds, separated by a hyphen `-` or equals sign `=` (possible typo I personally make a lot). Supports having text comments describing each timestamp above.

**Example `timestamps.txt`:**
```text
funny moment:
30-45

include context
120-150

ending segment:
3600-3660

```
(This will download a clip named `1.mp4` from 0:30-0:45, a clip named `2.mp4` from 2:00-2:30, and a clip named `3.mp4` from 1:00:00-1:01:00).

### 2. Configure PO Token (Optional but Recommended)
To prevent YouTube from blocking your downloads, you may need a PO Token. Open `kirinukiscript.py` in a text editor and update the `PO_TOKEN` variable at the top of the file.

```python
PO_TOKEN = "your_token_here"
```

### 3. Run the script from your terminal:

```bash
python kirinukiscript.py
```

### 4. Follow the Prompts
* **Terminal:** Paste the YouTube URL when prompted.
* **GUI Pop-up 1:** Select your `timestamps.txt` file.
* **GUI Pop-up 2:** Select the output folder (Remember: The executable `yt-dlp` must be inside this folder!).

The script will handle the rest, leaving you with neatly numbered `.mp4` clips in your destination folder.
