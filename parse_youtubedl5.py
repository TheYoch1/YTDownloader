import subprocess
out = subprocess.check_output(["javap", "-c", "-p", "-cp", "/tmp/library-aar/classes.jar", "com.yausername.youtubedl_android.YoutubeDL"]).decode("utf-8")
printing = False
for line in out.splitlines():
    if "init(" in line and "Code" not in line: printing = True
    if printing:
        print(line)
        if "312: return" in line: printing = False
