import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# 1. Add notification methods and state
notification_methods = """
    private var lastNotificationTime = 0L

    private fun getPendingIntent(): android.app.PendingIntent {
        val app = getApplication<Application>()
        val intent = android.content.Intent(app, MainActivity::class.java).apply {
            flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        val flags = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            android.app.PendingIntent.FLAG_IMMUTABLE or android.app.PendingIntent.FLAG_UPDATE_CURRENT
        } else {
            android.app.PendingIntent.FLAG_UPDATE_CURRENT
        }
        return android.app.PendingIntent.getActivity(app, 0, intent, flags)
    }

    private fun showProgressNotification(title: String, desc: String, progress: Float, id: Int, pendingIntent: android.app.PendingIntent?) {
        val currentTime = System.currentTimeMillis()
        if (currentTime - lastNotificationTime < 1000 && progress < 100f) return
        lastNotificationTime = currentTime

        val app = getApplication<Application>()
        val manager = app.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel("downloads_progress", "Downloads Progress", NotificationManager.IMPORTANCE_LOW)
            manager.createNotificationChannel(channel)
        }
        val builder = NotificationCompat.Builder(app, "downloads_progress")
            .setSmallIcon(android.R.drawable.stat_sys_download)
            .setContentTitle(title)
            .setContentText(desc)
            .setProgress(100, progress.toInt(), false)
            .setOngoing(true)
            .setOnlyAlertOnce(true)
            .setAutoCancel(false)
        
        if (pendingIntent != null) builder.setContentIntent(pendingIntent)
        manager.notify(id, builder.build())
    }

    private fun cancelProgressNotification(id: Int) {
        val app = getApplication<Application>()
        val manager = app.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.cancel(id)
    }
"""

# Replace showNotification with our new setup
old_show_notification = """    private fun showNotification(title: String, desc: String, id: Int, pendingIntent: android.app.PendingIntent?) {
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
    }"""

text = text.replace(old_show_notification, old_show_notification + notification_methods)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
