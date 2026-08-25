import urllib.request
urllib.request.urlretrieve("https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp", "yt-dlp")
import os
os.chmod("yt-dlp", 0o755)
