import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = """            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 1f, downloadSpeed = "", localFilePath = savedFileUri) else it } 
            }
            
            val typeStr = if (isPlaylist) "Playlist" else "Video\""""

rep = """            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 1f, downloadSpeed = "", localFilePath = savedFileUri) else it } 
            }
            
            try {
                val historyFile = java.io.File(application.filesDir, "history.log")
                val date = java.text.SimpleDateFormat("yyyy-MM-dd HH:mm", java.util.Locale.getDefault()).format(java.util.Date())
                historyFile.appendText("$date|${if(isPlaylist) "Playlist" else "Video"}|$titleStr\\n")
            } catch (e: Exception) { }
            
            val typeStr = if (isPlaylist) "Playlist" else "Video\""""

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
