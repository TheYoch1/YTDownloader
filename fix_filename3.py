with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

target = """            // Name format
            val cleanTitle = item.title.replace(Regex("[^a-zA-Z0-9.\\\\- ]"), "_")
            request.addOption("-o", item.settings.filenamePattern.replace("$title", cleanTitle) + ".%(ext)s")"""

target2 = '            val cleanTitle = item.title.replace(Regex("[^a-zA-Z0-9.\\\\- ]"), "_")'

replacement = """            // Name format
            request.addOption("-o", "%(title)s.%(ext)s")
            // Clean title removed"""

if target in text:
    text = text.replace(target, replacement)
else:
    # Try finding exact lines
    lines = text.split("\\n")
    for i, line in enumerate(lines):
        if "val cleanTitle = item.title.replace(Regex(" in line:
            lines[i] = "            // val cleanTitle removed"
        elif "request.addOption(\"-o\", item.settings.filenamePattern.replace" in line:
            lines[i] = "            request.addOption(\"-o\", \"%(title)s.%(ext)s\")"
    text = "\\n".join(lines)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
