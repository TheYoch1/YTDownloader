with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

text = text.replace("cancelProgressNotification(id)", "cancelProgressNotification(id)\n            DownloadManager.removeProgress(id)")

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)

