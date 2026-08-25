with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

text = text.replace('q.map { if (it.id == id) it.copy(status = "Finishing") else it } }', 'q.map { if (it.id == id) it.copy(status = "Finishing") else it } }\n            showProgressNotification("Finishing: ${item.title}", "Merging and saving file...", 100f, id)')

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)
