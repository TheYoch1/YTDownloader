code = """package com.aistudio.ytdownloader

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import android.os.Environment
import androidx.core.app.NotificationCompat
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.receiveAsFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.util.UUID

class DownloaderViewModel(application: Application) : AndroidViewModel(application) {
    private val _downloadQueue = MutableStateFlow<List<QueuedDownload>>(emptyList())
    val downloadQueue: StateFlow<List<QueuedDownload>> = _downloadQueue.asStateFlow()

    private val _appConfig = MutableStateFlow(AppConfig())
    val appConfig: StateFlow<AppConfig> = _appConfig.asStateFlow()

    private val downloadChannel = Channel<String>(Channel.UNLIMITED)

    init {
        // start download worker
        viewModelScope.launch(Dispatchers.IO) {
            for (id in downloadChannel) {
                processDownload(id)
            }
        }
    }

    fun updateConfig(config: AppConfig) {
        _appConfig.value = config
    }

    suspend fun fetchAvailableFormats(url: String): List<FormatOption> = withContext(Dispatchers.IO) {
        try {
            val request = YoutubeDLRequest(url)
            request.addOption("--dump-json")
            request.addOption("--no-playlist")
            
            val response = YoutubeDL.getInstance().execute(request, null, null)
            val jsonOut = response.out
            
            if (jsonOut.isNullOrEmpty()) return@withContext emptyList()
            
            val json = JSONObject(jsonOut)
            val formats = json.optJSONArray("formats") ?: JSONArray()
            
            val result = mutableListOf<FormatOption>()
            val videoOptions = mutableListOf<FormatOption>()
            
            for (i in 0 until formats.length()) {
                val f = formats.optJSONObject(i) ?: continue
                val vcodec = f.optString("vcodec", "none")
                val height = f.optInt("height", 0)
                val formatId = f.optString("format_id", "")
                val filesize = f.optLong("filesize", 0L)
                val ext = f.optString("ext", "")
                
                if (formatId.isEmpty()) continue
                
                if (vcodec != "none" && height >= 480) {
                    val sizeStr = if (filesize > 0) String.format("%.1f MB", filesize / 1024f / 1024f) else ""
                    videoOptions.add(FormatOption(formatId, "Video: ${height}p (MP4)", sizeStr, false, height))
                }
            }
            
            // Audio formats
            result.add(FormatOption("bestaudio[ext=m4a]/bestaudio", "M4A Audio", "", true))
            result.add(FormatOption("bestaudio", "MP3 Audio (Best Quality)", "", true))
            
            // Group by height and pick best format id
            val bestFormatsByHeight = videoOptions.groupBy { it.height }.mapNotNull { (height, formatsList) ->
                formatsList.lastOrNull() 
            }.sortedByDescending { it.height }
            
            result.addAll(bestFormatsByHeight)
            
            if (bestFormatsByHeight.isEmpty()) {
                result.add(FormatOption("bestvideo", "Video: Best Available (MP4)", "", false, 0))
            }
            
            return@withContext result
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }

    fun addDownload(url: String, title: String, isPlaylist: Boolean, settings: DownloadSettings) {
        val id = UUID.randomUUID().toString()
        val download = QueuedDownload(
            id = id,
            title = title,
            url = url,
            isPlaylist = isPlaylist,
            settings = settings
        )
        _downloadQueue.update { it + download }
        downloadChannel.trySend(id)
    }

    private suspend fun processDownload(id: String) {
        var tmpDir: File? = null
        try {
            val item = _downloadQueue.value.find { it.id == id } ?: return
            _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Downloading") else it } }
            
            val app = getApplication<Application>()
            val saveDir = if (_appConfig.value.saveDirectory == "Default") {
                File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), "YTDownloader")
            } else {
                File(_appConfig.value.saveDirectory)
            }
            if (!saveDir.exists()) saveDir.mkdirs()
            
            val request = YoutubeDLRequest(item.url)
            tmpDir = File(app.cacheDir, "yt_tmp_$id")
            if (!tmpDir.exists()) tmpDir.mkdirs()
            request.addOption("-P", tmpDir.absolutePath)
            
            // Name format natively handled by yt-dlp to fix issues
            request.addOption("-o", "%(title)s.%(ext)s")
            
            if (item.settings.audioOnly) {
                request.addOption("-x")
                request.addOption("--audio-format", item.settings.saveFormat)
                if (item.settings.saveFormat == "mp3") {
                    request.addOption("--audio-quality", "0")
                }
                if (item.settings.customFormatId != null) {
                    request.addOption("-f", item.settings.customFormatId!!)
                } else {
                    request.addOption("-f", "bestaudio")
                }
            } else {
                if (item.settings.customFormatId != null) {
                    if (!item.settings.customFormatId!!.contains("+")) {
                        request.addOption("-f", "${item.settings.customFormatId}+bestaudio/best")
                    } else {
                        request.addOption("-f", item.settings.customFormatId!!)
                    }
                } else {
                    request.addOption("-f", "bestvideo+bestaudio/best")
                }
                
                request.addOption("--merge-output-format", "mp4")
                
                if (item.settings.downloadSubtitles) {
                    request.addOption("--write-auto-sub")
                    request.addOption("--sub-lang", "en")
                }
            }
            
            YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->
                val speed = if (etaInSeconds > 0) "ETA: ${etaInSeconds}s" else ""
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id && it.status != "Cancelled" && it.status != "Paused") it.copy(progress = progress, downloadSpeed = speed) else it }
                }
            }
            
            if (_downloadQueue.value.find { it.id == id }?.status == "Cancelled") {
                tmpDir.deleteRecursively()
                return
            }
            _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Finishing") else it } }
            
            var downloadedFile: File? = null
            tmpDir.listFiles()?.forEach { file ->
                if (!file.name.endsWith(".part") && !file.name.endsWith(".ytdl")) {
                    downloadedFile = file
                }
            }
            
            var finalFileUri: String? = null
            if (downloadedFile != null) {
                val destFile = File(saveDir, downloadedFile!!.name)
                var actualDest = destFile
                var counter = 1
                while (actualDest.exists()) {
                    val nameWithoutExt = downloadedFile!!.nameWithoutExtension
                    val ext = downloadedFile!!.extension
                    actualDest = File(saveDir, "${nameWithoutExt}_$counter.$ext")
                    counter++
                }
                downloadedFile!!.copyTo(actualDest, overwrite = true)
                finalFileUri = actualDest.absolutePath
            }
            
            tmpDir.deleteRecursively()
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 100f, downloadSpeed = "Done", localFilePath = finalFileUri) else it }
            }
            
        } catch (e: Exception) {
            tmpDir?.deleteRecursively()
            val currentStatus = _downloadQueue.value.find { it.id == id }?.status
            if (currentStatus != "Cancelled" && currentStatus != "Paused") {
                val errorMsg = e.message ?: "Unknown error"
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id) it.copy(status = "Error", progress = 0f, downloadSpeed = "", errorMessage = errorMsg) else it }
                }
            }
        }
    }
    
    private fun showNotification(title: String, desc: String, id: Int, pendingIntent: android.app.PendingIntent?) {
        val app = getApplication<Application>()
        val manager = app.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel("downloads", "Downloads", NotificationManager.IMPORTANCE_LOW)
            manager.createNotificationChannel(channel)
        }
        val builder = NotificationCompat.Builder(app, "downloads")
            .setSmallIcon(android.R.drawable.stat_sys_download_done)
            .setContentTitle(title)
            .setContentText(desc)
            .setAutoCancel(true)
        if (pendingIntent != null) builder.setContentIntent(pendingIntent)
        manager.notify(id, builder.build())
    }

    fun cancelDownload(id: String) {
        val item = _downloadQueue.value.find { it.id == id }
        if (item?.status == "Downloading" || item?.status == "Extracting") {
            _downloadQueue.value = _downloadQueue.value.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it }
            Thread {
                try { YoutubeDL.getInstance().destroyProcessById(id) } catch (e: Exception) {}
            }.start()
        } else {
            _downloadQueue.value = _downloadQueue.value.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it }
        }
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
}
"""
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(code)
