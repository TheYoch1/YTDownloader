with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

# 1. Update Title
old_title = """                    Text(
                        text = download.title,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1
                    )"""

new_title = """                    Text(
                        text = if (download.isPlaylist && download.currentDownloadingTitle.isNotEmpty() && download.status == "Downloading") download.currentDownloadingTitle else download.title,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1
                    )"""
text = text.replace(old_title, new_title)

# 2. Update Format Label
old_format = """                    Text(
                        text = if (download.settings.audioOnly) "Format: Audio (MP3)" else "Format: Video (${download.settings.quality.label})",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.primary
                    )"""

new_format = """                    Text(
                        text = if (download.settings.formatLabel.isNotEmpty()) "Format: ${download.settings.formatLabel}" else if (download.settings.audioOnly) "Format: Audio (MP3)" else "Format: Video (${download.settings.quality.label})",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.primary
                    )"""
text = text.replace(old_format, new_format)

# 3. Update Progress Text
old_prog_text = """                val progressText = if (download.isPlaylist && download.totalItems > 0 && download.status == "Downloading") {
                    "${download.progress.toInt()}% Overall (${download.currentItemProgress.toInt()}% file)"
                } else {
                    "${download.progress.toInt()}%"
                }"""

new_prog_text = """                val progressText = if (download.isPlaylist && download.status == "Downloading") {
                    "${download.currentItemProgress.toInt()}%"
                } else {
                    "${download.progress.toInt()}%"
                }"""
text = text.replace(old_prog_text, new_prog_text)

# 4. Update Progress Bar
old_prog_bar = """                LinearProgressIndicator(
                    progress = { download.progress / 100f },"""

new_prog_bar = """                LinearProgressIndicator(
                    progress = { if (download.isPlaylist && download.status == "Downloading") download.currentItemProgress / 100f else download.progress / 100f },"""
text = text.replace(old_prog_bar, new_prog_bar)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
