package com.aistudio.ytdownloader

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import org.json.JSONObject

data class SearchResult(
    val title: String,
    val url: String,
    val thumbnailUrl: String? = null
)

suspend fun searchYouTubeVideos(query: String): List<SearchResult> = withContext(Dispatchers.IO) {
    if (!NetworkMonitor.isConnected.value) {
        throw Exception("No active internet connection.")
    }
    val results = mutableListOf<SearchResult>()
    try {
        val request = YoutubeDLRequest("ytsearch15:$query")
        request.addOption("--dump-json")
        request.addOption("--flat-playlist")
        request.addOption("--ignore-errors")
        request.addOption("--retries", "10")
        request.addOption("--socket-timeout", "15")
        
        val response = YoutubeDL.getInstance().execute(request, "search")
        val output = response.out ?: ""
        
        output.lines().forEach { line ->
            if (line.isNotBlank()) {
                try {
                    val json = JSONObject(line)
                    val id = json.optString("id")
                    val title = json.optString("title", "Unknown Title")
                    val url = json.optString("webpage_url", "https://youtube.com/watch?v=$id")
                    
                    var thumbUrl: String? = null
                    if (json.has("thumbnails")) {
                        val thumbs = json.getJSONArray("thumbnails")
                        if (thumbs.length() > 0) {
                            thumbUrl = thumbs.getJSONObject(thumbs.length() - 1).optString("url")
                        }
                    } else {
                        thumbUrl = "https://i.ytimg.com/vi/$id/hqdefault.jpg"
                    }
                    
                    if (id.isNotBlank() && (url.contains("watch") || url.contains("youtube"))) {
                        results.add(SearchResult(title, url, thumbUrl))
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
    } catch (e: Exception) {
        e.printStackTrace()
    }
    results
}
