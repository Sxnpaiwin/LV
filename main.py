import subprocess
import time
import requests

# Dropbox direct link
dropbox_url = "https://www.dropbox.com/scl/fi/lz1khkvahf5rcp5obbnn6/Ip-is-1-1.mp4?rlkey=jlxf0s2v97ngj2y6oxamvnlpy&st=303dvugp&raw=1"
video_file = "video.mp4"

# Download video
def download_video():
    print("Downloading video from Dropbox...")
    response = requests.get(dropbox_url)
    if response.status_code == 200:
        with open(video_file, "wb") as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print(f"Failed to download video. Status code: {response.status_code}")

# FFmpeg Command
ffmpeg_command = [
    'ffmpeg',
    '-stream_loop', '-1',
    '-re',
    '-i', video_file,
    '-vcodec', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'superfast',
    '-r', '30',
    '-b:v', '3000k',
    '-f', 'flv',
    "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"
]

# Start Streaming
if __name__ == "__main__":
    download_video()  # Fetch video before streaming
    while True:
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10)
