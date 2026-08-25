import subprocess
out = subprocess.check_output(["javap", "-c", "-p", "-cp", "/tmp/library-aar/classes.jar", "com.yausername.youtubedl_android.YoutubeDL"]).decode("utf-8")
for line in out.splitlines():
    if "ffmpegPath" in line: print(line)
