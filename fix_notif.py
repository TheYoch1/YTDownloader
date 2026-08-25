with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

old_notif = """                    val currentQ = DownloadRepository.getDownload(id)
                    if (currentQ != null && currentQ.status != "Cancelled" && currentQ.status != "Paused") {
                        showProgressNotification("Downloading ${currentQ.title}", "${currentQ.progress.toInt()}%", currentQ.progress, id)
                    }"""

new_notif = """                    val currentQ = DownloadRepository.getDownload(id)
                    if (currentQ != null && currentQ.status != "Cancelled" && currentQ.status != "Paused") {
                        val notifTitle = if (currentQ.isPlaylist && currentQ.currentDownloadingTitle.isNotEmpty()) "Downloading ${currentQ.currentDownloadingTitle}" else "Downloading ${currentQ.title}"
                        showProgressNotification(notifTitle, "${currentQ.progress.toInt()}%", currentQ.progress, id)
                    }"""
text = text.replace(old_notif, new_notif)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)
