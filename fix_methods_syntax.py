import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()
    
# Remove all Unresolved reference 'it'
text = text.replace("    fun cancelDownload(id: String) {", """
    fun cancelDownload(id: String) {
        val item = _downloadQueue.value.find { it.id == id }
        if (item?.status == "Downloading" || item?.status == "Extracting") {
            _downloadQueue.update { q -> 
                 q.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it } 
             }
            Thread {
                try { com.yausername.youtubedl_android.YoutubeDL.getInstance().destroyProcessById(id) } catch (e: Exception) {}
            }.start()
        } else {
            _downloadQueue.update { q -> 
                 q.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it } 
             }
        }
        stopForegroundServiceIfDone()
    }
""")

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
