import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

new_fetch = """    suspend fun fetchAvailableFormats(url: String): List<FormatOption> = withContext(Dispatchers.IO) {
        try {
            val request = YoutubeDLRequest(url)
            request.addOption("--dump-json")
            request.addOption("--no-playlist")
            
            val response = YoutubeDL.getInstance().execute(request, null, null)
            val jsonOut = response.out
            
            if (jsonOut.isNullOrEmpty()) return@withContext emptyList()
            
            val json = JSONObject(jsonOut)
            val formats = json.optJSONArray("formats") ?: JSONArray()
            
            val result = mutableListOf<FormatOption>()
            val videoOptions = mutableListOf<FormatOption>()
            
            for (i in 0 until formats.length()) {
                val f = formats.optJSONObject(i) ?: continue
                val vcodec = f.optString("vcodec", "none")
                val height = f.optInt("height", 0)
                val formatId = f.optString("format_id", "")
                val filesize = f.optLong("filesize", 0L)
                val ext = f.optString("ext", "")
                
                if (formatId.isEmpty()) continue
                if (vcodec != "none" && height >= 480) {
                    val sizeStr = if (filesize > 0) String.format("%.1f MB", filesize / 1024f / 1024f) else ""
                    // We prioritize mp4 formats later, so record the ext to help sort.
                    videoOptions.add(FormatOption(formatId, "Video: ${height}p (MP4)", sizeStr, false, height).apply { 
                        // Using label temporarily to store ext for sorting if needed, or just let distinctBy handle it. 
                    })
                }
            }
            
            // Audio formats
            result.add(FormatOption("bestaudio[ext=m4a]/bestaudio", "M4A Audio", "", true))
            result.add(FormatOption("bestaudio", "MP3 Audio (Best Quality)", "", true))
            
            // Group by height, prefer MP4 or just pick the best one
            val bestFormatsByHeight = videoOptions.groupBy { it.height }.mapNotNull { (height, formatsList) ->
                formatsList.lastOrNull() // Usually the last one in the JSON list for a given height is the best one (yt-dlp sorts them)
            }.sortedByDescending { it.height }
            
            result.addAll(bestFormatsByHeight)
            
            // Fallback if no video >= 480p is found
            if (bestFormatsByHeight.isEmpty()) {
                result.add(FormatOption("bestvideo", "Video: Best Available (MP4)", "", false, 0))
            }
            
            return@withContext result
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }"""

text = re.sub(r'    suspend fun fetchAvailableFormats.*?catch \(e: Exception\) \{\n.*?e\.printStackTrace\(\)\n.*?emptyList\(\)\n.*?\}\n    \}', new_fetch, text, flags=re.DOTALL)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
