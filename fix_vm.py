import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Update path logic
old_path_logic = """            val baseDir = if (_appConfig.value.saveDirectory == "Default") {
                File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), "YT Downloader")
            } else {
                File(_appConfig.value.saveDirectory)
            }
            val saveDir = if (item.settings.audioOnly) File(baseDir, "Music") else File(baseDir, "Videos")
            if (!saveDir.exists()) saveDir.mkdirs()"""

new_path_logic = """            val saveDirStr = _appConfig.value.saveDirectory
            var saveDirDoc: androidx.documentfile.provider.DocumentFile? = null
            val subfolder = if (item.settings.audioOnly) "Music" else "Videos"
            
            if (saveDirStr == "Default") {
                val defaultBase = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), "YT Downloader")
                if (!defaultBase.exists()) defaultBase.mkdirs()
                val baseDoc = androidx.documentfile.provider.DocumentFile.fromFile(defaultBase)
                var found = baseDoc.findFile(subfolder)
                if (found == null) found = baseDoc.createDirectory(subfolder)
                saveDirDoc = found
            } else if (saveDirStr.startsWith("content://")) {
                val baseDoc = androidx.documentfile.provider.DocumentFile.fromTreeUri(app, android.net.Uri.parse(saveDirStr))
                if (baseDoc != null) {
                    var found = baseDoc.findFile(subfolder)
                    if (found == null) found = baseDoc.createDirectory(subfolder)
                    saveDirDoc = found
                }
            } else {
                val customFile = File(saveDirStr)
                if (!customFile.exists()) customFile.mkdirs()
                val baseDoc = androidx.documentfile.provider.DocumentFile.fromFile(customFile)
                var found = baseDoc.findFile(subfolder)
                if (found == null) found = baseDoc.createDirectory(subfolder)
                saveDirDoc = found
            }"""

text = text.replace(old_path_logic, new_path_logic)

# Update progress regex and state logic
old_progress_logic = """                _downloadQueue.update { q -> 
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

new_progress_logic = """                _downloadQueue.update { q -> 
                    q.map { 
                        if (it.id == id && it.status != "Cancelled" && it.status != "Paused") {
                            val currentIndex = if (newIndex != -1) newIndex else it.currentItemIndex
                            val total = if (newTotal != -1) newTotal else it.totalItems
                            val activeTitle = newTitle ?: it.currentItemTitle
                            
                            val globalProgress = if (it.isPlaylist && total > 0 && currentIndex > 0) {
                                ((currentIndex - 1).toFloat() / total.toFloat()) * 100f
                            } else {
                                progress
                            }
                            
                            it.copy(
                                progress = globalProgress, 
                                downloadSpeed = speed,
                                currentItemIndex = currentIndex,
                                totalItems = total,
                                currentItemTitle = activeTitle,
                                currentItemProgress = progress
                            )
                        } else it 
                    }
                }"""
text = text.replace(old_progress_logic, new_progress_logic)

# Update copy logic
old_copy_logic = """            var finalFileUri: String? = null
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

new_copy_logic = """            var finalFileUri: String? = null
            tmpDir.listFiles()?.forEach { file ->
                if (!file.name.endsWith(".part") && !file.name.endsWith(".ytdl")) {
                    var targetDoc = saveDirDoc
                    if (item.isPlaylist && targetDoc != null) {
                        val videoTitle = file.nameWithoutExtension.replace(Regex("[\\\\/:*?\\"<>|]"), "_")
                        var playlistSubDoc = targetDoc.findFile(videoTitle)
                        if (playlistSubDoc == null) {
                            playlistSubDoc = targetDoc.createDirectory(videoTitle)
                        }
                        targetDoc = playlistSubDoc
                    }
                    
                    if (targetDoc != null) {
                        var finalDoc = targetDoc.findFile(file.name)
                        var counter = 1
                        var finalName = file.name
                        while (finalDoc != null) {
                            finalName = "${file.nameWithoutExtension}_$counter.${file.extension}"
                            finalDoc = targetDoc.findFile(finalName)
                            counter++
                        }
                        
                        val mime = if (item.settings.audioOnly) "audio/*" else "video/*"
                        val newFileDoc = targetDoc.createFile(mime, finalName)
                        if (newFileDoc != null) {
                            app.contentResolver.openOutputStream(newFileDoc.uri)?.use { outStream ->
                                file.inputStream().use { inStream ->
                                    inStream.copyTo(outStream)
                                }
                            }
                            finalFileUri = newFileDoc.uri.toString()
                        }
                    }
                }
            }"""

text = text.replace(old_copy_logic, new_copy_logic)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
