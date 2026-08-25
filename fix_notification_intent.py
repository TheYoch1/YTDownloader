import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                val item = _downloadQueue.value.find { it.id == id }
                val typeStr = if (item?.isPlaylist == true) "Playlist" else "Video"
                showNotification("$typeStr Download Failed", "${item?.title} encountered an error: $errorMsg", id.hashCode())'''

rep = '''                val item = _downloadQueue.value.find { it.id == id }
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
                showNotification("$typeStr Download Failed", "${item?.title} encountered an error: $errorMsg", id.hashCode(), pendingIntent)'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
