import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

imports = """import android.app.Application
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
"""
text = text.replace("import android.app.Application\nimport android.content.Intent", imports)

init_block = """class DownloaderViewModel(application: Application) : AndroidViewModel(application) {
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
"""
text = text.replace("class DownloaderViewModel(application: Application) : AndroidViewModel(application) {\n    val downloadQueue: StateFlow<List<QueuedDownload>> = DownloadRepository.downloadQueue\n", init_block)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
