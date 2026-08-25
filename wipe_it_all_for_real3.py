import urllib.request
import os
import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Replace any lingering issues from the last patch with clearFinishedDownloads and others
text = text.replace("""    fun clearFinishedDownloads() {
        _downloadQueue.update { q ->
            q.filter { it.status != "Completed" && it.status != "Error" && it.status != "Cancelled" }
        }
    }""", """    fun clearFinishedDownloads() {
        _downloadQueue.value = _downloadQueue.value.filter { it.status != "Completed" && it.status != "Error" && it.status != "Cancelled" }
    }""")

text = text.replace("""        cancelDownload(id)
        _downloadQueue.update { it.filter { download -> download.id != id } }""", """        cancelDownload(id)
        _downloadQueue.value = _downloadQueue.value.filter { download -> download.id != id }""")


# Delete end of file bracket
if text.endswith("}\n"):
    text = text[:-2]

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
