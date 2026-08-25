import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''    private fun updateNotificationProgress(id: String, title: String, progress: Float, speed: String) {
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
    }'''

rep = '''    private fun updateNotificationProgress(id: String, title: String, progress: Float, speed: String) {
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
    }'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
print("done func")
