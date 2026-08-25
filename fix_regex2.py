import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

text = re.sub(
    r'val matchPlaylist = Regex\(.*?\)\.find\(line\)',
    r'val matchPlaylist = Regex(\"\"\"\[download\] Downloading video (\\\\d+) of (\\\\d+)\"\"\").find(line)',
    text
)

text = text.replace('val dest = line.substringAfter("[download] Destination: ")', 'val dest = line.substringAfter("[download] Destination: ")')

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
