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
            val videoHeights = mutableSetOf<Int>()
            
            for (i in 0 until formats.length()) {
                val f = formats.optJSONObject(i) ?: continue
                val vcodec = f.optString("vcodec", "none")
                val height = f.optInt("height", 0)
                
                if (vcodec != "none" && height >= 480) {
                    videoHeights.add(height)
                }
            }
            
            // Audio formats
            result.add(FormatOption("bestaudio[ext=m4a]/bestaudio", "M4A Audio", "", true))
            result.add(FormatOption("bestaudio", "MP3 Audio (Best Quality)", "", true))
            
            // Standard Video Qualities
            val standardQualities = listOf(4320, 2160, 1440, 1080, 720, 480)
            for (q in standardQualities) {
                if (videoHeights.contains(q) || videoHeights.any { it in (q - 50)..(q + 50) }) {
                    result.add(FormatOption("bestvideo[height<=$q]+bestaudio/best", "Video: ${q}p (MP4)", "", false, q))
                }
            }
            
            // Fallback if no video >= 480p is found
            if (result.none { !it.isAudioOnly }) {
                result.add(FormatOption("bestvideo+bestaudio/best", "Video: Best Available (MP4)", "", false, 0))
            }
            
            return@withContext result.sortedByDescending { it.height }
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }"""

text = re.sub(r'    suspend fun fetchAvailableFormats.*?catch \(e: Exception\) \{\n.*?e\.printStackTrace\(\)\n.*?emptyList\(\)\n.*?\}\n    \}', new_fetch, text, flags=re.DOTALL)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)

