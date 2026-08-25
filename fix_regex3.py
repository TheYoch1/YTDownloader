with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

text = text.replace(
    'val matchPlaylist = Regex(\\\"\\\"\\\"\\[download\\] Downloading video (\\\\d+) of (\\\\d+)\\\"\\\"\\\").find(line)',
    'val matchPlaylist = Regex(\"\"\"\\[download\\] Downloading video (\\d+) of (\\d+)\"\"\").find(line)'
)
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
