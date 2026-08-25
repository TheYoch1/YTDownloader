with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = """    fun addDownload(url: String, initialTitle: String? = null, specificSettings: DownloadSettings? = null) {"""

replacement = """    suspend fun fetchAvailableQualities(url: String): List<VideoQuality> = withContext(Dispatchers.IO) {
        try {
            val info = YoutubeDL.getInstance().getInfo(url)
            val heights = info.formats?.mapNotNull { it.height }?.distinct() ?: emptyList()
            if (heights.isEmpty()) return@withContext VideoQuality.values().toList()
            
            val maxHeight = heights.maxOrNull() ?: 1080
            VideoQuality.values().filter { it.label.replace("p", "").toInt() <= maxHeight }
        } catch(e: Exception) {
            VideoQuality.values().toList()
        }
    }

    fun addDownload(url: String, initialTitle: String? = null, specificSettings: DownloadSettings? = null) {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
