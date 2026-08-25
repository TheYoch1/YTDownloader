import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
    'val activeDownloads = downloads.filter { it.status != "Cancelled" }',
    'val activeDownloads = downloads.filter { it.status != "Completed" && it.status != "Cancelled" }'
)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
