package com.aistudio.ytdownloader

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Environment
import android.os.IBinder
import android.widget.RemoteViews
import androidx.core.app.NotificationCompat
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File
import java.util.concurrent.ConcurrentHashMap
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

object DownloadManager {
    private val _progressMap = MutableStateFlow<Map<String, Float>>(emptyMap())
    val progressMap: StateFlow<Map<String, Float>> = _progressMap.asStateFlow()

    fun updateProgress(id: String, progress: Float) {
        _progressMap.update { it + (id to progress) }
    }
    
    fun removeProgress(id: String) {
        _progressMap.update { it - id }
    }
}


class DownloadService : Service() {
    companion object {
        const val CHANNEL_ID = "yt_downloader_foreground"
        const val NOTIFICATION_ID_BASE = 1010
        const val ACTION_START = "ACTION_START"
        const val ACTION_STOP_DOWNLOAD = "ACTION_STOP_DOWNLOAD"
        const val ACTION_CHECK_QUEUE = "ACTION_CHECK_QUEUE"
        const val EXTRA_DOWNLOAD_ID = "EXTRA_DOWNLOAD_ID"
    }

    private val serviceScope = CoroutineScope(Dispatchers.IO + Job())
    private val activeDownloads = ConcurrentHashMap<String, Job>()
    private val pendingDownloads = java.util.concurrent.ConcurrentLinkedQueue<String>()

    private fun checkQueue() {
        val max = DownloadRepository.appConfig.maxConcurrentDownloads
        synchronized(this) {
            while (activeDownloads.size < max) {
                val nextId = pendingDownloads.poll() ?: break
                val job = serviceScope.launch {
                    processDownload(nextId)
                }
                activeDownloads[nextId] = job
            }
        }
    }
    
    // To ensure foreground status
    private var isForeground = false

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val action = intent?.action
        val downloadId = intent?.getStringExtra(EXTRA_DOWNLOAD_ID)

        if (action == ACTION_START && downloadId != null) {
            val item = DownloadRepository.getDownload(downloadId)
            if (item != null) {
                if (!isForeground) {
                    startForeground(NOTIFICATION_ID_BASE, buildProgressNotification("Starting...", "Preparing download", 0f, downloadId))
                    isForeground = true
                }
                if (!pendingDownloads.contains(downloadId) && !activeDownloads.containsKey(downloadId)) {
                    pendingDownloads.add(downloadId)
                }
                checkQueue()
            }
        } else if (action == ACTION_STOP_DOWNLOAD && downloadId != null) {
            pendingDownloads.remove(downloadId)
            activeDownloads[downloadId]?.cancel()
            activeDownloads.remove(downloadId)
            cancelProgressNotification(downloadId)
            
            checkQueue()
            
            // If no active downloads, stop foreground
            if (activeDownloads.isEmpty() && pendingDownloads.isEmpty()) {
                stopForeground(STOP_FOREGROUND_REMOVE)
                isForeground = false
                stopSelf()
        }

        } else if (action == ACTION_CHECK_QUEUE) {
            checkQueue()
        }

        return START_NOT_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null
    
    override fun onDestroy() {
        super.onDestroy()
        activeDownloads.values.forEach { it.cancel() }
        activeDownloads.clear()
    }

    private suspend fun processDownload(id: String) {
        var tmpDir: File? = null
        try {
            val item = DownloadRepository.getDownload(id) ?: return
            DownloadRepository.updateQueue { q -> q.map { if (it.id == id) it.copy(status = "Downloading") else it } }

            val app = applicationContext
            val saveDirStr = DownloadRepository.appConfig.saveDirectory
            var saveDirDoc: androidx.documentfile.provider.DocumentFile? = null
            val subfolder = if (item.settings.audioOnly) "Music" else "Videos"

            if (saveDirStr == "Default") {
                val defaultBase = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), "YT Downloader")
                if (!defaultBase.exists()) defaultBase.mkdirs()
                val baseDoc = androidx.documentfile.provider.DocumentFile.fromFile(defaultBase)
                var found = baseDoc.findFile(subfolder)
                if (found == null) found = baseDoc.createDirectory(subfolder)
                saveDirDoc = found
            } else if (saveDirStr.startsWith("content://")) {
                val baseDoc = androidx.documentfile.provider.DocumentFile.fromTreeUri(app, android.net.Uri.parse(saveDirStr))
                if (baseDoc != null) {
                    var found = baseDoc.findFile(subfolder)
                    if (found == null) found = baseDoc.createDirectory(subfolder)
                    saveDirDoc = found
                }
            } else {
                val customFile = File(saveDirStr)
                if (!customFile.exists()) customFile.mkdirs()
                val baseDoc = androidx.documentfile.provider.DocumentFile.fromFile(customFile)
                var found = baseDoc.findFile(subfolder)
                if (found == null) found = baseDoc.createDirectory(subfolder)
                saveDirDoc = found
            }

            val request = YoutubeDLRequest(item.url)
            tmpDir = File(app.cacheDir, "yt_tmp_$id")
            if (!tmpDir.exists()) tmpDir.mkdirs()
            request.addOption("-P", tmpDir.absolutePath)

            if (item.isPlaylist) {
                request.addOption("--yes-playlist")
            } else {
                request.addOption("--no-playlist")
            }

            request.addOption("-o", "%(title)s.%(ext)s")

            if (item.settings.audioOnly) {
                request.addOption("-x")
                request.addOption("--audio-format", item.settings.saveFormat)
                if (item.settings.saveFormat == "mp3") {
                    request.addOption("--audio-quality", "0")
                }
                if (item.settings.customFormatId != null && !item.isPlaylist) {
                    request.addOption("-f", item.settings.customFormatId!!)
                } else {
                    request.addOption("-f", "bestaudio")
                }
            } else {
                if (item.isPlaylist && item.settings.selectedHeight > 0) {
                    request.addOption("-f", "bestvideo[height<=${item.settings.selectedHeight}]+bestaudio/best")
                } else if (item.settings.customFormatId != null) {
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
            
            withContext(Dispatchers.IO) {
                YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->
                    val speed = if (etaInSeconds > 0) "ETA: ${etaInSeconds}s" else ""
                    
                    var newIndex = -1
                    var newTotal = -1
                    var newTitle: String? = null

                    val matchPlaylist = Regex("""\[download\] Downloading (?:video|item) (\d+) of (\d+)""").find(line)
                    if (matchPlaylist != null) {
                        newIndex = matchPlaylist.groupValues[1].toInt()
                        newTotal = matchPlaylist.groupValues[2].toInt()
                    }

                    if (line.contains("[download] Destination: ")) {
                        val dest = line.substringAfter("[download] Destination: ")
                        newTitle = File(dest).nameWithoutExtension
                    } else if (line.contains("has already been downloaded")) {
                        val dest = line.substringAfter("[download] ").substringBefore(" has already been")
                        newTitle = File(dest).nameWithoutExtension
                    }
                    
                    DownloadRepository.updateQueue { q ->
                        q.map {
                            if (it.id == id && it.status != "Cancelled" && it.status != "Paused") {
                                val currentIndex = if (newIndex != -1) newIndex else it.currentItemIndex
                                val total = if (newTotal != -1) newTotal else it.totalItems
                                val activeTitle = newTitle ?: it.currentDownloadingTitle

                                val isNewItem = currentIndex > it.currentItemIndex
                                val hasProgress = line.contains("[download]") && line.contains("%")
                                
                                val effectiveItemProgress = if (isNewItem) {
                                    if (hasProgress) progress else 0f
                                } else {
                                    if (hasProgress) progress else it.currentItemProgress
                                }

                                val calculatedGlobalProgress = if (it.isPlaylist && total > 0 && currentIndex > 0) {
                                    (((currentIndex - 1).toFloat() * 100f) + effectiveItemProgress) / total.toFloat()
                                } else {
                                    effectiveItemProgress
                                }
                                
                                // yt-dlp often downloads video and audio as separate streams, causing progress to drop from 100% back to 0% mid-download.
                                // We use Math.max to prevent the progress bars from bouncing backwards.
                                val finalGlobalProgress = if (calculatedGlobalProgress < it.progress && !isNewItem) {
                                    it.progress
                                } else {
                                    calculatedGlobalProgress
                                }
                                
                                val finalItemProgress = if (effectiveItemProgress < it.currentItemProgress && !isNewItem) {
                                    it.currentItemProgress
                                } else {
                                    effectiveItemProgress
                                }

                                DownloadManager.updateProgress(id, finalItemProgress)
                                it.copy(
                                    progress = finalGlobalProgress,
                                    downloadSpeed = speed,
                                    currentItemIndex = currentIndex,
                                    totalItems = total,
                                    currentDownloadingTitle = activeTitle,
                                    currentItemProgress = finalItemProgress
                                )
                            } else it
                        }
                    }

                    val currentQ = DownloadRepository.getDownload(id)
                    if (currentQ != null && currentQ.status != "Cancelled" && currentQ.status != "Paused") {
                        val notifTitle = if (currentQ.isPlaylist && currentQ.currentDownloadingTitle.isNotEmpty()) "Downloading ${currentQ.currentDownloadingTitle}" else "Downloading ${currentQ.title}"
                        showProgressNotification(notifTitle, "${currentQ.progress.toInt()}%", currentQ.progress, id)
                    }
                }
            }

            if (DownloadRepository.getDownload(id)?.status == "Cancelled") {
                tmpDir.deleteRecursively()
                return
            }
            DownloadRepository.updateQueue { q -> q.map { if (it.id == id) it.copy(status = "Finishing") else it } }
            showProgressNotification("Finishing: ${item.title}", "Merging and saving file...", 100f, id)

            var finalFileUri: String? = null
            tmpDir.walkTopDown().filter { it.isFile }.forEach { file ->
                if (!file.name.endsWith(".part") && !file.name.endsWith(".ytdl")) {
                    var targetDoc = saveDirDoc
                    if (item.isPlaylist && targetDoc != null) {
                        val safePlaylistTitle = item.title.replace(Regex("[\\\\/:*?\"<>|]"), "_")
                        var playlistSubDoc = targetDoc.findFile(safePlaylistTitle)
                        if (playlistSubDoc == null) {
                            playlistSubDoc = targetDoc.createDirectory(safePlaylistTitle)
                        }
                        targetDoc = playlistSubDoc
                    }

                    if (targetDoc != null) {
                        var finalDoc = targetDoc.findFile(file.name)
                        var counter = 1
                        var finalName = file.name
                        while (finalDoc != null) {
                            finalName = "${file.nameWithoutExtension} ($counter).${file.extension}"
                            finalDoc = targetDoc.findFile(finalName)
                            counter++
                        }

                        val mime = if (item.settings.audioOnly) "audio/*" else "video/*"
                        val newFileDoc = targetDoc.createFile(mime, finalName)
                        if (newFileDoc != null) {
                            app.contentResolver.openOutputStream(newFileDoc.uri)?.use { outStream ->
                                file.inputStream().use { inStream ->
                                    inStream.copyTo(outStream)
                                }
                            }
                            finalFileUri = newFileDoc.uri.toString()
                        }
                    }
                }
            }

            tmpDir.deleteRecursively()
            DownloadRepository.updateQueue { q ->
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 100f, downloadSpeed = "Done", localFilePath = finalFileUri) else it }
            }
            try {
                val historyFile = File(app.filesDir, "history.log")
                val dateStr = java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(java.util.Date())
                historyFile.appendText("[$dateStr] Completed: ${item.title}\n")
            } catch (e: Exception) {}
            cancelProgressNotification(id)
            DownloadManager.removeProgress(id)
            showCompletionNotification("Completed: ${item.title}", "Download finished.", id)

        } catch (e: Exception) {
            tmpDir?.deleteRecursively()
            cancelProgressNotification(id)
            DownloadManager.removeProgress(id)
            val currentStatus = DownloadRepository.getDownload(id)?.status
            if (currentStatus != "Cancelled" && currentStatus != "Paused") {
                val errorMsg = e.message ?: "Unknown error"
                DownloadRepository.updateQueue { q ->
                    q.map { if (it.id == id) it.copy(status = "Error", progress = 0f, downloadSpeed = "", errorMessage = errorMsg) else it }
                }
                val title = DownloadRepository.getDownload(id)?.title ?: "Download"
                showCompletionNotification("Error: $title", errorMsg, id)
            }
        } finally {
            activeDownloads.remove(id)
            checkQueue()
            if (activeDownloads.isEmpty() && pendingDownloads.isEmpty()) {
                stopForeground(STOP_FOREGROUND_REMOVE)
                isForeground = false
                stopSelf()
            }
        }
    }

    private fun getPendingIntent(): PendingIntent {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        val flags = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        } else {
            PendingIntent.FLAG_UPDATE_CURRENT
        }
        return PendingIntent.getActivity(this, 0, intent, flags)
    }

    private fun buildProgressNotification(title: String, desc: String, progress: Float, downloadId: String): Notification {
        val remoteViews = RemoteViews(packageName, R.layout.notification_progress).apply {
            setTextViewText(R.id.notification_title, title)
            setTextViewText(R.id.notification_desc, desc)
            setProgressBar(R.id.notification_progress_bar, 100, progress.toInt(), false)
            
            val cancelIntent = Intent(this@DownloadService, DownloadService::class.java).apply {
                action = ACTION_STOP_DOWNLOAD
                putExtra(EXTRA_DOWNLOAD_ID, downloadId)
            }
            val cancelPendingIntent = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                PendingIntent.getForegroundService(this@DownloadService, downloadId.hashCode(), cancelIntent, PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)
            } else {
                PendingIntent.getService(this@DownloadService, downloadId.hashCode(), cancelIntent, PendingIntent.FLAG_UPDATE_CURRENT)
            }
            setOnClickPendingIntent(R.id.notification_cancel_btn, cancelPendingIntent)
        }
        
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setCustomContentView(remoteViews)
            .setStyle(NotificationCompat.DecoratedCustomViewStyle())
            .setOngoing(true)
            .setOnlyAlertOnce(true)
            .setContentIntent(getPendingIntent())
            .build()
    }

    private fun showProgressNotification(title: String, desc: String, progress: Float, downloadId: String) {
        val notificationId = NOTIFICATION_ID_BASE + Math.abs(downloadId.hashCode() % 10000)
        val notification = buildProgressNotification(title, desc, progress, downloadId)
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.notify(notificationId, notification)
    }

    private fun showCompletionNotification(title: String, desc: String, downloadId: String) {
        if (!DownloadRepository.appConfig.notifyOnComplete) return
        val notificationId = NOTIFICATION_ID_BASE + Math.abs(downloadId.hashCode() % 10000)
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(title)
            .setContentText(desc)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setAutoCancel(true)
            .setContentIntent(getPendingIntent())
            .build()
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.notify(notificationId, notification)
    }

    private fun cancelProgressNotification(downloadId: String) {
        val notificationId = NOTIFICATION_ID_BASE + Math.abs(downloadId.hashCode() % 10000)
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.cancel(notificationId)
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Foreground Downloads",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager?.createNotificationChannel(channel)
        }
    }
}
