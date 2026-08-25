package com.aistudio.ytdownloader

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

enum class ConflictResolution { SKIP, OVERWRITE, KEEP_BOTH }
data class ConflictDialogState(val fileName: String, val deferred: CompletableDeferred<ConflictResolution>)

class DownloaderViewModel(application: Application) : AndroidViewModel(application) {
    val isStorageFull = MutableStateFlow(false)
    
    init {
        // Monitor storage space periodically
        viewModelScope.launch(Dispatchers.IO) {
            while (true) {
                try {
                    val stat = StatFs(Environment.getExternalStorageDirectory().path)
                    val bytesAvailable = stat.availableBlocksLong * stat.blockSizeLong
                    val isFull = bytesAvailable < 500 * 1024 * 1024 // 500 MB threshold
                    if (isFull != isStorageFull.value) {
                        isStorageFull.value = isFull
                        if (!isFull) {
                            // Storage freed, auto-resume any Paused downloads
                            _downloadQueue.update { q ->
                                q.map { if (it.status == "Paused") it.copy(status = "Downloading", downloadSpeed = "Resuming...") else it }
                            }
                        } else {
                            // Storage full, auto-pause active downloads
                            _downloadQueue.update { q ->
                                q.map { if (it.status == "Downloading") it.copy(status = "Paused", downloadSpeed = "No Space") else it }
                            }
                        }
                    }
                } catch (e: Exception) {}
                delay(5000)
            }
        }
    }
    val fileConflictState = MutableStateFlow<ConflictDialogState?>(null)
    
    fun resolveConflict(resolution: ConflictResolution) {
        fileConflictState.value?.deferred?.complete(resolution)
    }
    private val repository = SettingsRepository(application)
    
    private val _appConfig = MutableStateFlow(AppConfig())
    val appConfig: StateFlow<AppConfig> = _appConfig.asStateFlow()

    private val _downloadQueue = MutableStateFlow<List<QueuedDownload>>(emptyList())
    val downloadQueue: StateFlow<List<QueuedDownload>> = _downloadQueue.asStateFlow()

    private val _currentSettings = MutableStateFlow(DownloadSettings())
    val currentSettings: StateFlow<DownloadSettings> = _currentSettings.asStateFlow()

    private val downloadChannel = Channel<String>(Channel.UNLIMITED)
    private var currentDownloadJob: Job? = null
    private var currentDownloadId: String? = null

    init {
        createNotificationChannel()

        viewModelScope.launch {
            repository.downloadSettingsFlow.collect { settings ->
                _currentSettings.value = settings
            }
        }

        viewModelScope.launch {
            repository.appConfigFlow.collect { config ->
                _appConfig.value = config
            }
        }
        
        // Concurrent processor loop with ThreadPoolExecutor
        val executor = java.util.concurrent.ThreadPoolExecutor(
            1, 1, 0L, java.util.concurrent.TimeUnit.MILLISECONDS,
            java.util.concurrent.LinkedBlockingQueue<Runnable>()
        )
        val dispatcher = executor.asCoroutineDispatcher()

        // Auto-resume on network reconnect
        viewModelScope.launch {
            var wasDisconnected = !NetworkMonitor.isConnected.value
            NetworkMonitor.isConnected.collect { connected ->
                if (connected && wasDisconnected) {
                    _downloadQueue.value.forEach { item ->
                        if (item.status == "Error" && item.errorMessage?.contains("storage", ignoreCase = true) != true) {
                            retryDownload(item.id)
                        }
                    }
                }
                wasDisconnected = !connected
            }
        }

        viewModelScope.launch {
            // Watch config for max concurrent downloads changes and update Executor
            launch {
                _appConfig.collect { config ->
                    val max = config.maxConcurrentDownloads.coerceAtLeast(1)
                    executor.corePoolSize = max
                    executor.maximumPoolSize = max
                }
            }
            
            for (id in downloadChannel) {
                val item = _downloadQueue.value.find { it.id == id }
                if (item == null || item.status == "Cancelled") continue
                
                // Submit to the executor-backed dispatcher to handle concurrency safely
                launch(dispatcher) {
                    processDownload(id)
                }
            }
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = "Downloads"
            val descriptionText = "Notifications for download status"
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel("DOWNLOAD_CHANNEL", name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager = 
                getApplication<Application>().getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    private fun showNotification(title: String, content: String, notificationId: Int = UUID.randomUUID().hashCode(), intent: android.app.PendingIntent? = null) {
        val notificationManager = 
            getApplication<Application>().getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        
        val builder = NotificationCompat.Builder(getApplication(), "DOWNLOAD_CHANNEL")
            .setSmallIcon(android.R.drawable.stat_sys_download_done)
            .setContentTitle(title)
            .setContentText(content)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true)
            
        if (intent != null) {
            builder.setContentIntent(intent)
        }
        
        notificationManager.notify(notificationId, builder.build())
    }
    
    private fun updateNotificationProgress(id: String, title: String, progress: Float, speed: String) {
        val context = getApplication<Application>()
        val intent = Intent(context, DownloadService::class.java).apply {
            action = DownloadService.ACTION_UPDATE
            putExtra(DownloadService.EXTRA_TITLE, title)
            putExtra(DownloadService.EXTRA_STATUS, speed)
            putExtra(DownloadService.EXTRA_PROGRESS, progress * 100f)
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            context.startForegroundService(intent)
        } else {
            context.startService(intent)
        }
    }
    
    private fun startForegroundService(title: String) {
        val context = getApplication<Application>()
        val intent = Intent(context, DownloadService::class.java).apply {
            action = DownloadService.ACTION_START
            putExtra(DownloadService.EXTRA_TITLE, title)
            putExtra(DownloadService.EXTRA_STATUS, "Starting...")
            putExtra(DownloadService.EXTRA_PROGRESS, 0f)
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            context.startForegroundService(intent)
        } else {
            context.startService(intent)
        }
    }
    
    private fun stopForegroundServiceIfDone() {
        val active = _downloadQueue.value.any { it.status == "Downloading" || it.status == "Extracting" }
        if (!active) {
            val context = getApplication<Application>()
            val intent = Intent(context, DownloadService::class.java).apply {
                action = DownloadService.ACTION_STOP
            }
            context.startService(intent)
        }
    }
    
    private fun logError(error: String) {
        try {
            val file = File(getApplication<Application>().filesDir, "error_log.txt")
            file.appendText("${System.currentTimeMillis()}: $error\n")
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun updateConfig(config: AppConfig) {
        _appConfig.value = config
        viewModelScope.launch {
            repository.updateAppConfig(config)
        }
    }

    fun updateCurrentSettings(settings: DownloadSettings) {
        _currentSettings.value = settings
        viewModelScope.launch {
            repository.updateDownloadSettings(settings)
        }
    }

    suspend fun fetchAvailableQualities(url: String): List<QualityOption> = withContext(Dispatchers.IO) {
        try {
            if (url.contains("list=")) return@withContext VideoQuality.values().map { QualityOption(it, "") }
            val req = com.yausername.youtubedl_android.YoutubeDLRequest(url)
            req.addOption("--extractor-args", "youtube:player-client=web,mweb")
            val info = YoutubeDL.getInstance().getInfo(req)
            val formats = info.formats ?: emptyList()
            
            val bestAudioSize = formats.filter { it.acodec != "none" && it.vcodec == "none" }
                                     .maxByOrNull { it.fileSize }?.fileSize ?: 0L
                                     
            val formatResolutions = formats.flatMap { listOfNotNull(it.height, it.width) }.toSet()
            if (formatResolutions.isEmpty()) return@withContext VideoQuality.values().map { QualityOption(it, "") }
            
            val available = VideoQuality.values().filter { q ->
                val qRes = q.label.replace("p", "").toInt()
                formatResolutions.contains(qRes)
            }
            
            val finalQualities = if (available.isEmpty()) {
                val maxHeight = formatResolutions.maxOrNull() ?: 1080
                val filtered = VideoQuality.values().filter { it.label.replace("p", "").toInt() <= maxHeight }
                if (filtered.isEmpty()) VideoQuality.values().toList() else filtered
            } else {
                available
            }
            
            finalQualities.map { quality ->
                val qRes = quality.label.replace("p", "").toInt()
                // find best video for this res
                val vFormat = formats.filter { (it.height == qRes || it.width == qRes) && it.vcodec != "none" }
                                     .maxByOrNull { it.fileSize }
                val vSize = vFormat?.fileSize ?: 0L
                val totalBytes = vSize + bestAudioSize
                val sizeStr = if (totalBytes > 0) {
                    String.format("%.1f MB", totalBytes / (1024.0 * 1024.0))
                } else {
                    ""
                }
                QualityOption(quality, sizeStr)
            }
        } catch(e: Exception) {
            VideoQuality.values().map { QualityOption(it, "") }
        }
    }

    fun addDownload(url: String, initialTitle: String? = null, specificSettings: DownloadSettings? = null) {
        if (url.isBlank()) return
        
        try {
            val stat = android.os.StatFs(android.os.Environment.getExternalStorageDirectory().path)
            val bytesAvailable = stat.availableBlocksLong * stat.blockSizeLong
            if (bytesAvailable < 500 * 1024 * 1024) { // less than 500 MB
                val newDownload = QueuedDownload(
                    id = java.util.UUID.randomUUID().toString(),
                    title = initialTitle ?: url,
                    url = url,
                    isPlaylist = url.contains("list="),
                    status = "Error",
                    errorMessage = "Not enough storage available. Please free up space (Need at least 500MB).",
                    settings = specificSettings ?: _currentSettings.value.copy()
                )
                _downloadQueue.update { it + newDownload }
                return
            }
        } catch (e: Exception) {}
        
        if (!NetworkMonitor.isConnected.value) {
            val newDownload = QueuedDownload(
                id = java.util.UUID.randomUUID().toString(),
                title = initialTitle ?: url,
                url = url,
                isPlaylist = url.contains("list="),
                status = "Error",
                errorMessage = "No internet connection available.",
                settings = specificSettings ?: _currentSettings.value.copy()
            )
            _downloadQueue.update { it + newDownload }
            return
        }
        
        if (_appConfig.value.wifiOnly && !NetworkMonitor.isWifiConnected.value) {
            val newDownload = QueuedDownload(
                id = java.util.UUID.randomUUID().toString(),
                title = initialTitle ?: url,
                url = url,
                isPlaylist = url.contains("list="),
                status = "Error",
                errorMessage = "Wi-Fi connection required.",
                settings = specificSettings ?: _currentSettings.value.copy()
            )
            _downloadQueue.update { it + newDownload }
            return
        }
        
        val newDownload = QueuedDownload(
            id = UUID.randomUUID().toString(),
            title = initialTitle ?: "Pending...",
            url = url,
            isPlaylist = url.contains("list="),
            status = "Queued",
            settings = specificSettings ?: _currentSettings.value.copy()
        )
        
        _downloadQueue.update { it + newDownload }
        downloadChannel.trySend(newDownload.id)
    }

    private suspend fun processDownload(id: String) {
        val application = getApplication<Application>()
        var tmpDir: File? = null
        try {
            val itemInfo = _downloadQueue.value.find { it.id == id }
            if (itemInfo == null || itemInfo.status == "Cancelled") return
            
            if (_appConfig.value.wifiOnly && !NetworkMonitor.isWifiConnected.value) {
                _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Error", errorMessage = "Wi-Fi connection required.") else it } }
                return
            }
            
            val url = itemInfo.url
            val settings = itemInfo.settings
            
            _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Extracting") else it } }
            
            val isPlaylist = itemInfo.isPlaylist
            var titleStr = itemInfo.title
            var finalSaveDirStr = ""
            var savedFileUri: String? = null
            
            startForegroundService(titleStr)
            withContext(Dispatchers.IO) {
                try {
                    val req = com.yausername.youtubedl_android.YoutubeDLRequest(url)
            req.addOption("--extractor-args", "youtube:player-client=web,mweb")
            val info = YoutubeDL.getInstance().getInfo(req)
                    titleStr = info.title ?: "Unknown Title"
                    _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(title = titleStr) else it } }
                } catch(e: Exception) {
                    e.printStackTrace()
                }
                
                _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Downloading") else it } }
                
                tmpDir = File(application.cacheDir, id)
                tmpDir?.mkdirs()
                
                val request = YoutubeDLRequest(url)
                request.addOption("--extractor-args", "youtube:player-client=web,mweb")
                request.addOption("--force-overwrites")
                request.addOption("--retries", "infinite")
                request.addOption("--fragment-retries", "infinite")
                request.addOption("--retry-sleep", "5")
                request.addOption("--socket-timeout", "30")
                if (isPlaylist) {
                    request.addOption("--yes-playlist")
                    request.addOption("-o", "${tmpDir?.absolutePath}/%(playlist_index)s - %(title)s.%(ext)s")
                } else {
                    request.addOption("--no-playlist")
                    request.addOption("-o", "${tmpDir?.absolutePath}/%(title)s.%(ext)s")
                }
                
                if (settings.audioOnly) {
                    request.addOption("-x")
                    request.addOption("--audio-format", settings.saveFormat)
                } else {
                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[height<=2160]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best"
                        "High1440" -> "bestvideo[height<=1440]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best"
                        "High1080" -> "bestvideo[height<=1080]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best"
                        "High720" -> "bestvideo[height<=720]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best"
                        "Medium480" -> "bestvideo[height<=480]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best"
                        "Medium360" -> "bestvideo[height<=360]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best"
                        "Low240" -> "bestvideo[height<=240]+bestaudio[ext=m4a]/bestvideo[height<=240]+bestaudio/best"
                        "Low144" -> "bestvideo[height<=144]+bestaudio[ext=m4a]/bestvideo[height<=144]+bestaudio/best"
                        else -> "bestvideo+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
                    }
                    request.addOption("-f", formatStr)
                    request.addOption("--merge-output-format", "mp4")
                // Removed hardcoded player_client to prevent 360p throttling
                }
                
                if (settings.downloadSubtitles) {
                    request.addOption("--write-auto-subs")
                    request.addOption("--write-subs")
                    request.addOption("--sub-langs", "en,en-US,en-GB")
                    request.addOption("--convert-subs", "srt")
                }
                
                                while (isStorageFull.value && _downloadQueue.value.find { it.id == id }?.status != "Cancelled") {
                    kotlinx.coroutines.delay(2000)
                }
                request.addOption("--verbose")
                


                var currentItemTitle = titleStr
                var lastTime = System.currentTimeMillis()
                var lastBytes = 0L
                var lastSpeedStr = ""
                
                YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->
                    if (isPlaylist && line != null && line.contains("[download] Destination: ")) {
                        val fileName = line.substringAfter("[download] Destination: ").substringAfterLast("/")
                        currentItemTitle = fileName
                    }
                    var currentStatus = _downloadQueue.value.find { it.id == id }?.status
                    if (currentStatus == "Cancelled") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else if (currentStatus == "Paused") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else {
                        // Calculate speed manually by tracking bytes over time
                        var currentBytes = 0L
                        val sizeMatch = Regex("of (~?[0-9.]+)([a-zA-Z]+)").find(line ?: "")
                        if (sizeMatch != null) {
                            val num = sizeMatch.groupValues[1].replace("~", "").toFloatOrNull() ?: 0f
                            val unit = sizeMatch.groupValues[2].lowercase()
                            val multiplier = when {
                                unit.contains("k") -> 1024L
                                unit.contains("m") -> 1024L * 1024L
                                unit.contains("g") -> 1024L * 1024L * 1024L
                                else -> 1L
                            }
                            val totalBytes = (num * multiplier).toLong()
                            currentBytes = (totalBytes * (progress / 100.0)).toLong()
                        } else {
                            val dlMatch = Regex("\\[download\\]\\s+([0-9.]+)([a-zA-Z]+) at").find(line ?: "")
                            if (dlMatch != null) {
                                val num = dlMatch.groupValues[1].toFloatOrNull() ?: 0f
                                val unit = dlMatch.groupValues[2].lowercase()
                                val multiplier = when {
                                    unit.contains("k") -> 1024L
                                    unit.contains("m") -> 1024L * 1024L
                                    unit.contains("g") -> 1024L * 1024L * 1024L
                                    else -> 1L
                                }
                                currentBytes = (num * multiplier).toLong()
                            }
                        }
                        
                        val currentTime = System.currentTimeMillis()
                        val timeDiff = currentTime - lastTime
                        if (timeDiff >= 1000 && currentBytes > lastBytes) {
                            val bytesDiff = currentBytes - lastBytes
                            val speedBps = (bytesDiff * 1000) / timeDiff
                            val speedMBps = speedBps / (1024f * 1024f)
                            lastSpeedStr = if (speedMBps >= 1.0) {
                                String.format(java.util.Locale.US, "%.1f MB/s", speedMBps)
                            } else {
                                val speedKBps = speedBps / 1024f
                                String.format(java.util.Locale.US, "%.1f KB/s", speedKBps)
                            }
                            lastTime = currentTime
                            lastBytes = currentBytes
                        }
                        val speedStr = lastSpeedStr
                        
                        var etaStr = ""
                        if (etaInSeconds > 0) {
                            val mins = etaInSeconds / 60
                            val secs = etaInSeconds % 60
                            etaStr = if (mins > 0) "${mins}m ${secs}s left" else "${secs}s left"
                        }
                        
                        val finalSpeedStr = if (speedStr.isNotEmpty() && etaStr.isNotEmpty()) "$speedStr • ETA $etaStr" else if (etaStr.isNotEmpty()) "ETA $etaStr" else speedStr
                        
                        val displayTitle = if (isPlaylist) currentItemTitle else titleStr
                        _downloadQueue.update { q -> 
                            q.map { if (it.id == id) it.copy(title = displayTitle, progress = progress / 100f, downloadSpeed = finalSpeedStr) else it } 
                        }
                        updateNotificationProgress(id, displayTitle, progress / 100f, finalSpeedStr)
                    }
                }
                
                // Finished downloading to tmpDir. Copy to actual save location.
                val baseSaveDir = if (_appConfig.value.saveDirectory == "Default") {
                    if (settings.audioOnly) "/storage/emulated/0/Download/YT Downloader/Music" else "/storage/emulated/0/Download/YT Downloader/Videos"
                } else _appConfig.value.saveDirectory
                finalSaveDirStr = if (isPlaylist) {
                    if (baseSaveDir.startsWith("content://")) baseSaveDir else "$baseSaveDir/${titleStr.replace(Regex("[\\\\/:*?\"<>|]"), "_")}"
                } else baseSaveDir
                
                tmpDir?.walkTopDown()?.filter { it.isFile }?.forEach { fileToCopy ->
                    if (finalSaveDirStr.startsWith("content://")) {
                        val treeUri = Uri.parse(finalSaveDirStr)
                        var docFile = DocumentFile.fromTreeUri(application, treeUri)
                        
                        if (isPlaylist && docFile != null) {
                            val playlistFolderName = titleStr.replace(Regex("[\\\\/:*?\"<>|]"), "_")
                            var playlistFolder = docFile.findFile(playlistFolderName)
                            if (playlistFolder == null) {
                                playlistFolder = docFile.createDirectory(playlistFolderName)
                            }
                            docFile = playlistFolder
                        }
                        
                        if (docFile != null) {
                            var mimeType = "application/octet-stream"
                            if (fileToCopy.name.endsWith(".mp3") || fileToCopy.name.endsWith(".m4a")) mimeType = "audio/*"
                            else if (fileToCopy.name.endsWith(".mp4") || fileToCopy.name.endsWith(".webm") || fileToCopy.name.endsWith(".mkv")) mimeType = "video/*"
                            else if (fileToCopy.name.endsWith(".vtt") || fileToCopy.name.endsWith(".srt")) mimeType = "text/plain"
                            
                            val newFile = docFile.createFile(mimeType, fileToCopy.name)
                            if (newFile != null) {
                                application.contentResolver.openOutputStream(newFile.uri)?.use { out ->
                                    fileToCopy.inputStream().use { input ->
                                        input.copyTo(out)
                                    }
                                }
                                if (savedFileUri == null || (!fileToCopy.name.endsWith(".vtt") && !fileToCopy.name.endsWith(".srt"))) {
                                    savedFileUri = newFile.uri.toString()
                                }
                            }
                        }
                    } else {
                        // Fallback for standard paths
                        val destDir = File(finalSaveDirStr)
                        if (!destDir.exists()) destDir.mkdirs()
                        var destFile = File(destDir, fileToCopy.name)
                        if (destFile.exists()) {
                            val nameWithoutExtension = fileToCopy.nameWithoutExtension
                            val extension = fileToCopy.extension
                            var counter = 1
                            do {
                                destFile = File(destDir, "${nameWithoutExtension} ($counter).$extension")
                                counter++
                            } while (destFile.exists())
                        }
                        fileToCopy.copyTo(destFile, overwrite = false)
                        
                        // Register with Android MediaStore (Gallery/Music apps)
                        val mime = if (destFile.name.endsWith(".mp4") || destFile.name.endsWith(".webm") || destFile.name.endsWith(".mkv")) "video/*" else "audio/*"
                        android.media.MediaScannerConnection.scanFile(application, arrayOf(destFile.absolutePath), arrayOf(mime), null)
                        
                        if (savedFileUri == null || (!fileToCopy.name.endsWith(".vtt") && !fileToCopy.name.endsWith(".srt"))) {
                            savedFileUri = "file://" + destFile.absolutePath
                            recordDownloadStatsSize(destFile.length())
                        }
                    }
                }
            }
            
            tmpDir?.deleteRecursively()
            
            if (isPlaylist && finalSaveDirStr.startsWith("content://")) {
                savedFileUri = finalSaveDirStr // For playlists, link to the folder
            }
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 1f, downloadSpeed = "", localFilePath = savedFileUri) else it } 
            }
            
            try {
                val historyFile = java.io.File(application.filesDir, "history.log")
                val date = java.text.SimpleDateFormat("yyyy-MM-dd HH:mm", java.util.Locale.getDefault()).format(java.util.Date())
                historyFile.appendText("$date|${if(isPlaylist) "Playlist" else "Video"}|$titleStr\n")
            } catch (e: Exception) { }
            
            val typeStr = if (isPlaylist) "Playlist" else "Video"
            var pendingIntent: android.app.PendingIntent? = null
            if (savedFileUri != null) {
                val intent = android.content.Intent(android.content.Intent.ACTION_VIEW)
                val uri = Uri.parse(savedFileUri)
                if (savedFileUri!!.startsWith("content://") && isPlaylist) {
                    intent.data = uri
                } else if (savedFileUri!!.startsWith("file://")) {
                    val file = java.io.File(uri.path!!)
                    val contentUri = androidx.core.content.FileProvider.getUriForFile(application, "${application.packageName}.provider", file)
                    val mime = if (savedFileUri!!.endsWith(".mp4") || savedFileUri!!.endsWith(".webm") || savedFileUri!!.endsWith(".mkv")) "video/*" else "audio/*"
                    intent.setDataAndType(contentUri, mime)
                    intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                } else {
                    val mime = if (savedFileUri!!.endsWith(".mp4") || savedFileUri!!.endsWith(".webm") || savedFileUri!!.endsWith(".mkv")) "video/*" else "audio/*"
                    intent.setDataAndType(uri, mime)
                    intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                }
                
                val flags = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
                    android.app.PendingIntent.FLAG_IMMUTABLE or android.app.PendingIntent.FLAG_UPDATE_CURRENT
                } else {
                    android.app.PendingIntent.FLAG_UPDATE_CURRENT
                }
                pendingIntent = android.app.PendingIntent.getActivity(application, id.hashCode(), intent, flags)
            }
            
            if (_appConfig.value.notifyOnComplete) {
                showNotification("$typeStr Download Complete", "$titleStr has finished downloading.", id.hashCode(), pendingIntent)
            }
        } catch (e: Exception) {
            tmpDir?.deleteRecursively()
            val currentStatus = _downloadQueue.value.find { it.id == id }?.status
            if (currentStatus == "Cancelled") {
                // already handled
            } else if (currentStatus == "Paused") {
                // keep paused
            } else {
                val errorMsg = e.message ?: e.cause?.message ?: "Unknown error occurred"
                logError(errorMsg)
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id) it.copy(status = "Error", progress = 0f, downloadSpeed = "", errorMessage = errorMsg) else it } 
                }
                val item = _downloadQueue.value.find { it.id == id }
                val typeStr = if (item?.isPlaylist == true) "Playlist" else "Video"
                val intent = android.content.Intent(application, MainActivity::class.java).apply {
                    flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TASK
                }
                val flags = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
                    android.app.PendingIntent.FLAG_IMMUTABLE or android.app.PendingIntent.FLAG_UPDATE_CURRENT
                } else {
                    android.app.PendingIntent.FLAG_UPDATE_CURRENT
                }
                val pendingIntent = android.app.PendingIntent.getActivity(application, id.hashCode(), intent, flags)
                showNotification("$typeStr Download Failed", "${item?.title} encountered an error: $errorMsg", id.hashCode(), pendingIntent)
            }
        } finally {
            stopForegroundServiceIfDone()
        }
    }

    fun cancelDownload(id: String) {
        val item = _downloadQueue.value.find { it.id == id }
        if (item?.status == "Downloading" || item?.status == "Extracting") {
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it } 
            }
            Thread {
                try { YoutubeDL.getInstance().destroyProcessById(id) } catch (e: Exception) {}
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
        val app = getApplication<Application>()
        try {
            // Clean up cache dir from yt-dlp leftovers
            java.io.File(app.cacheDir, "yt-dlp").deleteRecursively()
            // Clean up general yt-dlp tmp files
            val noBackup = app.noBackupFilesDir
            val ytdlDir = java.io.File(noBackup, "youtubedl-android")
            if (ytdlDir.exists()) {
                ytdlDir.listFiles()?.forEach { file -> 
                    if (file.name == "tmp" || file.name.contains("temp") || file.name.endsWith(".part")) {
                        file.deleteRecursively()
                    }
                }
            }
            // Sweep app cache for residual format files
            app.cacheDir.listFiles()?.forEach { file ->
                if (file.name.endsWith(".part") || file.name.endsWith(".ytdl")) {
                    file.delete()
                }
            }
        } catch (e: Exception) {}
    }
    
    private fun recordDownloadStatsSize(bytes: Long) {
        val context = getApplication<Application>()
        val prefs = context.getSharedPreferences("download_stats", Context.MODE_PRIVATE)
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


