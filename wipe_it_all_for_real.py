import urllib.request
import os
import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Completely replace the broken functions
text = text.replace("""        cancelDownload(id)
        _downloadQueue.update { q -> q.filter { download -> download.id != id } }""", """        cancelDownload(id)
        _downloadQueue.value = _downloadQueue.value.filter { download -> download.id != id }""")

text = text.replace("""        _downloadQueue.update { q ->
            q.filter { it.status != "Completed" && it.status != "Error" && it.status != "Cancelled" }
        }""", """        _downloadQueue.value = _downloadQueue.value.filter { it.status != "Completed" && it.status != "Error" && it.status != "Cancelled" }""")

text = text.replace("""    fun reorderQueue(fromIndex: Int, toIndex: Int) {
        _downloadQueue.update { q ->
            val mutableQ = q.toMutableList()
            if (fromIndex in mutableQ.indices && toIndex in mutableQ.indices) {
                val item = mutableQ.removeAt(fromIndex)
                mutableQ.add(toIndex, item)
            }
            mutableQ
        }
    }""", """    fun reorderQueue(fromIndex: Int, toIndex: Int) {
        val q = _downloadQueue.value
        val mutableQ = q.toMutableList()
        if (fromIndex in mutableQ.indices && toIndex in mutableQ.indices) {
            val item = mutableQ.removeAt(fromIndex)
            mutableQ.add(toIndex, item)
        }
        _downloadQueue.value = mutableQ
    }""")
    
text = text.replace("""    fun retryDownload(id: String) {
        val download = _downloadQueue.value.find { it.id == id } ?: return
        if (download.status == "Error") {
            _downloadQueue.update { q ->
                q.map { if (it.id == id) it.copy(status = "Queued", progress = 0f, errorMessage = null) else it }
            }
            downloadChannel.trySend(id)
        }
    }""", """    fun retryDownload(id: String) {
        val download = _downloadQueue.value.find { it.id == id } ?: return
        if (download.status == "Error") {
            _downloadQueue.value = _downloadQueue.value.map { if (it.id == id) it.copy(status = "Queued", progress = 0f, errorMessage = null) else it }
            downloadChannel.trySend(id)
        }
    }""")

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
