import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# Make it stay in the queue
content = content.replace(
    'val activeDownloads = downloads.filter { it.status != "Completed" && it.status != "Cancelled" }',
    'val activeDownloads = downloads.filter { it.status != "Cancelled" }'
)

content = content.replace(
    'val filteredActiveDownloads = downloads.filter { it.status == "Downloading" || it.status == "Extracting" || it.status == "Queued" || it.status == "Paused" }',
    'val filteredActiveDownloads = downloads.filter { it.status == "Downloading" || it.status == "Extracting" || it.status == "Queued" || it.status == "Paused" || it.status == "Completed" || it.status == "Error" }'
)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
