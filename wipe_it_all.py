import urllib.request
import os

# We will simply revert the DownloaderViewModel locally and then reapply our clean patch
# But we can't fetch it, so let's just parse line by line and fix the _downloadQueue.update syntax issues which is causing "unresolved reference it"

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()
    
# Replace bad updates
text = text.replace("""_downloadQueue.update { it.filter { download -> download.id != id } }""", """_downloadQueue.update { q -> q.filter { download -> download.id != id } }""")

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)

