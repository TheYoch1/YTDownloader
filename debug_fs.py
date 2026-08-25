import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                val request = YoutubeDLRequest(url)
                request.addOption("--extractor-args", "youtube:player_client=android,web")'''

rep = '''                val request = YoutubeDLRequest(url)
                
                // Debug FS
                val binDir = java.io.File(application.applicationInfo.nativeLibraryDir)
                val binFiles = binDir.listFiles()?.joinToString { it.name } ?: "null"
                
                request.addOption("--extractor-args", "youtube:player_client=android,web")'''
                
content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
