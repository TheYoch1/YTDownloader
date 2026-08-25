import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = """                // Ensure FFmpeg is executable and path is explicitly set
                val ffmpegDir = java.io.File(getApplication<Application>().noBackupFilesDir, "youtubedl-android/packages/ffmpeg")
                if (ffmpegDir.exists() && ffmpegDir.isDirectory) {
                    ffmpegDir.listFiles()?.forEach { it.setExecutable(true) }
                    request.addOption("--ffmpeg-location", ffmpegDir.absolutePath)
                } else {
                    // Try alternate locations just in case
                    val filesDirFfmpeg = java.io.File(getApplication<Application>().filesDir, "ffmpeg")
                    if (filesDirFfmpeg.exists()) {
                        if (filesDirFfmpeg.isDirectory) {
                            filesDirFfmpeg.listFiles()?.forEach { it.setExecutable(true) }
                            request.addOption("--ffmpeg-location", filesDirFfmpeg.absolutePath)
                        } else {
                            filesDirFfmpeg.setExecutable(true)
                            request.addOption("--ffmpeg-location", filesDirFfmpeg.absolutePath)
                        }
                    }
                }"""

# The wrapper is located at:
# context.applicationInfo.nativeLibraryDir + "/libffmpeg.so"
# Because YoutubeDL already adds this exact path to ffmpegPath automatically,
# I don't need to add it again. But just to be 100% sure we don't regress if YoutubeDL doesn't add it,
# I will add it pointing to the nativeLibraryDir wrapper!
rep = """                // Use the explicit JNI wrapper for FFmpeg on Android 10+ (API 29+)
                val nativeLibDir = getApplication<Application>().applicationInfo.nativeLibraryDir
                val libFfmpeg = java.io.File(nativeLibDir, "libffmpeg.so")
                if (libFfmpeg.exists()) {
                    request.addOption("--ffmpeg-location", libFfmpeg.absolutePath)
                }"""

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
