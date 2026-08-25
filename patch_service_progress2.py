with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

old_logic = """                                it.copy(
                                    progress = finalGlobalProgress,
                                    downloadSpeed = speed,
                                    currentItemIndex = currentIndex,
                                    totalItems = total,
                                    currentDownloadingTitle = activeTitle,
                                    currentItemProgress = finalItemProgress
                                )"""

new_logic = """                                DownloadManager.updateProgress(id, finalItemProgress)
                                it.copy(
                                    progress = finalGlobalProgress,
                                    downloadSpeed = speed,
                                    currentItemIndex = currentIndex,
                                    totalItems = total,
                                    currentDownloadingTitle = activeTitle,
                                    currentItemProgress = finalItemProgress
                                )"""

text = text.replace(old_logic, new_logic)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)

