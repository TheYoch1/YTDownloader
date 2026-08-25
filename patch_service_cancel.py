with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

old_build = """    private fun buildProgressNotification(title: String, desc: String, progress: Float, downloadId: String): Notification {
        val remoteViews = RemoteViews(packageName, R.layout.notification_progress).apply {
            setTextViewText(R.id.notification_title, title)
            setTextViewText(R.id.notification_desc, desc)
            setProgressBar(R.id.notification_progress_bar, 100, progress.toInt(), false)
        }
        
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setCustomContentView(remoteViews)
            .setStyle(NotificationCompat.DecoratedCustomViewStyle())
            .setOngoing(true)
            .setOnlyAlertOnce(true)
            .setContentIntent(getPendingIntent())
            .build()
    }"""

new_build = """    private fun buildProgressNotification(title: String, desc: String, progress: Float, downloadId: String): Notification {
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
    }"""

text = text.replace(old_build, new_build)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)

