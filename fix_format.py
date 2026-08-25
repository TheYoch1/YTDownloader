import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

def replace_fmt(match):
    height = match.group(1)
    return f'"{match.group(0)}" -> "bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best"'

content = re.sub(r'"High(\d+)" -> "bestvideo\[height<=\d+\]\+bestaudio/best"', replace_fmt, content)
content = re.sub(r'"Medium(\d+)" -> "bestvideo\[height<=\d+\]\+bestaudio/best"', replace_fmt, content)
content = re.sub(r'"Low(\d+)" -> "bestvideo\[height<=\d+\]\+bestaudio/best"', replace_fmt, content)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
