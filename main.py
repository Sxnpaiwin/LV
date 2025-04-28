import subprocess
import time
import sys

# --- Configuration ---
# Replace with the actual path to your video file
video_file = "/workspaces/LV/Minecraft CRACKED SMP LIVE ｜｜ PUBLIC SMP 24⧸7 JAVA｜｜ ｜Illmatic Smp.mp4"  # Make sure this path is correct!

# Your audio stream URL
audio_url = "http://stream.zeno.fm/9kaed9hws98uv"

# Your YouTube stream key
# WARNING: Using RTMP is less secure than RTMPS. YouTube strongly recommends RTMPS.
# If possible, use RTMPS instead.
stream_key = "mqzu-y4k5-44uq-e900-2hvu"

# YouTube RTMP URL (WARNING: Less secure than RTMPS)
# Check your YouTube Live dashboard for the exact RTMP URL if you must use it.
# YouTube usually provides an RTMPS URL by default.
youtube_rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

# FFmpeg command with your specified inputs and settings
ffmpeg_command = [
    'ffmpeg',
    '-stream_loop', '-1',  # Loop video infinitely
    '-re',                 # Read input at native frame rate
    '-i', video_file,      # Video input
    '-stream_loop', '-1',  # Loop audio infinitely
    '-re',                 # Read input at native frame rate
    '-i', audio_url,       # Audio input
    '-vcodec', 'libx264',
    '-pix_fmt', 'yuvj420p',
    '-maxrate', '3500k',    # Maximum video bitrate
    '-preset', 'superfast', # Encoding speed/quality trade-off (ultrafast is fast, lower quality)
    '-r', '30',             # Video frame rate (1 frame per second) - This seems very low, consider increasing it!
    '-g', '50',            # GOP size (Group of Pictures)
    '-c:a', 'aac',
    '-b:a', '128k',
    '-ar', '44100',
    '-strict', 'experimental', # Required for some AAC encoders
    '-video_track_timescale', '1000',
    '-b:v', '3000k',       # Video bitrate
    '-f', 'flv',
    youtube_rtmp_url
]

# --- Script Logic (same as before) ---

def start_streaming():
    """Starts the FFmpeg process to stream."""
    print("Starting stream...")
    try:
        # Use stdout and stderr to capture FFmpeg's output
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return process
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please ensure it's installed and in your system's PATH.")
        return None
    except Exception as e:
        print(f"An error occurred while starting FFmpeg: {e}")
        # Print the command being executed for debugging
        print(f"FFmpeg command attempted: {' '.join(ffmpeg_command)}")
        return None

if __name__ == "__main__":
    print("Starting YouTube livestream...")
    while True:
        ffmpeg_process = start_streaming()

        if ffmpeg_process:
            print("FFmpeg process started. Monitoring...")
            try:
                # Add a loop to read and print FFmpeg's output
                while ffmpeg_process.poll() is None:
                    output = ffmpeg_process.stderr.readline() # FFmpeg usually outputs progress and errors to stderr
                    if output:
                        print(f"FFmpeg: {output.strip()}")
                    time.sleep(0.1) # Small delay to avoid busy-waiting

                # Process has exited, read remaining output
                remaining_output = ffmpeg_process.stderr.read()
                if remaining_output:
                    print(f"FFmpeg final output:\n{remaining_output.strip()}")

                return_code = ffmpeg_process.returncode
                if return_code != 0:
                    print(f"FFmpeg process exited with error code {return_code}. Restarting in 10 seconds...")
                else:
                     print("FFmpeg process exited cleanly (unexpected for looping). Restarting in 10 seconds...")

                ffmpeg_process.terminate() # Ensure process is terminated if it didn't exit cleanly
                time.sleep(10)

            except KeyboardInterrupt:
                print("Ctrl+C detected. Stopping stream...")
                ffmpeg_process.terminate()
                break
            except Exception as e:
                print(f"An error occurred while monitoring FFmpeg: {e}")
                print("Restarting FFmpeg in 10 seconds...")
                if ffmpeg_process.poll() is None: # Check if process is still running before terminating
                     ffmpeg_process.terminate()
                time.sleep(10)

        else:
            print("Failed to start FFmpeg. Retrying in 60 seconds...")
            time.sleep(60)