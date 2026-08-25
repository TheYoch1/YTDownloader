with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

import re

old_title_logic = """            val json = JSONObject(jsonOut)
            val playlistTitle = json.optString("playlist_title", "")
            val title = if (url.contains("list=") && playlistTitle.isNotEmpty() && playlistTitle != "null") playlistTitle else if (url.contains("list=") && json.optString("playlist", "").isNotEmpty() && json.optString("playlist") != "null") json.optString("playlist") else json.optString("title", "Unknown Title")"""

new_title_logic = """            val json = JSONObject(jsonOut)
            var playlistTitle = json.optString("playlist_title", "")
            if (playlistTitle.isEmpty() || playlistTitle == "null") playlistTitle = json.optString("playlist", "")
            
            if (url.contains("list=") && (playlistTitle.isEmpty() || playlistTitle == "null")) {
                try {
                    val plRequest = com.yausername.youtubedl_android.YoutubeDLRequest(url)
                    plRequest.addOption("--dump-single-json")
                    plRequest.addOption("--playlist-items", "1")
                    val plResponse = com.yausername.youtubedl_android.YoutubeDL.getInstance().execute(plRequest, null, null)
                    val plJsonOut = plResponse.out
                    if (!plJsonOut.isNullOrEmpty()) {
                        val plJson = JSONObject(plJsonOut)
                        playlistTitle = plJson.optString("title", "")
                    }
                } catch (e: Exception) {}
            }
            
            val title = if (url.contains("list=") && playlistTitle.isNotEmpty() && playlistTitle != "null") playlistTitle else json.optString("title", "Unknown Title")"""

text = text.replace(old_title_logic, new_title_logic)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
