with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "val cleanTitle = item.title.replace(Regex" in line:
        lines[i] = '            val cleanTitle = item.title.replace(Regex("[^a-zA-Z0-9.\\\\- ]"), "_")\n'
    if "item.settings.filenamePattern.replace" in line:
        lines[i] = '            request.addOption("-o", "${item.settings.filenamePattern.replace(\\"\\\\$title\\", cleanTitle)}.% (ext)s")\n'

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.writelines(lines)
