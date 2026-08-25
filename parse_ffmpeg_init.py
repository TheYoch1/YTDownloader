import subprocess
out = subprocess.check_output(["javap", "-c", "-p", "-cp", "/tmp/ffmpeg-aar/classes.jar", "com.yausername.ffmpeg.FFmpeg"]).decode("utf-8")
printing = False
for line in out.splitlines():
    if "init(" in line and "Code" not in line: printing = True
    if printing:
        print(line)
        if "return" in line: printing = False
