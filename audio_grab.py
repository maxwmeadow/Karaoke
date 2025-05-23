from spotdl import Spotdl
import subprocess
import os

def grab_set_up():
    old_dir = "ffmpeg-2025-05-21-git-4099d53759-essentials_build.7z"
    extraction = "ffmpeg-2025-05-21-git-4099d53759-essentials_build"
    bin = os.path.join(extraction, "bin")

    if not os.path.exists(os.path.join(bin, "ffmpeg.exe")):
        subprocess.run(["7zr.exe", "x", old_dir])

    os.environ["PATH"] = os.path.abspath(bin) +  os.pathsep + os.environ["PATH"]

    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)

    except Exception as e:
        print("Failed getting ffmpeg: " + e)

def get_mp3(track_url: str, title: str, artist: str):
    print("in function")
    client = Spotdl()
    print("crash here")
    result = client.search([track_url, title, artist])
    print("search crash")
    print(result)