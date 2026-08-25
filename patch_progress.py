with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

old_text = """                val progressText = if (download.isPlaylist && download.status == "Downloading") {
                    "${download.currentItemProgress.toInt()}%"
                } else {
                    "${download.progress.toInt()}%"
                }"""
new_text = """                val progressText = if (download.isPlaylist && download.totalItems > 0 && download.status == "Downloading") {
                    "${download.progress.toInt()}% Overall (${download.currentItemProgress.toInt()}% file)"
                } else {
                    "${download.progress.toInt()}%"
                }"""
text = text.replace(old_text, new_text)

old_bar = """                LinearProgressIndicator(
                    progress = { if (download.isPlaylist && download.status == "Downloading") download.currentItemProgress / 100f else download.progress / 100f },"""
new_bar = """                LinearProgressIndicator(
                    progress = { download.progress / 100f },"""
text = text.replace(old_bar, new_bar)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
