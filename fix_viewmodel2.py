import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = """    fun removeDownload(id: String) {
        cancelDownload(id)
        _downloadQueue.update { it.filter { download -> download.id != id } }
    }"""

replacement = """    fun removeDownload(id: String) {
        cancelDownload(id)
        _downloadQueue.update { it.filter { download -> download.id != id } }
    }
    
    fun clearFinishedDownloads() {
        _downloadQueue.update { q ->
            q.filter { it.status != "Completed" && it.status != "Error" && it.status != "Cancelled" }
        }
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
