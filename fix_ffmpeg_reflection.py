import re

with open("app/src/main/java/com/aistudio/ytdownloader/YTDownloaderApp.kt", "r") as f:
    content = f.read()

target = '''            NetworkMonitor.initialize(this)
            FFmpeg.getInstance().init(this)'''

rep = '''            NetworkMonitor.initialize(this)
            FFmpeg.getInstance().init(this)
            
            // Fix ffmpeg location for yt-dlp
            try {
                val ffmpegDir = java.io.File(this.noBackupFilesDir, "youtubedl-android/packages/ffmpeg")
                val field = YoutubeDL::class.java.getDeclaredField("ffmpegPath")
                field.isAccessible = true
                field.set(null, ffmpegDir)
            } catch (e: Exception) {
                e.printStackTrace()
            }'''
            
content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/YTDownloaderApp.kt", "w") as f:
    f.write(content)
