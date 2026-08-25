import re
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

# Update the progress percentage text
old_text_progress = """                Text(
                    text = "${download.progress.toInt()}%",
                    style = MaterialTheme.typography.bodySmall,
                    fontWeight = FontWeight.Bold
                )"""
new_text_progress = """                val progressText = if (download.isPlaylist && download.totalItems > 0 && download.status == "Downloading") {
                    "${download.progress.toInt()}% Overall (${download.currentItemProgress.toInt()}% file)"
                } else {
                    "${download.progress.toInt()}%"
                }
                
                Text(
                    text = progressText,
                    style = MaterialTheme.typography.bodySmall,
                    fontWeight = FontWeight.Bold
                )"""

text = text.replace(old_text_progress, new_text_progress)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
