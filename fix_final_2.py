with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "fun cancelDownload(id: String) {" in line:
        break
    new_lines.append(line)

bottom = """    fun cancelDownload(id: String) {
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
    fun pauseDownload(id: String) {
        _downloadQueue.update { q ->
            q.map { if (it.id == id && it.status == "Downloading") it.copy(status = "Paused", downloadSpeed = "Paused") else it }
        }
    }
    fun resumeDownload(id: String) {
        _downloadQueue.update { q ->
            q.map { if (it.id == id && it.status == "Paused") it.copy(status = "Downloading", downloadSpeed = "Resuming...") else it }
        }
    }
    fun removeDownload(id: String) {
        cancelDownload(id)
        _downloadQueue.update { it.filter { download -> download.id != id } }
    }
    fun reorderQueue(fromIndex: Int, toIndex: Int) {
        _downloadQueue.update { q ->
            val mutableQ = q.toMutableList()
            if (fromIndex in mutableQ.indices && toIndex in mutableQ.indices) {
                val item = mutableQ.removeAt(fromIndex)
                mutableQ.add(toIndex, item)
            }
            mutableQ
        }
    }
        
    fun clearFinishedDownloads() {
        _downloadQueue.update { q ->
            q.filter { it.status != "Completed" && it.status != "Error" && it.status != "Cancelled" }
        }
    }
    fun retryDownload(id: String) {
        val download = _downloadQueue.value.find { it.id == id } ?: return
        if (download.status == "Error") {
            _downloadQueue.update { q ->
                q.map { if (it.id == id) it.copy(status = "Queued", progress = 0f, errorMessage = null) else it }
            }
            downloadChannel.trySend(id)
        }
    }
    private fun recordDownloadStats() {
        val app = getApplication<android.app.Application>()
        try {
            java.io.File(app.cacheDir, "yt-dlp").deleteRecursively()
            val noBackup = app.noBackupFilesDir
            val ytdlDir = java.io.File(noBackup, "youtubedl-android")
            if (ytdlDir.exists()) {
                ytdlDir.listFiles()?.forEach { file -> 
                     if (file.name == "tmp" || file.name.contains("temp") || file.name.endsWith(".part")) {
                        file.deleteRecursively()
                    }
                }
            }
            app.cacheDir.listFiles()?.forEach { file ->
                if (file.name.endsWith(".part") || file.name.endsWith(".ytdl")) {
                    file.delete()
                }
            }
        } catch (e: Exception) {}
    }
        
    private fun recordDownloadStatsSize(bytes: Long) {
        val context = getApplication<android.app.Application>()
        val prefs = context.getSharedPreferences("download_stats", android.content.Context.MODE_PRIVATE)
        val today = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
                
        val countKey = "count_$today"
        val count = prefs.getInt(countKey, 0)
                
        val sizeKey = "size_$today"
        val size = prefs.getLong(sizeKey, 0L)
                
        prefs.edit()
            .putInt(countKey, count + 1)
            .putLong(sizeKey, size + bytes)
            .apply()
    }
}
"""

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.writelines(new_lines)
    f.write(bottom)
