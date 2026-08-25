import sys

with open('app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt', 'r') as f:
    content = f.read()

imports = '''import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import android.net.Uri
import androidx.documentfile.provider.DocumentFile
import java.io.File
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
'''

if 'import com.yausername.youtubedl_android.YoutubeDL' not in content:
    content = content.replace('import java.util.UUID', 'import java.util.UUID\n' + imports)

process_download_old = '''    private suspend fun processDownload(id: String) {
        try {
            _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Extracting") else it } }
            delay(1500)
            
            val isPlaylist = _downloadQueue.value.find { it.id == id }?.isPlaylist == true
            val titleStr = if (isPlaylist) "Playlist: Top Hits" else "Video Title Placeholder"
            
            _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(title = titleStr, status = "Downloading") else it } }
            
            // Randomly fail sometimes to demonstrate error notification (10% chance)
            val willFail = (1..10).random() == 1
            val failAtProgress = if (willFail) (20..80).random() else 100
            // Simulate progress
            for (i in 1..100) {
                if (willFail && i == failAtProgress) {
                    throw Exception("Simulated network error")
                }
                
                var currentStatus = _downloadQueue.value.find { it.id == id }?.status
                while (currentStatus == "Paused") {
                    delay(200)
                    currentStatus = _downloadQueue.value.find { it.id == id }?.status
                }
                if (currentStatus == "Cancelled") {
                    throw CancellationException()
                }
                
                delay((30..80).random().toLong())
                
                // Simulate download speed
                val speedVal = (15..55).random() / 10f
                val speedStr = String.format("%.1f MB/s", speedVal)
                
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id && it.status != "Paused" && it.status != "Cancelled") it.copy(progress = i / 100f, downloadSpeed = speedStr, status = "Downloading") else it } 
                }
            }
            
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 1f, downloadSpeed = "") else it } 
            }
            
            val typeStr = if (isPlaylist) "Playlist" else "Video"
            showNotification("$typeStr Download Complete", "$titleStr has finished downloading.")
        } catch (e: CancellationException) {
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it } 
            }
            throw e
        } catch (e: Exception) {
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Error", progress = 0f, downloadSpeed = "") else it } 
            }
            
            val item = _downloadQueue.value.find { it.id == id }
            val typeStr = if (item?.isPlaylist == true) "Playlist" else "Video"
            showNotification("$typeStr Download Failed", "${item?.title} encountered an error: ${e.message}")
        }
    }'''

process_download_new = '''    private suspend fun processDownload(id: String) {
        val application = getApplication<Application>()
        var tmpDir: File? = null
        try {
            val itemInfo = _downloadQueue.value.find { it.id == id }
            if (itemInfo == null || itemInfo.status == "Cancelled") return
            
            val url = itemInfo.url
            val settings = itemInfo.settings
            
            _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Extracting") else it } }
            
            val isPlaylist = itemInfo.isPlaylist
            var titleStr = itemInfo.title
            
            withContext(Dispatchers.IO) {
                try {
                    val info = YoutubeDL.getInstance().getInfo(url)
                    titleStr = info.title ?: "Unknown Title"
                    _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(title = titleStr) else it } }
                } catch(e: Exception) {
                    e.printStackTrace()
                }
                
                _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Downloading") else it } }
                
                tmpDir = File(application.cacheDir, id)
                tmpDir?.mkdirs()
                
                val request = YoutubeDLRequest(url)
                request.addOption("-o", "${tmpDir?.absolutePath}/%(title)s.%(ext)s")
                
                if (settings.audioOnly) {
                    request.addOption("-x")
                    request.addOption("--audio-format", settings.saveFormat)
                } else {
                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[height<=2160]+bestaudio/best"
                        "High1440" -> "bestvideo[height<=1440]+bestaudio/best"
                        "High1080" -> "bestvideo[height<=1080]+bestaudio/best"
                        "High720" -> "bestvideo[height<=720]+bestaudio/best"
                        "Medium480" -> "bestvideo[height<=480]+bestaudio/best"
                        "Medium360" -> "bestvideo[height<=360]+bestaudio/best"
                        "Low240" -> "bestvideo[height<=240]+bestaudio/best"
                        "Low144" -> "bestvideo[height<=144]+bestaudio/best"
                        else -> "bestvideo+bestaudio/best"
                    }
                    request.addOption("-f", formatStr)
                }
                
                if (settings.downloadSubtitles) {
                    request.addOption("--write-sub")
                    request.addOption("--sub-langs", "en")
                }
                
                YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->
                    var currentStatus = _downloadQueue.value.find { it.id == id }?.status
                    if (currentStatus == "Cancelled") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else if (currentStatus == "Paused") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                        // It will stop, throwing exception, but wait, if it throws we need to handle it.
                    } else {
                        val speedStr = if (etaInSeconds > 0) "${etaInSeconds}s left" else ""
                        _downloadQueue.update { q -> 
                            q.map { if (it.id == id) it.copy(progress = progress / 100f, downloadSpeed = speedStr) else it } 
                        }
                    }
                }
                
                // Finished downloading to tmpDir. Copy to actual save location.
                val saveDir = _appConfig.value.saveDirectory
                if (saveDir.startsWith("content://")) {
                    val treeUri = Uri.parse(saveDir)
                    val docFile = DocumentFile.fromTreeUri(application, treeUri)
                    tmpDir?.listFiles()?.forEach { fileToCopy ->
                        if (docFile != null) {
                            var mimeType = "application/octet-stream"
                            if (fileToCopy.name.endsWith(".mp3") || fileToCopy.name.endsWith(".m4a")) mimeType = "audio/*"
                            else if (fileToCopy.name.endsWith(".mp4") || fileToCopy.name.endsWith(".webm") || fileToCopy.name.endsWith(".mkv")) mimeType = "video/*"
                            
                            val newFile = docFile.createFile(mimeType, fileToCopy.name)
                            if (newFile != null) {
                                application.contentResolver.openOutputStream(newFile.uri)?.use { out ->
                                    fileToCopy.inputStream().use { input ->
                                        input.copyTo(out)
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            tmpDir?.deleteRecursively()
            
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 1f, downloadSpeed = "") else it } 
            }
            
            val typeStr = if (isPlaylist) "Playlist" else "Video"
            showNotification("$typeStr Download Complete", "$titleStr has finished downloading.")
        } catch (e: Exception) {
            tmpDir?.deleteRecursively()
            val currentStatus = _downloadQueue.value.find { it.id == id }?.status
            if (currentStatus == "Cancelled") {
                // already handled
            } else if (currentStatus == "Paused") {
                // keep paused
            } else {
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id) it.copy(status = "Error", progress = 0f, downloadSpeed = "") else it } 
                }
                val item = _downloadQueue.value.find { it.id == id }
                val typeStr = if (item?.isPlaylist == true) "Playlist" else "Video"
                showNotification("$typeStr Download Failed", "${item?.title} encountered an error: ${e.message}")
            }
        }
    }'''

content = content.replace(process_download_old, process_download_new)

with open('app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt', 'w') as f:
    f.write(content)

