with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

text = text.replace('replace("\\\\$title", cleanTitle)', 'replace("\\$title", cleanTitle)')

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
