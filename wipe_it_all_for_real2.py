import urllib.request
import os
import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Replace any lingering q.map issues
text = text.replace("""            _downloadQueue.update { q -> 
                 q.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it } 
             }""", """            _downloadQueue.value = _downloadQueue.value.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it }""")

text = text.replace("""        _downloadQueue.update { q ->
            q.map { if (it.id == id && it.status == "Downloading") it.copy(status = "Paused", downloadSpeed = "Paused") else it }
        }""", """        _downloadQueue.value = _downloadQueue.value.map { if (it.id == id && it.status == "Downloading") it.copy(status = "Paused", downloadSpeed = "Paused") else it }""")

text = text.replace("""        _downloadQueue.update { q ->
            q.map { if (it.id == id && it.status == "Paused") it.copy(status = "Downloading", downloadSpeed = "Resuming...") else it }
        }""", """        _downloadQueue.value = _downloadQueue.value.map { if (it.id == id && it.status == "Paused") it.copy(status = "Downloading", downloadSpeed = "Resuming...") else it }""")


with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
