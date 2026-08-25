import re
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

text = text.replace(
    '\"${(avgProgress * 100).toInt()}%\"',
    '\"${avgProgress.toInt()}%\"'
)
text = text.replace(
    'text = \"${(download.progress * 100).toInt()}%\"',
    'text = \"${download.progress.toInt()}%\"'
)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
