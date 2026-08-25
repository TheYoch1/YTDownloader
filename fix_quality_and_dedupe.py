import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

# Fix fetchAvailableQualities
target_fetch = '''    suspend fun fetchAvailableQualities(url: String): List<VideoQuality> = withContext(Dispatchers.IO) {
        try {
            if (url.contains("list=")) return@withContext VideoQuality.values().toList()
            val req = com.yausername.youtubedl_android.YoutubeDLRequest(url)
            val info = YoutubeDL.getInstance().getInfo(req)
            val heights = info.formats?.mapNotNull { it.height }?.distinct() ?: emptyList()
            if (heights.isEmpty()) return@withContext VideoQuality.values().toList()
            
            val maxHeight = heights.maxOrNull() ?: 1080
            val filtered = VideoQuality.values().filter { it.label.replace("p", "").toInt() <= maxHeight }
            if (filtered.isEmpty()) VideoQuality.values().toList() else filtered
        } catch(e: Exception) {
            VideoQuality.values().toList()
        }
    }'''

rep_fetch = '''    suspend fun fetchAvailableQualities(url: String): List<VideoQuality> = withContext(Dispatchers.IO) {
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
content = content.replace(target_fetch, rep_fetch)

# Fix file deduplication
target_dedupe = '''                        var destFile = File(destDir, fileToCopy.name)
                        if (destFile.exists()) {
                            val deleted = destFile.delete()
                            if (!deleted) {
                                val nameWithoutExtension = fileToCopy.nameWithoutExtension
                                val extension = fileToCopy.extension
                                destFile = File(destDir, "${nameWithoutExtension}_${System.currentTimeMillis()}.$extension")
                            }
                        }'''

rep_dedupe = '''                        var destFile = File(destDir, fileToCopy.name)
                        if (destFile.exists()) {
                            val deleted = destFile.delete()
                            if (!deleted) {
                                val nameWithoutExtension = fileToCopy.nameWithoutExtension
                                val extension = fileToCopy.extension
                                var counter = 1
                                do {
                                    destFile = File(destDir, "${nameWithoutExtension} ($counter).$extension")
                                    counter++
                                } while (destFile.exists())
                            }
                        }'''
content = content.replace(target_dedupe, rep_dedupe)

# Fix format strings (remove [res>=480] floor and simplify)
target_format = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[res<=2160][res>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[res<=2160][res>=480]+bestaudio/best[res<=2160][res>=480]/best[res>=480]"
                        "High1440" -> "bestvideo[res<=1440][res>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[res<=1440][res>=480]+bestaudio/best[res<=1440][res>=480]/best[res>=480]"
                        "High1080" -> "bestvideo[res<=1080][res>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[res<=1080][res>=480]+bestaudio/best[res<=1080][res>=480]/best[res>=480]"
                        "High720" -> "bestvideo[res<=720][res>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[res<=720][res>=480]+bestaudio/best[res<=720][res>=480]/best[res>=480]"
                        "Medium480" -> "bestvideo[res<=480][res>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[res<=480][res>=480]+bestaudio/best[res<=480][res>=480]/best[res>=480]"
                        "Medium360" -> "bestvideo[res<=360][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[res<=360]+bestaudio/best[res<=360]/best"
                        "Low240" -> "bestvideo[res<=240][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[res<=240]+bestaudio/best[res<=240]/best"
                        "Low144" -> "bestvideo[res<=144][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[res<=144]+bestaudio/best[res<=144]/best"
                        else -> "bestvideo[res>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[res>=480]+bestaudio/best[res>=480]"
                    }'''

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
                    }'''
content = content.replace(target_format, rep_format)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)

print(content.find(rep_fetch))
print(content.find(rep_dedupe))
print(content.find(rep_format))
