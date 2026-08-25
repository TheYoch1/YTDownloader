import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Update -o parameter
old_o = 'request.addOption("-o", "%(title)s.%(ext)s")'
new_o = """if (item.isPlaylist) {
                request.addOption("-o", "%(playlist_title)s/%(title)s.%(ext)s")
            } else {
                request.addOption("-o", "%(title)s.%(ext)s")
            }"""
text = text.replace(old_o, new_o)

# Update copy logic to handle subdirectories and remove videoTitle folder creation
old_copy_start = """            var finalFileUri: String? = null
            tmpDir.listFiles()?.forEach { file ->"""

new_copy_start = """            var finalFileUri: String? = null
            tmpDir.walkTopDown().filter { it.isFile }.forEach { file ->"""

text = text.replace(old_copy_start, new_copy_start)

# Update sub-doc logic
old_subdoc = """                    if (item.isPlaylist && targetDoc != null) {
                        val videoTitle = file.nameWithoutExtension.replace(Regex("[\\\\/:*?\\"<>|]"), "_")
                        var playlistSubDoc = targetDoc.findFile(videoTitle)
                        if (playlistSubDoc == null) {
                            playlistSubDoc = targetDoc.createDirectory(videoTitle)
                        }
                        targetDoc = playlistSubDoc
                    }"""

new_subdoc = """                    if (item.isPlaylist && targetDoc != null) {
                        val playlistTitle = file.parentFile?.name ?: "Unknown Playlist"
                        val safePlaylistTitle = playlistTitle.replace(Regex("[\\\\/:*?\\"<>|]"), "_")
                        var playlistSubDoc = targetDoc.findFile(safePlaylistTitle)
                        if (playlistSubDoc == null) {
                            playlistSubDoc = targetDoc.createDirectory(safePlaylistTitle)
                        }
                        targetDoc = playlistSubDoc
                    }"""

text = text.replace(old_subdoc, new_subdoc)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
