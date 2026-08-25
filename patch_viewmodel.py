import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = """                        var docFile = DocumentFile.fromTreeUri(application, treeUri)
                        if (isPlaylist && docFile != null) {"""

replacement = """                        var docFile = DocumentFile.fromTreeUri(application, treeUri)
                        
                        if (docFile != null && docFile.name != "YT Downloader") {
                            var ytFolder = docFile.findFile("YT Downloader")
                            if (ytFolder == null) {
                                ytFolder = docFile.createDirectory("YT Downloader")
                            }
                            if (ytFolder != null) docFile = ytFolder
                        }
                        
                        if (isPlaylist && docFile != null) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
