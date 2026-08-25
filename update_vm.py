import re

with open("/app/applet/app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                // Point yt-dlp to our newly extracted FFmpeg
                val internalFfmpeg = java.io.File(application.filesDir, "ffmpeg")
                if (internalFfmpeg.exists()) {
                    request.addOption("--ffmpeg-location", internalFfmpeg.absolutePath)
                }'''

rep = '''                // Use the native library directory (Android 10+ secure approach)
                val nativeDir = application.applicationInfo.nativeLibraryDir
                val nativeFfmpeg = java.io.File(nativeDir, "libffmpeg.so")
                if (nativeFfmpeg.exists()) {
                    request.addOption("--ffmpeg-location", nativeFfmpeg.absolutePath)
                }'''

content = content.replace(target, rep)

with open("/app/applet/app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
