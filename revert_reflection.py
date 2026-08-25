import re

with open("app/src/main/java/com/aistudio/ytdownloader/YTDownloaderApp.kt", "r") as f:
    content = f.read()

target = '''            // Fix ffmpeg location for yt-dlp
            try {
                var ffmpegDir = java.io.File(this.noBackupFilesDir, "youtubedl-android/packages/ffmpeg/usr/bin")
                if (!ffmpegDir.exists()) {
                    ffmpegDir = java.io.File(this.noBackupFilesDir, "youtubedl-android/packages/ffmpeg")
                }
                val field = YoutubeDL::class.java.getDeclaredField("ffmpegPath")
                field.isAccessible = true
                field.set(null, ffmpegDir)
            } catch (e: Exception) {
                e.printStackTrace()
            }'''

content = content.replace(target, '')

with open("app/src/main/java/com/aistudio/ytdownloader/YTDownloaderApp.kt", "w") as f:
    f.write(content)
