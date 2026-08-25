with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

text = text.replace('request.addOption("-o", "${item.settings.filenamePattern.replace(\\"\\\\$title\\", cleanTitle)}.% (ext)s")', 'request.addOption("-o", item.settings.filenamePattern.replace("\\\\$title", cleanTitle) + ".%(ext)s")')
text = text.replace('.% (ext)s', '.%(ext)s') # Just in case

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
