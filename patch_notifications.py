import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target_show_notif = """    private fun showNotification(title: String, content: String) {
        val notificationManager = 
            getApplication<Application>().getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        
        val notification = NotificationCompat.Builder(getApplication(), "DOWNLOAD_CHANNEL")
            .setSmallIcon(android.R.drawable.stat_sys_download_done)
            .setContentTitle(title)
            .setContentText(content)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true)
            .build()
            
        notificationManager.notify(UUID.randomUUID().hashCode(), notification)
    }"""

replacement_show_notif = """    private fun showNotification(title: String, content: String, notificationId: Int = UUID.randomUUID().hashCode()) {
        val notificationManager = 
            getApplication<Application>().getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        
        val notification = NotificationCompat.Builder(getApplication(), "DOWNLOAD_CHANNEL")
            .setSmallIcon(android.R.drawable.stat_sys_download_done)
            .setContentTitle(title)
            .setContentText(content)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true)
            .build()
            
        notificationManager.notify(notificationId, notification)
    }
    
    private fun updateNotificationProgress(id: String, title: String, progress: Float, speed: String) {
        val notificationManager = 
            getApplication<Application>().getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            
        val notificationId = id.hashCode()
        
        val notification = NotificationCompat.Builder(getApplication(), "DOWNLOAD_CHANNEL")
            .setSmallIcon(android.R.drawable.stat_sys_download)
            .setContentTitle(title)
            .setContentText(speed)
            .setProgress(100, (progress * 100).toInt(), false)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOnlyAlertOnce(true)
            .setOngoing(true)
            .build()
            
        notificationManager.notify(notificationId, notification)
    }
    
    private fun logError(error: String) {
        try {
            val file = File(getApplication<Application>().filesDir, "error_log.txt")
            file.appendText("${System.currentTimeMillis()}: $error\n")
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }"""

content = content.replace(target_show_notif, replacement_show_notif)

target_ytdlp_execute = """                YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->
                    var currentStatus = _downloadQueue.value.find { it.id == id }?.status
                    if (currentStatus == "Cancelled") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else if (currentStatus == "Paused") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else {
                        val speedStr = if (etaInSeconds > 0) "${etaInSeconds}s left" else ""
                        _downloadQueue.update { q -> 
                            q.map { if (it.id == id) it.copy(progress = progress / 100f, downloadSpeed = speedStr) else it } 
                        }
                    }
                }"""

replacement_ytdlp_execute = """                YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->
                    var currentStatus = _downloadQueue.value.find { it.id == id }?.status
                    if (currentStatus == "Cancelled") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else if (currentStatus == "Paused") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else {
                        val speedStr = if (etaInSeconds > 0) "${etaInSeconds}s left" else ""
                        _downloadQueue.update { q -> 
                            q.map { if (it.id == id) it.copy(progress = progress / 100f, downloadSpeed = speedStr) else it } 
                        }
                        updateNotificationProgress(id, titleStr, progress / 100f, speedStr)
                    }
                }"""

content = content.replace(target_ytdlp_execute, replacement_ytdlp_execute)

target_completed = """            showNotification("$typeStr Download Complete", "$titleStr has finished downloading.")"""
replacement_completed = """            showNotification("$typeStr Download Complete", "$titleStr has finished downloading.", id.hashCode())"""
content = content.replace(target_completed, replacement_completed)

target_catch = """                val errorMsg = e.message ?: e.cause?.message ?: "Unknown error occurred"
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id) it.copy(status = "Error", progress = 0f, downloadSpeed = "", errorMessage = errorMsg) else it } 
                }
                val item = _downloadQueue.value.find { it.id == id }
                val typeStr = if (item?.isPlaylist == true) "Playlist" else "Video"
                showNotification("$typeStr Download Failed", "${item?.title} encountered an error.")"""
replacement_catch = """                val errorMsg = e.message ?: e.cause?.message ?: "Unknown error occurred"
                logError(errorMsg)
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id) it.copy(status = "Error", progress = 0f, downloadSpeed = "", errorMessage = errorMsg) else it } 
                }
                val item = _downloadQueue.value.find { it.id == id }
                val typeStr = if (item?.isPlaylist == true) "Playlist" else "Video"
                showNotification("$typeStr Download Failed", "${item?.title} encountered an error: $errorMsg", id.hashCode())"""
content = content.replace(target_catch, replacement_catch)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)

