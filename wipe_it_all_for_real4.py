import urllib.request
import os
import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# I see what's happening. The methods are being pushed OUTSIDE the DownloaderViewModel class because of the extra closing bracket
# that was originally left from processDownload catching up.

lines = text.split('\n')
for i, line in enumerate(lines):
    if "fun cancelDownload" in line:
        # Check how many brackets are open right here
        segment = '\n'.join(lines[:i])
        balance = segment.count('{') - segment.count('}')
        print(f"Balance at cancelDownload: {balance}")
        
