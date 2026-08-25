import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = """                // Let FFmpeg library handle its own location.
                // The junkfood02 fork sets ffmpeg location internally when initialized.
                // We also add the youtube:player_client workaround to fix 360p throttling
                request.addOption("--extractor-args", "youtube:player_client=android,web")"""

replacement = """                // We add the youtube:player_client workaround to fix 360p throttling
                request.addOption("--extractor-args", "youtube:player_client=android,web")
                
                // Use the explicit JNI wrapper for FFmpeg on Android 10+ (API 29+)
                val nativeLibDir = getApplication<Application>().applicationInfo.nativeLibraryDir
                val libFfmpeg = java.io.File(nativeLibDir, "libffmpeg.so")
                if (libFfmpeg.exists()) {
                    request.addOption("--ffmpeg-location", libFfmpeg.absolutePath)
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
