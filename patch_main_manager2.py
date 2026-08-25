with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

text = text.replace(
    "val downloads by viewModel.downloadQueue.collectAsState()",
    "val downloads by viewModel.downloadQueue.collectAsState()\n    val individualProgressMap by DownloadManager.progressMap.collectAsState()"
)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)

