with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

old_title = """            val json = JSONObject(jsonOut)
            val title = json.optString("title", "Unknown Title")"""

new_title = """            val json = JSONObject(jsonOut)
            val playlistTitle = json.optString("playlist_title", "")
            val title = if (url.contains("list=") && playlistTitle.isNotEmpty() && playlistTitle != "null") playlistTitle else if (url.contains("list=") && json.optString("playlist", "").isNotEmpty() && json.optString("playlist") != "null") json.optString("playlist") else json.optString("title", "Unknown Title")"""

text = text.replace(old_title, new_title)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
