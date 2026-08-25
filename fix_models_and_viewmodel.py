import re
with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "r") as f:
    text = f.read()
text = text.replace("    var errorMessage: String? = null,\n    var errorMessage: String? = null,", "    var errorMessage: String? = null,")
with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "w") as f:
    f.write(text)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

text = text.replace(
    'Regex("\\[download\\] Downloading video (\\\\d+) of (\\\\d+)")',
    'Regex("\\\\[download\\\\] Downloading video (\\\\d+) of (\\\\d+)")'
)
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
