import re
import subprocess
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import Tuple, Optional, List

# --- CONFIGURATION ---
# Replace this with your actual PO Token, or leave blank if not required.
PO_TOKEN = "mweb.gvs+XXX" 

def get_user_paths() -> Tuple[Optional[Path], Optional[Path]]:
    """Opens GUI dialogs to let the user select the input file and output folder."""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True) 

    print("Opening file dialog... Please select your timestamps text file.")
    txt_file_path = filedialog.askopenfilename(
        title="1/2: Select Timestamps Text File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if not txt_file_path:
        print("No text file selected. Cancellation detected. Exiting...")
        return None, None

    print(f"Selected file: {txt_file_path}")
    print("\nOpening folder dialog... Please select your output destination.")
    
    output_folder = filedialog.askdirectory(
        title="2/2: Select Output Destination Folder"
    )
    
    if not output_folder:
        print("No output folder selected. Cancellation detected. Exiting...")
        return None, None

    print(f"Selected destination: {output_folder}\n")
    return Path(txt_file_path), Path(output_folder)

def download_clips(txt_file_path: Path, output_folder: Path, video_url: str, po_token: str) -> None:
    """Parses timestamps and runs the local yt-dlp executable to download clips."""
    
    # 1. Determine the exact path to the local yt-dlp executable
    import os
    exe_name = "yt-dlp.exe" if os.name == "nt" else "yt-dlp"
    yt_dlp_path = output_folder / exe_name
    
    # 2. Verify that yt-dlp is actually in the chosen folder
    if not yt_dlp_path.exists():
        print(f"Error: Could not find '{exe_name}' inside the selected folder.")
        print(f"Please make sure it is placed exactly in: {output_folder}")
        return

    # 3. Parse the timestamps
    timestamps: List[Tuple[str, str]] = []
    pattern = re.compile(r"(\d+)[-=](\d+)") 
    
    try:
        with open(txt_file_path, "r", encoding="utf-8") as file:
            for line in file:
                match = pattern.search(line)
                if match:
                    start, end = match.groups()
                    timestamps.append((start, end))
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    if not timestamps:
        print("No valid timestamps found in the selected file.")
        return

    print(f"Found {len(timestamps)} timestamp ranges. Starting download...")

    # 4. Iterate through timestamps and download each section
    for index, (start, end) in enumerate(timestamps, start=1):
        print(f"\n--- Downloading clip {index}: {start} to {end} ---")
        
        # Construct the command using the LOCAL yt-dlp path
        command = [
            str(yt_dlp_path), 
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "-o", f"{index}.%(ext)s", 
            "--download-sections", f"*{start}-{end}",
        ]

        # Conditionally add the PO Token if it exists
        if po_token and po_token != "mweb.gvs+XXX":
            command.extend(["--extractor-args", f"youtube:po_token={po_token}"])
        
        command.append(video_url)
        
        # Run the command with cwd set to the target folder
        try:
            subprocess.run(command, cwd=output_folder, check=True)
            print(f"Successfully downloaded clip {index}.mp4")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading clip {index}: {e}")

if __name__ == "__main__":
    print("=== YouTube Clip Downloader (Local Execution) ===")
    
    # Ask for URL via the terminal
    VIDEO_URL = input("Paste the YouTube Video URL: ").strip()
    
    if not VIDEO_URL:
        print("URL is required. Exiting...")
    else:
        # Trigger the pop-ups for file and folder selection
        file_path, out_folder = get_user_paths()
        
        if file_path and out_folder:
            download_clips(file_path, out_folder, VIDEO_URL, PO_TOKEN)
            print("\n=== All tasks finished! ===")