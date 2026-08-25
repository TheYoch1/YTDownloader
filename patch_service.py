with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

old = """                                val globalProgress = if (it.isPlaylist && total > 0 && currentIndex > 0) {
                                    (((currentIndex - 1).toFloat() * 100f) + progress) / total.toFloat()
                                } else {
                                    progress
                                }

                                it.copy(
                                    progress = globalProgress,
                                    downloadSpeed = speed,
                                    currentItemIndex = currentIndex,
                                    totalItems = total,
                                    currentDownloadingTitle = activeTitle,
                                    currentItemProgress = progress
                                )"""

new = """                                val calculatedGlobalProgress = if (it.isPlaylist && total > 0 && currentIndex > 0) {
                                    (((currentIndex - 1).toFloat() * 100f) + progress) / total.toFloat()
                                } else {
                                    progress
                                }
                                
                                // yt-dlp often downloads video and audio as separate streams, causing progress to drop from 100% back to 0% mid-download.
                                // We use Math.max to prevent the progress bars from bouncing backwards.
                                val finalGlobalProgress = if (calculatedGlobalProgress < it.progress && currentIndex == it.currentItemIndex) {
                                    it.progress
                                } else {
                                    calculatedGlobalProgress
                                }
                                
                                val finalItemProgress = if (progress < it.currentItemProgress && currentIndex == it.currentItemIndex) {
                                    it.currentItemProgress
                                } else {
                                    progress
                                }

                                it.copy(
                                    progress = finalGlobalProgress,
                                    downloadSpeed = speed,
                                    currentItemIndex = currentIndex,
                                    totalItems = total,
                                    currentDownloadingTitle = activeTitle,
                                    currentItemProgress = finalItemProgress
                                )"""

text = text.replace(old, new)
with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)
print("Service patched")
