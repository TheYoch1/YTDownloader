import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                val ffmpegDir = java.io.File(application.noBackupFilesDir, "youtubedl-android/packages/ffmpeg")
                if (ffmpegDir.exists()) {
                    request.addOption("--ffmpeg-location", ffmpegDir.absolutePath)
                }
'''

content = content.replace(target, '')

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
