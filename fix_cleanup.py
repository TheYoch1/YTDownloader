import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = """    private fun recordDownloadStats() {
        // Called in finally, can be used for general cleanup if needed. Count is now handled in recordDownloadStatsSize.
    }"""
    
rep = """    private fun recordDownloadStats() {
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
    }"""
content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
