import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''    fun removeDownload(id: String) {
        cancelDownload(id)
        _downloadQueue.update { it.filter { download -> download.id != id } }
    }'''

rep = '''    fun removeDownload(id: String) {
        cancelDownload(id)
        _downloadQueue.update { it.filter { download -> download.id != id } }
    }

    fun retryDownload(id: String) {
        val download = _downloadQueue.value.find { it.id == id } ?: return
        if (download.status == "Error") {
            _downloadQueue.update { q ->
                q.map { if (it.id == id) it.copy(status = "Queued", progress = 0f, errorMessage = null) else it }
            }
            downloadChannel.trySend(id)
        }
    }'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)

print("Retry added")
