import subprocess
import re

out = subprocess.check_output(["javap", "-c", "-p", "-cp", "/tmp/ffmpeg-aar/classes.jar", "com.yausername.ffmpeg.FFmpeg"]).decode("utf-8")
print(out[:2000])
