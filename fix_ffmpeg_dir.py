import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                val request = YoutubeDLRequest(url)
                request.addOption("--extractor-args", "youtube:player_client=android,web")'''

rep = '''                val request = YoutubeDLRequest(url)
                
                // Find ffmpeg
                val packagesDir = java.io.File(application.noBackupFilesDir, "youtubedl-android/packages")
                val ffmpegUsrBin = java.io.File(packagesDir, "ffmpeg/usr/bin")
                if (ffmpegUsrBin.exists()) {
                    request.addOption("--ffmpeg-location", ffmpegUsrBin.absolutePath)
                } else {
                    val ffmpegBase = java.io.File(packagesDir, "ffmpeg")
                    if (ffmpegBase.exists()) {
                        request.addOption("--ffmpeg-location", ffmpegBase.absolutePath)
                    }
                }
                
                request.addOption("--extractor-args", "youtube:player_client=android,web")'''
                
content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
