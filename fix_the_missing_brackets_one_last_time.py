# The issue is we STILL have 02 open at line 173 and 01 open at line 174. 
# But wait... the bracket counter is showing 03 at line 172. This means the balance is positive.
# Meaning we have extra opening brackets OR we are missing closing brackets!
# I will just write a simpler fix: replace everything from cancelDownload down with a perfectly formatted block and delete the rest.
import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

lines = text.split('\n')
for i, line in enumerate(lines):
    if "fun cancelDownload(id: String) {" in line:
        top_half = '\n'.join(lines[:i])
        break

# Make sure top_half ends cleanly before cancelDownload
# Specifically, we know processDownload needs to end cleanly. Let's find the finally { ... }
finally_idx = top_half.rfind("} finally {")
if finally_idx != -1:
    top_half = top_half[:finally_idx] + "} finally {\n            stopForegroundServiceIfDone()\n        }\n    }\n"

bottom_half = """
    fun cancelDownload(id: String) {
        val item = _downloadQueue.value.find { it.id == id }
        if (item?.status == "Downloading" || item?.status == "Extracting") {
            _downloadQueue.value = _downloadQueue.value.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it }
            Thread {
                try { com.yausername.youtubedl_android.YoutubeDL.getInstance().destroyProcessById(id) } catch (e: Exception) {}
            }.start()
        } else {
            _downloadQueue.value = _downloadQueue.value.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it }
        }
        stopForegroundServiceIfDone()
    }

    fun pauseDownload(id: String) {
        _downloadQueue.value = _downloadQueue.value.map { if (it.id == id && it.status == "Downloading") it.copy(status = "Paused", downloadSpeed = "Paused") else it }
    }

    fun resumeDownload(id: String) {
        _downloadQueue.value = _downloadQueue.value.map { if (it.id == id && it.status == "Paused") it.copy(status = "Downloading", downloadSpeed = "Resuming...") else it }
    }

    fun removeDownload(id: String) {
        cancelDownload(id)
        _downloadQueue.value = _downloadQueue.value.filter { download -> download.id != id }
    }

    fun reorderQueue(fromIndex: Int, toIndex: Int) {
        val q = _downloadQueue.value
        val mutableQ = q.toMutableList()
        if (fromIndex in mutableQ.indices && toIndex in mutableQ.indices) {
            val item = mutableQ.removeAt(fromIndex)
            mutableQ.add(toIndex, item)
        }
        _downloadQueue.value = mutableQ
    }
        
    fun clearFinishedDownloads() {
        _downloadQueue.value = _downloadQueue.value.filter { it.status != "Completed" && it.status != "Error" && it.status != "Cancelled" }
    }

    fun retryDownload(id: String) {
        val download = _downloadQueue.value.find { it.id == id } ?: return
        if (download.status == "Error") {
            _downloadQueue.value = _downloadQueue.value.map { if (it.id == id) it.copy(status = "Queued", progress = 0f, errorMessage = null) else it }
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
    f.write(top_half + bottom_half)
