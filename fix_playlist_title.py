with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

import re

old_start = """    private suspend fun processDownload(id: String) {
        var tmpDir: File? = null
        try {
            val item = DownloadRepository.getDownload(id) ?: return
            DownloadRepository.updateQueue { q -> q.map { if (it.id == id) it.copy(status = "Downloading") else it } }
            val app = applicationContext"""

new_start = """    private suspend fun processDownload(id: String) {
        var tmpDir: File? = null
        try {
            var item = DownloadRepository.getDownload(id) ?: return
            
            // Fetch playlist title if unknown
            if (item.isPlaylist && (item.title == "Unknown Title" || item.title.isEmpty())) {
                try {
                    val plRequest = com.yausername.youtubedl_android.YoutubeDLRequest(item.url)
                    plRequest.addOption("--dump-single-json")
                    plRequest.addOption("--playlist-items", "1")
                    val plResponse = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) { com.yausername.youtubedl_android.YoutubeDL.getInstance().execute(plRequest, null, null) }
                    if (!plResponse.out.isNullOrEmpty()) {
                        val json = org.json.JSONObject(plResponse.out)
                        var plTitle = json.optString("playlist_title", "")
                        if (plTitle.isEmpty() || plTitle == "null") plTitle = json.optString("playlist", "")
                        if (plTitle.isEmpty() || plTitle == "null") plTitle = json.optString("title", "Unknown Title")
                        
                        DownloadRepository.updateQueue { q -> q.map { if (it.id == id) it.copy(title = plTitle) else it } }
                        item = DownloadRepository.getDownload(id) ?: item
                    }
                } catch (e: Exception) {}
            }
            
            DownloadRepository.updateQueue { q -> q.map { if (it.id == id) it.copy(status = "Downloading") else it } }
            val app = applicationContext"""

text = text.replace(old_start, new_start)

# Now fix the regex for item progress
old_regex = """val matchPlaylist = Regex(\"\"\"\\[download\\] Downloading video (\\d+) of (\\d+)\"\"\").find(line)"""
new_regex = """val matchPlaylist = Regex(\"\"\"\\[download\\] Downloading (?:video|item) (\\d+) of (\\d+)\"\"\").find(line)"""
text = text.replace(old_regex, new_regex)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)
