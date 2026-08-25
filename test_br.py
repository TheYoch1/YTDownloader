with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

print("Bracket count:", text.count("{") - text.count("}"))
