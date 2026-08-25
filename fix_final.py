with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Fix MainActivity first
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    main = f.read()
main = main.replace("var selectedFormatId by remember(formatDialogUrl) { mutableStateOf<String?>(null) }", "var selectedFormatId by remember(formatDialogUrl) { mutableStateOf<String?>(null) }\n        if (formatDialogUrl?.contains(\"list=\") == true) {\n            isAudio = false\n            downloadSubtitles = settings.downloadSubtitles\n        }")
main = main.replace("selectedFormatId = VideoQuality.High720", "selectedFormatId = null")
main = main.replace("selectedQuality = VideoQuality.High720", "") # Remove left over
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(main)
