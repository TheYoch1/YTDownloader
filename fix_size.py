import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

dataclass = "\ndata class QualityOption(val quality: VideoQuality, val sizeStr: String)\n"

if "data class QualityOption" not in content:
    content = content.replace("enum class VideoQuality", dataclass + "\nenum class VideoQuality")

target_fetch = '''    suspend fun fetchAvailableQualities(url: String): List<VideoQuality> = withContext(Dispatchers.IO) {
        try {
            if (url.contains("list=")) return@withContext VideoQuality.values().toList()
            val req = com.yausername.youtubedl_android.YoutubeDLRequest(url)
            val info = YoutubeDL.getInstance().getInfo(req)
            val formatResolutions = info.formats?.flatMap { listOfNotNull(it.height, it.width) }?.toSet() ?: emptySet()
            if (formatResolutions.isEmpty()) return@withContext VideoQuality.values().toList()
            
            val available = VideoQuality.values().filter { q ->
                val qRes = q.label.replace("p", "").toInt()
                formatResolutions.contains(qRes)
            }
            if (available.isEmpty()) {
                val maxHeight = formatResolutions.maxOrNull() ?: 1080
                val filtered = VideoQuality.values().filter { it.label.replace("p", "").toInt() <= maxHeight }
                if (filtered.isEmpty()) VideoQuality.values().toList() else filtered
            } else {
                available
            }
        } catch(e: Exception) {
            VideoQuality.values().toList()
        }
    }'''

rep_fetch = '''    suspend fun fetchAvailableQualities(url: String): List<QualityOption> = withContext(Dispatchers.IO) {
        try {
            if (url.contains("list=")) return@withContext VideoQuality.values().map { QualityOption(it, "") }
            val req = com.yausername.youtubedl_android.YoutubeDLRequest(url)
            val info = YoutubeDL.getInstance().getInfo(req)
            val formats = info.formats ?: emptyList()
            
            val bestAudioSize = formats.filter { it.acodec != "none" && it.vcodec == "none" }
                                     .maxByOrNull { it.fileSize }?.fileSize ?: 0L
                                     
            val formatResolutions = formats.flatMap { listOfNotNull(it.height, it.width) }.toSet()
            if (formatResolutions.isEmpty()) return@withContext VideoQuality.values().map { QualityOption(it, "") }
            
            val available = VideoQuality.values().filter { q ->
                val qRes = q.label.replace("p", "").toInt()
                formatResolutions.contains(qRes)
            }
            
            val finalQualities = if (available.isEmpty()) {
                val maxHeight = formatResolutions.maxOrNull() ?: 1080
                val filtered = VideoQuality.values().filter { it.label.replace("p", "").toInt() <= maxHeight }
                if (filtered.isEmpty()) VideoQuality.values().toList() else filtered
            } else {
                available
            }
            
            finalQualities.map { quality ->
                val qRes = quality.label.replace("p", "").toInt()
                // find best video for this res
                val vFormat = formats.filter { (it.height == qRes || it.width == qRes) && it.vcodec != "none" }
                                     .maxByOrNull { it.fileSize }
                val vSize = vFormat?.fileSize ?: 0L
                val totalBytes = vSize + bestAudioSize
                val sizeStr = if (totalBytes > 0) {
                    String.format("%.1f MB", totalBytes / (1024.0 * 1024.0))
                } else {
                    ""
                }
                QualityOption(quality, sizeStr)
            }
        } catch(e: Exception) {
            VideoQuality.values().map { QualityOption(it, "") }
        }
    }'''

content = content.replace(target_fetch, rep_fetch)

# Now fix the formats! The user requested `-f "bestvideo+bestaudio/best" --merge-output-format mp4`

target_format = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[res<=2160][ext=mp4]+bestaudio[ext=m4a]/best[res<=2160][ext=mp4]/best"
                        "High1440" -> "bestvideo[res<=1440][ext=mp4]+bestaudio[ext=m4a]/best[res<=1440][ext=mp4]/best"
                        "High1080" -> "bestvideo[res<=1080][ext=mp4]+bestaudio[ext=m4a]/best[res<=1080][ext=mp4]/best"
                        "High720" -> "bestvideo[res<=720][ext=mp4]+bestaudio[ext=m4a]/best[res<=720][ext=mp4]/best"
                        "Medium480" -> "bestvideo[res<=480][ext=mp4]+bestaudio[ext=m4a]/best[res<=480][ext=mp4]/best"
                        "Medium360" -> "bestvideo[res<=360][ext=mp4]+bestaudio[ext=m4a]/best[res<=360][ext=mp4]/best"
                        "Low240" -> "bestvideo[res<=240][ext=mp4]+bestaudio[ext=m4a]/best[res<=240][ext=mp4]/best"
                        "Low144" -> "bestvideo[res<=144][ext=mp4]+bestaudio[ext=m4a]/best[res<=144][ext=mp4]/best"
                        else -> "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                    }
                    request.addOption("-f", formatStr)'''

rep_format = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[res<=2160]+bestaudio/best[res<=2160]/best"
                        "High1440" -> "bestvideo[res<=1440]+bestaudio/best[res<=1440]/best"
                        "High1080" -> "bestvideo[res<=1080]+bestaudio/best[res<=1080]/best"
                        "High720" -> "bestvideo[res<=720]+bestaudio/best[res<=720]/best"
                        "Medium480" -> "bestvideo[res<=480]+bestaudio/best[res<=480]/best"
                        "Medium360" -> "bestvideo[res<=360]+bestaudio/best[res<=360]/best"
                        "Low240" -> "bestvideo[res<=240]+bestaudio/best[res<=240]/best"
                        "Low144" -> "bestvideo[res<=144]+bestaudio/best[res<=144]/best"
                        else -> "bestvideo+bestaudio/best"
                    }
                    request.addOption("-f", formatStr)
                    request.addOption("--merge-output-format", "mp4")'''

content = content.replace(target_format, rep_format)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
print("done sizes")
