import os

code = """package com.aistudio.ytdownloader

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Job
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.CompletableDeferred
import android.os.Environment
import android.os.StatFs
import kotlinx.coroutines.launch
import android.content.Intent
import android.provider.Settings
import androidx.documentfile.provider.DocumentFile
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import java.util.UUID
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.asCoroutineDispatcher
import android.net.Uri
import java.io.File
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import org.json.JSONObject
import org.json.JSONArray

enum class ConflictResolution { SKIP, OVERWRITE, KEEP_BOTH }
data class ConflictDialogState(val fileName: String, val deferred: CompletableDeferred<ConflictResolution>)

class DownloaderViewModel(application: Application) : AndroidViewModel(application) {
    val isStorageFull = MutableStateFlow(false)
    private val _downloadQueue = MutableStateFlow<List<QueuedDownload>>(emptyList())
    val downloadQueue: StateFlow<List<QueuedDownload>> = _downloadQueue.asStateFlow()

    private val _appConfig = MutableStateFlow(AppConfig())
    val appConfig: StateFlow<AppConfig> = _appConfig.asStateFlow()

    val currentSettings = MutableStateFlow(DownloadSettings())

    private val downloadChannel = Channel<String>(Channel.UNLIMITED)
    private val activeJobs = mutableMapOf<String, Job>()
    
    val currentConflictDialog = MutableStateFlow<ConflictDialogState?>(null)

    private val dispatcher = java.util.concurrent.Executors.newFixedThreadPool(4).asCoroutineDispatcher()

    init {
        loadConfig()
        viewModelScope.launch(Dispatchers.IO) {
            while (true) {
                try {
                    val stat = StatFs(Environment.getExternalStorageDirectory().path)
                    val bytesAvailable = stat.availableBlocksLong * stat.blockSizeLong
                    val isFull = bytesAvailable < 500 * 1024 * 1024 // 500 MB threshold
                    if (isFull != isStorageFull.value) {
                        isStorageFull.value = isFull
                        if (!isFull) {
                            _downloadQueue.update { q ->
                                q.map { if (it.status == "Paused" && it.downloadSpeed == "No Space") it.copy(status = "Downloading", downloadSpeed = "Resuming...") else it }
                            }
                        } else {
                            _downloadQueue.update { q ->
                                q.map { if (it.status == "Downloading") it.copy(status = "Paused", downloadSpeed = "No Space") else it }
                            }
                        }
                    }
                } catch (e: Exception) { }
                delay(10000)
            }
        }

        viewModelScope.launch {
            for (id in downloadChannel) {
                if (!activeJobs.containsKey(id) || activeJobs[id]?.isCompleted == true) {
                    val job = viewModelScope.launch(dispatcher) {
                        processDownload(id)
                    }
                    activeJobs[id] = job
                }
            }
        }
    }
    
    private fun loadConfig() {
        val prefs = getApplication<Application>().getSharedPreferences("ytdl_config", Context.MODE_PRIVATE)
        _appConfig.value = AppConfig(
            theme = prefs.getString("theme", "Dark") ?: "Dark",
            accent = prefs.getString("accent", "Teal") ?: "Teal",
            saveDirectory = prefs.getString("saveDirectory", "Default") ?: "Default",
            maxConcurrentDownloads = prefs.getInt("maxConcurrentDownloads", 1),
            colorOffset = prefs.getFloat("colorOffset", -1f),
            confirmExit = prefs.getBoolean("confirmExit", true),
            wifiOnly = prefs.getBoolean("wifiOnly", false),
            notifyOnComplete = prefs.getBoolean("notifyOnComplete", true)
        )
    }

    fun updateConfig(newConfig: AppConfig) {
        _appConfig.value = newConfig
        val prefs = getApplication<Application>().getSharedPreferences("ytdl_config", Context.MODE_PRIVATE)
        prefs.edit()
            .putString("theme", newConfig.theme)
            .putString("accent", newConfig.accent)
            .putString("saveDirectory", newConfig.saveDirectory)
            .putInt("maxConcurrentDownloads", newConfig.maxConcurrentDownloads)
            .putFloat("colorOffset", newConfig.colorOffset)
            .putBoolean("confirmExit", newConfig.confirmExit)
            .putBoolean("wifiOnly", newConfig.wifiOnly)
            .putBoolean("notifyOnComplete", newConfig.notifyOnComplete)
            .apply()
    }

    fun updateCurrentSettings(newSettings: DownloadSettings) {
        currentSettings.value = newSettings
    }
    
    suspend fun fetchAvailableFormats(url: String): List<FormatOption> = withContext(Dispatchers.IO) {
        try {
            val request = YoutubeDLRequest(url)
            request.addOption("--dump-json")
            request.addOption("--no-playlist")
            
            // Bypass PO Token limitations
            request.addOption("--extractor-args", "youtube:player-client=web,mweb")
            
            val response = YoutubeDL.getInstance().execute(request, null, null)
            val jsonOut = response.out
            
            if (jsonOut.isNullOrEmpty()) return@withContext emptyList()
            
            val json = JSONObject(jsonOut)
            val formats = json.optJSONArray("formats") ?: JSONArray()
            
            val result = mutableListOf<FormatOption>()
            for (i in 0 until formats.length()) {
                val f = formats.optJSONObject(i) ?: continue
                val formatId = f.optString("format_id", "")
                val ext = f.optString("ext", "")
                val acodec = f.optString("acodec", "none")
                val vcodec = f.optString("vcodec", "none")
                val filesize = f.optLong("filesize", 0L)
                val formatNote = f.optString("format_note", "")
                val height = f.optInt("height", 0)
                
                if (formatId.isEmpty()) continue
                
                val sizeStr = if (filesize > 0) String.format("%.1f MB", filesize / 1024f / 1024f) else "Unknown Size"
                
                val isAudioOnly = vcodec == "none" || vcodec == ""
                val isVideoOnly = acodec == "none" || acodec == ""
                
                if (isAudioOnly && acodec != "none") {
                    result.add(FormatOption(formatId, "Audio: $ext $formatNote", sizeStr, true))
                } else if (!isAudioOnly && vcodec != "none") {
                    val label = if (isVideoOnly) "Video (No Audio): ${height}p $ext $formatNote" else "Video: ${height}p $ext $formatNote"
                    result.add(FormatOption(formatId, label, sizeStr, false, height))
                }
            }
            
            // Deduplicate and sort
            return@withContext result.distinctBy { it.label }.sortedByDescending { it.height }
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }

    fun addDownload(url: String, title: String, isPlaylist: Boolean, settings: DownloadSettings) {
        val id = UUID.randomUUID().toString()
        val download = QueuedDownload(id, title, url, isPlaylist, settings = settings)
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
            
            // Name format
            val cleanTitle = item.title.replace(Regex("[^a-zA-Z0-9.\\\\- ]"), "_")
            request.addOption("-o", "${item.settings.filenamePattern.replace("\\$title", cleanTitle)}.% (ext)s")
            
            // Bypass PO Token limitations
            request.addOption("--extractor-args", "youtube:player-client=web,mweb")

            if (item.settings.audioOnly) {
                request.addOption("-x")
                request.addOption("--audio-format", item.settings.saveFormat)
                if (item.settings.customFormatId != null) {
                    request.addOption("-f", item.settings.customFormatId!!)
                } else {
                    request.addOption("-f", "bestaudio")
                }
            } else {
                if (item.settings.customFormatId != null) {
                    // For video with custom format, we usually want that format + best audio
                    if (!item.settings.customFormatId!!.contains("+")) {
                        request.addOption("-f", "${item.settings.customFormatId}+bestaudio/best")
                    } else {
                        request.addOption("-f", item.settings.customFormatId!!)
                    }
                } else {
                    val qHeight = item.settings.quality.label.replace("p", "")
                    request.addOption("-f", "bestvideo[height<=$qHeight]+bestaudio/best")
                }
                
                if (item.settings.convert) {
                    request.addOption("--recode-video", item.settings.saveFormat)
                } else {
                    request.addOption("--merge-output-format", item.settings.saveFormat)
                }
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
            
            // Check if cancelled
            if (_downloadQueue.value.find { it.id == id }?.status == "Cancelled") {
                tmpDir.deleteRecursively()
                return
            }

            _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Finishing") else it } }
            
            // Move file to final location
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
