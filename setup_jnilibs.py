import urllib.request
import tarfile
import os
import shutil

os.makedirs('app/src/main/jniLibs/x86_64', exist_ok=True)
os.makedirs('app/src/main/jniLibs/arm64-v8a', exist_ok=True)

if os.path.exists('app/src/main/assets/ffmpeg'):
    shutil.move('app/src/main/assets/ffmpeg', 'app/src/main/jniLibs/x86_64/libffmpeg.so')
    print("Moved x86_64 from assets")
elif os.path.exists('ffmpeg'):
    shutil.copy('ffmpeg', 'app/src/main/jniLibs/x86_64/libffmpeg.so')
    print("Moved x86_64 from root")

url = "https://github.com/Khang-NT/ffmpeg-binary-android/releases/download/2018-07-31/arm64-v8a-lite.tar.bz2"
print("Downloading arm64...")
urllib.request.urlretrieve(url, 'arm64.tar.bz2')
print("Extracting arm64...")
with tarfile.open('arm64.tar.bz2', 'r:bz2') as tar:
    tar.extractall(path='arm64_out')

shutil.move('arm64_out/ffmpeg', 'app/src/main/jniLibs/arm64-v8a/libffmpeg.so')
print("Moved arm64 to jniLibs")

if os.path.exists('app/src/main/assets'):
    os.rmdir('app/src/main/assets') # will only succeed if empty, which is fine
