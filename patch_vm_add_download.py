with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = """    fun addDownload(url: String, initialTitle: String? = null) {
        if (url.isBlank()) return
        
        val newDownload = QueuedDownload(
            id = UUID.randomUUID().toString(),
            title = initialTitle ?: "Pending...",
            url = url,
            isPlaylist = url.contains("list="),
            status = "Queued",
            settings = _currentSettings.value.copy()
        )
        
        _downloadQueue.update { it + newDownload }
        downloadChannel.trySend(newDownload.id)
    }"""

replacement = """    fun addDownload(url: String, initialTitle: String? = null, specificSettings: DownloadSettings? = null) {
        if (url.isBlank()) return
        
        val newDownload = QueuedDownload(
            id = UUID.randomUUID().toString(),
            title = initialTitle ?: "Pending...",
            url = url,
            isPlaylist = url.contains("list="),
            status = "Queued",
            settings = specificSettings ?: _currentSettings.value.copy()
        )
        
        _downloadQueue.update { it + newDownload }
        downloadChannel.trySend(newDownload.id)
    }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
