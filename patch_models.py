with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "r") as f:
    content = f.read()

content = content.replace(
    'var saveDirectory: String = "/storage/emulated/0/Download",',
    'var saveDirectory: String = "/storage/emulated/0/Movies/YT Downloader",\n    var maxConcurrentDownloads: Int = 1,'
)

with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "w") as f:
    f.write(content)
