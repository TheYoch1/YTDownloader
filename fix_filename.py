import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Replace the manual regex and `-o` argument
old_name_code = """            // Name format
            val cleanTitle = item.title.replace(Regex("[^a-zA-Z0-9.\\\\- ]"), "_")
            request.addOption("-o", item.settings.filenamePattern.replace("$title", cleanTitle) + ".%(ext)s")"""

new_name_code = """            // Name format (using yt-dlp native title to support all languages)
            request.addOption("-o", "%(title)s.%(ext)s")"""

text = text.replace(old_name_code, new_name_code)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
