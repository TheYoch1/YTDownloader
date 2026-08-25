import re

with open("app/src/main/java/com/aistudio/ytdownloader/YTDownloaderApp.kt", "r") as f:
    content = f.read()

target = '''                val ffmpegDir = java.io.File(this.noBackupFilesDir, "youtubedl-android/packages/ffmpeg")
                val field = YoutubeDL::class.java.getDeclaredField("ffmpegPath")'''

rep = '''                var ffmpegDir = java.io.File(this.noBackupFilesDir, "youtubedl-android/packages/ffmpeg/usr/bin")
                if (!ffmpegDir.exists()) {
                    ffmpegDir = java.io.File(this.noBackupFilesDir, "youtubedl-android/packages/ffmpeg")
                }
                val field = YoutubeDL::class.java.getDeclaredField("ffmpegPath")'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/YTDownloaderApp.kt", "w") as f:
    f.write(content)
