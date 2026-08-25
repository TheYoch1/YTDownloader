package com.aistudio.ytdownloader

import android.app.Application
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

import androidx.core.content.ContextCompat
import androidx.lifecycle.AndroidViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.util.UUID

class DownloaderViewModel(application: Application) : AndroidViewModel(application) {
    val downloadQueue: StateFlow<List<QueuedDownload>> = DownloadRepository.downloadQueue

    private val sharedPreferences: SharedPreferences = application.getSharedPreferences("yt_downloader_prefs", Context.MODE_PRIVATE)
    private val gson = Gson()

    init {
        loadQueue()
    }

    fun saveQueue() {
        val json = gson.toJson(DownloadRepository.downloadQueue.value)
        sharedPreferences.edit().putString("saved_queue", json).apply()
    }

    private fun loadQueue() {
        val json = sharedPreferences.getString("saved_queue", null)
        if (json != null) {
            try {
                val type = object : TypeToken<List<QueuedDownload>>() {}.type
                val savedList: List<QueuedDownload> = gson.fromJson(json, type)
                
                // State Correction on Load
                val correctedList = savedList.map { item ->
                    if (item.status == "Downloading" || item.status == "Finishing") {
                        item.copy(status = "Paused", downloadSpeed = "")
                    } else {
                        item
                    }
                }
                DownloadRepository.updateQueue { correctedList }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    private val _currentSettings = MutableStateFlow(DownloadSettings())
    val currentSettings: StateFlow<DownloadSettings> = _currentSettings.asStateFlow()

    private val _appConfig = MutableStateFlow(AppConfig())
    val appConfig: StateFlow<AppConfig> = _appConfig.asStateFlow()

    fun updateCurrentSettings(settings: DownloadSettings) {
        _currentSettings.value = settings
    }

    fun updateConfig(config: AppConfig) {
        _appConfig.value = config
        DownloadRepository.appConfig = config
    }

    suspend fun fetchAvailableFormats(url: String): Pair<String, List<FormatOption>> = withContext(Dispatchers.IO) {
        try {
            val request = com.yausername.youtubedl_android.YoutubeDLRequest(url)
            request.addOption("--dump-json")
            request.addOption("--no-playlist")
            
            val response = com.yausername.youtubedl_android.YoutubeDL.getInstance().execute(request, null, null)
            val jsonOut = response.out
            
            if (jsonOut.isNullOrEmpty()) return@withContext Pair("Unknown Title", emptyList())
            
            val json = JSONObject(jsonOut)
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
            
            val title = if (url.contains("list=") && playlistTitle.isNotEmpty() && playlistTitle != "null") playlistTitle else json.optString("title", "Unknown Title")
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
                
                if (formatId.isEmpty()) continue
                
                val minDim = if (width > 0 && height > 0) Math.min(width, height) else height
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
            }
            
            result.add(FormatOption("bestaudio[ext=m4a]/bestaudio", "M4A Audio", "", true))
            result.add(FormatOption("bestaudio", "MP3 Audio (Best Quality)", "", true))
            
            val bestFormatsByHeight = videoOptions.groupBy { it.height }.mapNotNull { (height, formatsList) ->
                formatsList.lastOrNull() 
            }.sortedByDescending { it.height }
            
            result.addAll(bestFormatsByHeight)
            
            if (bestFormatsByHeight.isEmpty()) {
                result.add(FormatOption("bestvideo", "Best Available", "", false, 0))
            }
            
            return@withContext Pair(title, result)
        } catch (e: Exception) {
            e.printStackTrace()
            Pair("Unknown Title", emptyList())
        }
    }

    fun addDownload(url: String, title: String, isPlaylist: Boolean, settings: DownloadSettings) {
        val id = UUID.randomUUID().toString()
        val download = QueuedDownload(
            id = id,
            title = title,
            url = url,
            isPlaylist = isPlaylist,
            settings = settings
        )
        DownloadRepository.addDownload(download)
        
        val intent = Intent(getApplication(), DownloadService::class.java).apply {
            action = DownloadService.ACTION_START
            putExtra(DownloadService.EXTRA_DOWNLOAD_ID, id)
        }
        ContextCompat.startForegroundService(getApplication(), intent)
    }

    fun cancelDownload(id: String) {
        val item = DownloadRepository.getDownload(id)
        if (item?.status == "Downloading" || item?.status == "Queued") {
            DownloadRepository.updateQueue { q -> q.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it } }
            val intent = Intent(getApplication(), DownloadService::class.java).apply {
                action = DownloadService.ACTION_STOP_DOWNLOAD
                putExtra(DownloadService.EXTRA_DOWNLOAD_ID, id)
            }
            ContextCompat.startForegroundService(getApplication(), intent)
        } else {
            DownloadRepository.updateQueue { q -> q.map { if (it.id == id) it.copy(status = "Cancelled", progress = 0f, downloadSpeed = "") else it } }
        }
    }

    fun pauseDownload(id: String) {
        DownloadRepository.updateQueue { q -> q.map { if (it.id == id && it.status == "Downloading") it.copy(status = "Paused", downloadSpeed = "Paused") else it } }
        val intent = Intent(getApplication(), DownloadService::class.java).apply {
            action = DownloadService.ACTION_STOP_DOWNLOAD
            putExtra(DownloadService.EXTRA_DOWNLOAD_ID, id)
        }
        ContextCompat.startForegroundService(getApplication(), intent)
    }

    fun resumeDownload(id: String) {
        DownloadRepository.updateQueue { q -> q.map { if (it.id == id && it.status == "Paused") it.copy(status = "Queued", downloadSpeed = "Resuming...") else it } }
        val intent = Intent(getApplication(), DownloadService::class.java).apply {
            action = DownloadService.ACTION_START
            putExtra(DownloadService.EXTRA_DOWNLOAD_ID, id)
        }
        ContextCompat.startForegroundService(getApplication(), intent)
    }

    fun removeDownload(id: String) {
        cancelDownload(id)
        DownloadRepository.updateQueue { q -> q.filter { download -> download.id != id } }
    }

        fun sortQueue(sortType: String) {
        DownloadRepository.updateQueue { q ->
            when (sortType) {
                "Alphabetical" -> q.sortedBy { it.title.lowercase() }
                "Newest First" -> q.sortedByDescending { it.timestamp }
                "Oldest First" -> q.sortedBy { it.timestamp }
                else -> q
            }
        }
        saveQueue()
    }

    fun reorderQueue(fromIndex: Int, toIndex: Int) {
        DownloadRepository.updateQueue { q ->
            val mutableQ = q.toMutableList()
            if (fromIndex in 0 until mutableQ.size && toIndex in 0 until mutableQ.size) {
                val item = mutableQ.removeAt(fromIndex)
                mutableQ.add(toIndex, item)
            }
            mutableQ
        }
    }

    fun clearFinishedDownloads() {
        DownloadRepository.updateQueue { q -> q.filter { it.status != "Completed" && it.status != "Error" && it.status != "Cancelled" } }
    }

    fun retryDownload(id: String) {
        val download = DownloadRepository.getDownload(id) ?: return
        if (download.status == "Error") {
            DownloadRepository.updateQueue { q -> q.map { if (it.id == id) it.copy(status = "Queued", progress = 0f, errorMessage = null) else it } }
            val intent = Intent(getApplication(), DownloadService::class.java).apply {
                action = DownloadService.ACTION_START
                putExtra(DownloadService.EXTRA_DOWNLOAD_ID, id)
            }
            ContextCompat.startForegroundService(getApplication(), intent)
        }
    }
}
