import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Change return type
text = text.replace(
    "suspend fun fetchAvailableFormats(url: String): List<FormatOption> = withContext(Dispatchers.IO) {",
    "suspend fun fetchAvailableFormats(url: String): Pair<String, List<FormatOption>> = withContext(Dispatchers.IO) {"
)

# Return empty if fail
text = text.replace(
    "if (jsonOut.isNullOrEmpty()) return@withContext emptyList()",
    "if (jsonOut.isNullOrEmpty()) return@withContext Pair(\"Unknown Title\", emptyList())"
)

# Parse title and width/height
new_loop = """            val json = JSONObject(jsonOut)
            val title = json.optString("title", "Unknown Title")
            val formats = json.optJSONArray("formats") ?: JSONArray()
            
            val result = mutableListOf<FormatOption>()
            val videoOptions = mutableListOf<FormatOption>()
            
            for (i in 0 until formats.length()) {
                val f = formats.optJSONObject(i) ?: continue
                val vcodec = f.optString("vcodec", "none")
                val height = f.optInt("height", 0)
                val width = f.optInt("width", 0)
                val formatId = f.optString("format_id", "")
                val filesize = f.optLong("filesize", 0L)
                val ext = f.optString("ext", "")
                
                if (formatId.isEmpty()) continue
                
                // Determine standard quality (p)
                val minDim = if (width > 0 && height > 0) Math.min(width, height) else height
                // Map to closest standard resolution if near
                val standardP = when {
                    minDim >= 4300 -> 4320
                    minDim >= 2100 -> 2160
                    minDim >= 1400 -> 1440
                    minDim >= 1000 -> 1080
                    minDim >= 700 -> 720
                    minDim >= 470 -> 480
                    else -> minDim
                }
                
                if (vcodec != "none" && standardP >= 480) {
                    val sizeStr = if (filesize > 0) String.format("%.1f MB", filesize / 1024f / 1024f) else ""
                    videoOptions.add(FormatOption(formatId, "${standardP}p", sizeStr, false, standardP))
                }
            }"""

old_loop = r"""            val json = JSONObject\(jsonOut\)\n            val formats = json\.optJSONArray\("formats"\) \?: JSONArray\(\)\n            \n            val result = mutableListOf<FormatOption>\(\)\n            val videoOptions = mutableListOf<FormatOption>\(\)\n            \n            for \(i in 0 until formats\.length\(\)\) \{\n                val f = formats\.optJSONObject\(i\) \?: continue\n                val vcodec = f\.optString\("vcodec", "none"\)\n                val height = f\.optInt\("height", 0\)\n                val formatId = f\.optString\("format_id", ""\)\n                val filesize = f\.optLong\("filesize", 0L\)\n                val ext = f\.optString\("ext", ""\)\n                \n                if \(formatId\.isEmpty\(\)\) continue\n                \n                if \(vcodec != "none" && height >= 480\) \{\n                    val sizeStr = if \(filesize > 0\) String\.format\("%.1f MB", filesize / 1024f / 1024f\) else ""\n                    videoOptions\.add\(FormatOption\(formatId, "Video: \$\{height\}p \(MP4\)", sizeStr, false, height\)\)\n                \}\n            \}"""

text = re.sub(old_loop, new_loop, text, flags=re.DOTALL)

text = text.replace(
    """            if (bestFormatsByHeight.isEmpty()) {
                result.add(FormatOption("bestvideo", "Video: Best Available (MP4)", "", false, 0))
            }
            
            return@withContext result""",
    """            if (bestFormatsByHeight.isEmpty()) {
                result.add(FormatOption("bestvideo", "Best Available", "", false, 0))
            }
            
            return@withContext Pair(title, result)"""
)

text = text.replace(
    """        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }""",
    """        } catch (e: Exception) {
            e.printStackTrace()
            Pair("Unknown Title", emptyList())
        }"""
)

# Fix save location
text = text.replace(
    """            val saveDir = if (_appConfig.value.saveDirectory == "Default") {
                File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), "YTDownloader")
            } else {
                File(_appConfig.value.saveDirectory)
            }
            if (!saveDir.exists()) saveDir.mkdirs()""",
    """            val baseDir = if (_appConfig.value.saveDirectory == "Default") {
                File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), "YT Downloader")
            } else {
                File(_appConfig.value.saveDirectory)
            }
            val saveDir = if (item.settings.audioOnly) File(baseDir, "Music") else File(baseDir, "Video")
            if (!saveDir.exists()) saveDir.mkdirs()"""
)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
