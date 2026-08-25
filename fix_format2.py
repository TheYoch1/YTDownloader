import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

def clean(match):
    name = match.group(1)
    height = match.group(2)
    return f'"{name}" -> "bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best"'

content = re.sub(r'""(High|Medium|Low)(\d+)" -> "bestvideo\[height<=\d+\]\+bestaudio/best"" -> ".*?"', clean, content)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
