with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

text = text.replace("tmpDir.listFiles()?.forEach", "tmpDir?.listFiles()?.forEach")
text = text.replace("tmpDir.deleteRecursively()", "tmpDir?.deleteRecursively()")

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
