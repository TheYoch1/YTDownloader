import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# 1. Update the yt-dlp -o parameter back to a flat structure
old_o = """            if (item.isPlaylist) {
                request.addOption("-o", "%(playlist_title)s/%(title)s.%(ext)s")
            } else {
                request.addOption("-o", "%(title)s.%(ext)s")
            }"""
new_o = """            request.addOption("-o", "%(title)s.%(ext)s")"""
text = text.replace(old_o, new_o)

# 2. Update the folder creation to explicitly use item.title
old_subdoc = """                    if (item.isPlaylist && targetDoc != null) {
                        val playlistTitle = file.parentFile?.name ?: "Unknown Playlist"
                        val safePlaylistTitle = playlistTitle.replace(Regex("[\\\\/:*?\\"<>|]"), "_")
                        var playlistSubDoc = targetDoc.findFile(safePlaylistTitle)
                        if (playlistSubDoc == null) {
                            playlistSubDoc = targetDoc.createDirectory(safePlaylistTitle)
                        }
                        targetDoc = playlistSubDoc
                    }"""

new_subdoc = """                    if (item.isPlaylist && targetDoc != null) {
                        val safePlaylistTitle = item.title.replace(Regex("[\\\\/:*?\\"<>|]"), "_")
                        var playlistSubDoc = targetDoc.findFile(safePlaylistTitle)
                        if (playlistSubDoc == null) {
                            playlistSubDoc = targetDoc.createDirectory(safePlaylistTitle)
                        }
                        targetDoc = playlistSubDoc
                    }"""

text = text.replace(old_subdoc, new_subdoc)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
