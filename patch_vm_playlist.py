import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

# 1. Update fetchAvailableQualities to skip quality check for playlists or handle them gracefully
target_fetch = """    suspend fun fetchAvailableQualities(url: String): List<VideoQuality> = withContext(Dispatchers.IO) {
        try {
            val info = YoutubeDL.getInstance().getInfo(url)"""
replacement_fetch = """    suspend fun fetchAvailableQualities(url: String): List<VideoQuality> = withContext(Dispatchers.IO) {
        try {
            if (url.contains("list=")) return@withContext VideoQuality.values().toList()
            val info = YoutubeDL.getInstance().getInfo(url)"""
content = content.replace(target_fetch, replacement_fetch)

# 2. Add concurrency and playlist logic to processDownload / queue loop
# Let's replace the single consumer loop with a concurrent one.
target_loop = """        // Sequential processor loop
        viewModelScope.launch {
            for (id in downloadChannel) {
                // Skip if it was cancelled while in the queue
                val item = _downloadQueue.value.find { it.id == id }
                if (item == null || item.status == "Cancelled") continue

                currentDownloadId = id
                currentDownloadJob = launch {
                    processDownload(id)
                }
                currentDownloadJob?.join()
                currentDownloadId = null
            }
        }"""
replacement_loop = """        // Concurrent processor loop
        viewModelScope.launch {
            val semaphore = kotlinx.coroutines.sync.Semaphore(1)
            
            // Watch config for max concurrent downloads changes
            launch {
                _appConfig.collect { config ->
                    // Semaphores can't be resized easily, so we handle concurrency dynamically
                    // Actually, a simpler way is to launch workers based on the current setting.
                    // But for simplicity, we'll just check active downloads.
                }
            }
            
            for (id in downloadChannel) {
                val item = _downloadQueue.value.find { it.id == id }
                if (item == null || item.status == "Cancelled") continue
                
                launch {
                    while (true) {
                        val activeCount = _downloadQueue.value.count { it.status == "Downloading" || it.status == "Extracting" }
                        if (activeCount < _appConfig.value.maxConcurrentDownloads) {
                            break
                        }
                        delay(1000)
                    }
                    processDownload(id)
                }
            }
        }"""
content = content.replace(target_loop, replacement_loop)

# 3. Update cancelDownload
target_cancel = """    fun cancelDownload(id: String) {
        if (id == currentDownloadId) {
            currentDownloadJob?.cancel()
            Thread {
                try { YoutubeDL.getInstance().destroyProcessById(id) } catch (e: Exception) {}
            }.start()
        } else {
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it } 
            }
        }
    }"""
replacement_cancel = """    fun cancelDownload(id: String) {
        val item = _downloadQueue.value.find { it.id == id }
        if (item?.status == "Downloading" || item?.status == "Extracting") {
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it } 
            }
            Thread {
                try { YoutubeDL.getInstance().destroyProcessById(id) } catch (e: Exception) {}
            }.start()
        } else {
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it } 
            }
        }
    }"""
content = content.replace(target_cancel, replacement_cancel)

# 4. Update processDownload to handle playlists properly in save logic
target_save = """                // Finished downloading to tmpDir. Copy to actual save location.
                val saveDir = _appConfig.value.saveDirectory
                tmpDir?.listFiles()?.forEach { fileToCopy ->
                    if (saveDir.startsWith("content://")) {
                        val treeUri = Uri.parse(saveDir)
                        val docFile = DocumentFile.fromTreeUri(application, treeUri)
                        if (docFile != null) {
                            var mimeType = "application/octet-stream"
                            if (fileToCopy.name.endsWith(".mp3") || fileToCopy.name.endsWith(".m4a")) mimeType = "audio/*"
                            else if (fileToCopy.name.endsWith(".mp4") || fileToCopy.name.endsWith(".webm") || fileToCopy.name.endsWith(".mkv")) mimeType = "video/*"
                            else if (fileToCopy.name.endsWith(".vtt") || fileToCopy.name.endsWith(".srt")) mimeType = "text/plain"
                            
                            val newFile = docFile.createFile(mimeType, fileToCopy.name)
                            if (newFile != null) {
                                application.contentResolver.openOutputStream(newFile.uri)?.use { out ->
                                    fileToCopy.inputStream().use { input ->
                                        input.copyTo(out)
                                    }
                                }
                            }
                        }
                    } else {
                        // Fallback for standard paths
                        val destDir = File(saveDir)
                        if (!destDir.exists()) destDir.mkdirs()
                        val destFile = File(destDir, fileToCopy.name)
                        fileToCopy.copyTo(destFile, overwrite = true)
                    }
                }"""
replacement_save = """                // Finished downloading to tmpDir. Copy to actual save location.
                val baseSaveDir = _appConfig.value.saveDirectory
                val finalSaveDirStr = if (isPlaylist) {
                    if (baseSaveDir.startsWith("content://")) baseSaveDir else "$baseSaveDir/${titleStr.replace(Regex("[\\\\\\\\/:*?\\"<>|]"), "_")}"
                } else baseSaveDir
                
                tmpDir?.walkTopDown()?.filter { it.isFile }?.forEach { fileToCopy ->
                    if (finalSaveDirStr.startsWith("content://")) {
                        val treeUri = Uri.parse(finalSaveDirStr)
                        var docFile = DocumentFile.fromTreeUri(application, treeUri)
                        if (isPlaylist && docFile != null) {
                            val playlistFolderName = titleStr.replace(Regex("[\\\\\\\\/:*?\\"<>|]"), "_")
                            var playlistFolder = docFile.findFile(playlistFolderName)
                            if (playlistFolder == null) {
                                playlistFolder = docFile.createDirectory(playlistFolderName)
                            }
                            docFile = playlistFolder
                        }
                        
                        if (docFile != null) {
                            var mimeType = "application/octet-stream"
                            if (fileToCopy.name.endsWith(".mp3") || fileToCopy.name.endsWith(".m4a")) mimeType = "audio/*"
                            else if (fileToCopy.name.endsWith(".mp4") || fileToCopy.name.endsWith(".webm") || fileToCopy.name.endsWith(".mkv")) mimeType = "video/*"
                            else if (fileToCopy.name.endsWith(".vtt") || fileToCopy.name.endsWith(".srt")) mimeType = "text/plain"
                            
                            val newFile = docFile.createFile(mimeType, fileToCopy.name)
                            if (newFile != null) {
                                application.contentResolver.openOutputStream(newFile.uri)?.use { out ->
                                    fileToCopy.inputStream().use { input ->
                                        input.copyTo(out)
                                    }
                                }
                            }
                        }
                    } else {
                        // Fallback for standard paths
                        val destDir = File(finalSaveDirStr)
                        if (!destDir.exists()) destDir.mkdirs()
                        val destFile = File(destDir, fileToCopy.name)
                        fileToCopy.copyTo(destFile, overwrite = true)
                    }
                }"""
content = content.replace(target_save, replacement_save)


# 5. Add yes-playlist to ytdlp request
target_options = """                val request = YoutubeDLRequest(url)
                //request.addOption("--force-ipv4")
                request.addOption("-o", "${tmpDir?.absolutePath}/%(title)s.%(ext)s")"""
replacement_options = """                val request = YoutubeDLRequest(url)
                if (isPlaylist) {
                    request.addOption("--yes-playlist")
                    request.addOption("-o", "${tmpDir?.absolutePath}/%(playlist_index)s - %(title)s.%(ext)s")
                } else {
                    request.addOption("--no-playlist")
                    request.addOption("-o", "${tmpDir?.absolutePath}/%(title)s.%(ext)s")
                }"""
content = content.replace(target_options, replacement_options)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)

