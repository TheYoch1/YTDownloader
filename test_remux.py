import subprocess
import os

# Create dummy mp4
subprocess.run(["./yt-dlp", "-o", "dummy.mp4", "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4"])
# Convert to mkv manually
subprocess.run(["ffmpeg", "-i", "dummy.mp4", "-c", "copy", "dummy.mkv"])

# Run yt-dlp on the dummy.mkv
subprocess.run(["./yt-dlp", "--remux-video", "mp4", "--postprocessor-args", "VideoRemuxer:-tag:v hvc1", "dummy.mkv"])
