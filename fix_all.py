import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Fix Video location
text = text.replace(
    'val saveDir = if (item.settings.audioOnly) File(baseDir, "Music") else File(baseDir, "Video")',
    'val saveDir = if (item.settings.audioOnly) File(baseDir, "Music") else File(baseDir, "Videos")'
)

# Fix File copying for playlists
old_copy = """            var downloadedFile: File? = null
            tmpDir.listFiles()?.forEach { file ->
                if (!file.name.endsWith(".part") && !file.name.endsWith(".ytdl")) {
                    downloadedFile = file
                }
            }
            
            var finalFileUri: String? = null
            if (downloadedFile != null) {
                val destFile = File(saveDir, downloadedFile!!.name)
                var actualDest = destFile
                var counter = 1
                while (actualDest.exists()) {
                    val nameWithoutExt = downloadedFile!!.nameWithoutExtension
                    val ext = downloadedFile!!.extension
                    actualDest = File(saveDir, "${nameWithoutExt}_$counter.$ext")
                    counter++
                }
                downloadedFile!!.copyTo(actualDest, overwrite = true)
                finalFileUri = actualDest.absolutePath
            }"""

new_copy = """            var finalFileUri: String? = null
            tmpDir.listFiles()?.forEach { file ->
                if (!file.name.endsWith(".part") && !file.name.endsWith(".ytdl")) {
                    val destFile = File(saveDir, file.name)
                    var actualDest = destFile
                    var counter = 1
                    while (actualDest.exists()) {
                        val nameWithoutExt = file.nameWithoutExtension
                        val ext = file.extension
                        actualDest = File(saveDir, "${nameWithoutExt}_$counter.$ext")
                        counter++
                    }
                    file.copyTo(actualDest, overwrite = true)
                    finalFileUri = actualDest.absolutePath
                }
            }"""

text = text.replace(old_copy, new_copy)

# Fix progress reporting for playlists
old_update = """                _downloadQueue.update { q -> 
                    q.map { 
                        if (it.id == id && it.status != "Cancelled" && it.status != "Paused") {
                            it.copy(
                                progress = progress, 
                                downloadSpeed = speed,
                                currentItemIndex = if (newIndex != -1) newIndex else it.currentItemIndex,
                                totalItems = if (newTotal != -1) newTotal else it.totalItems,
                                currentItemTitle = newTitle ?: it.currentItemTitle
                            )
                        } else it 
                    }
                }"""

new_update = """                _downloadQueue.update { q -> 
                    q.map { 
                        if (it.id == id && it.status != "Cancelled" && it.status != "Paused") {
                            val currentIndex = if (newIndex != -1) newIndex else it.currentItemIndex
                            val total = if (newTotal != -1) newTotal else it.totalItems
                            val activeTitle = newTitle ?: it.currentItemTitle
                            
                            val effectiveProgress = if (it.isPlaylist && total > 0 && currentIndex > 0) {
                                (((currentIndex - 1) * 100f) + progress) / total
                            } else {
                                progress
                            }
                            
                            it.copy(
                                progress = effectiveProgress, 
                                downloadSpeed = speed,
                                currentItemIndex = currentIndex,
                                totalItems = total,
                                currentItemTitle = activeTitle
                            )
                        } else it 
                    }
                }"""

text = text.replace(old_update, new_update)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
