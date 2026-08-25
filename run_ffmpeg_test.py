import subprocess
import os
import glob

paths = glob.glob("/data/app/*/com.aistudio.ytdownloader-*/lib/x86_64")
if paths:
    lib_dir = paths[0]
    ffmpeg_path = os.path.join(lib_dir, "libffmpeg.so")
    print(f"Testing {ffmpeg_path}")
    if os.path.exists(ffmpeg_path):
        try:
            result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True)
            print("Return code:", result.returncode)
            print("Stdout:", result.stdout)
            print("Stderr:", result.stderr)
        except Exception as e:
            print("Error:", e)
else:
    print("No lib dir found")
