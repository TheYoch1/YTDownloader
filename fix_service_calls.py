import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target1 = '''            withContext(Dispatchers.IO) {
                try {
                    val req = com.yausername.youtubedl_android.YoutubeDLRequest(url)'''

rep1 = '''            startForegroundService(titleStr)
            withContext(Dispatchers.IO) {
                try {
                    val req = com.yausername.youtubedl_android.YoutubeDLRequest(url)'''
content = content.replace(target1, rep1)

target2 = '''            } catch (e: Exception) {
                if (e !is CancellationException) {
                    _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Error") else it } }
                    logError(e.message ?: "Unknown error")
                }
            } finally {
                activeJobs.remove(id)
            }
        }
        activeJobs[id] = job
    }'''

rep2 = '''            } catch (e: Exception) {
                if (e !is CancellationException) {
                    _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Error") else it } }
                    logError(e.message ?: "Unknown error")
                }
            } finally {
                activeJobs.remove(id)
                stopForegroundServiceIfDone()
                recordDownloadStats()
            }
        }
        activeJobs[id] = job
    }'''
content = content.replace(target2, rep2)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
print("done calls")
