with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

import_code = "import android.widget.RemoteViews"
if import_code not in text:
    text = text.replace("import android.os.IBinder", "import android.os.IBinder\nimport android.widget.RemoteViews")

old_build = """    private fun buildProgressNotification(title: String, desc: String, progress: Float, downloadId: String): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(title)
            .setContentText(desc)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setProgress(100, progress.toInt(), false)
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

