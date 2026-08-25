import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

content = content.replace('request.addOption("--merge-output-format", "mp4")', '// request.addOption("--merge-output-format", "mp4") // removed to prevent transcoding failures')

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
