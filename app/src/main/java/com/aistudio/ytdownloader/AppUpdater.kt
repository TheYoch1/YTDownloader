package com.aistudio.ytdownloader

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import okhttp3.Request

@Serializable
data class UpdateInfo(
    val latest_version: Int,
    val url: String,
    val mandatory: Boolean = false
)

object AppUpdater {
    // Replace with the actual URL where your version.json is hosted
    private const val UPDATE_URL = "https://TheYoch1.github.io/YTDownloader/version.json"

    suspend fun checkForUpdates(context: Context): UpdateInfo? = withContext(Dispatchers.IO) {
        try {
            val request = Request.Builder()
                .url(UPDATE_URL)
                .build()
            
            NetworkMonitor.okHttpClient.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    val body = response.body?.string()
                    if (body != null) {
                        val format = Json { ignoreUnknownKeys = true }
                        return@withContext format.decodeFromString<UpdateInfo>(body)
                    }
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        null
    }
}
