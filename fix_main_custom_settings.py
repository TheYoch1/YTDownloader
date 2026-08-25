with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

old = """                    val customSettings = DownloadSettings(
                        audioOnly = isAudio,
                        downloadSubtitles = downloadSubtitles,
                        saveFormat = saveFmt,
                        customFormatId = selectedFormatId
                    )"""

new = """                    val customSettings = DownloadSettings(
                        audioOnly = isAudio,
                        downloadSubtitles = downloadSubtitles,
                        saveFormat = saveFmt,
                        customFormatId = selectedFormatId,
                        formatLabel = if (isAudio) "Audio ($saveFmt)" else "Video (${selectedFormat?.label ?: "Auto"})",
                        selectedHeight = selectedFormat?.height ?: 0
                    )"""

text = text.replace(old, new)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
