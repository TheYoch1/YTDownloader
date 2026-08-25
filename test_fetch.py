with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

if "fetchAvailableQualities" in content:
    print("Already has fetchAvailableQualities")
else:
    print("Need to add fetchAvailableQualities")
