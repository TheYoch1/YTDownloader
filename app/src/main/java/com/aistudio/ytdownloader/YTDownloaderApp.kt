package com.aistudio.ytdownloader

import android.app.Application
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLException
import com.yausername.ffmpeg.FFmpeg
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import androidx.work.*
import java.util.concurrent.TimeUnit

class YTDownloaderApp : Application() {
    companion object {
        var initError: String? = null
    }

    @OptIn(DelicateCoroutinesApi::class)
    override fun onCreate() {
        super.onCreate()
        
        // 1. Global Crash Handler (Safe Fallback)
        val defaultHandler = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
            // Save the crash flag so SplashActivity knows we died fatally
            val prefs = getSharedPreferences("app_prefs", MODE_PRIVATE)
            prefs.edit().putBoolean("crashed_last_time", true).commit()
            
            // Allow the default handler to kill the process to avoid zombification
            defaultHandler?.uncaughtException(thread, throwable)
        }

        try {
            // Note: YoutubeDL and FFmpeg init have been MOVED to SplashActivity
            // so they don't block the AppUpdater from running!
            NetworkMonitor.initialize(this)
            

            
            // Schedule periodic background updates using WorkManager
            val updateWorkRequest = PeriodicWorkRequestBuilder<UpdateWorker>(24, TimeUnit.HOURS)
                .setConstraints(
                    Constraints.Builder()
                        .setRequiredNetworkType(NetworkType.CONNECTED)
                        .build()
                )
                .build()
            
            WorkManager.getInstance(this).enqueueUniquePeriodicWork(
                "YTDlpUpdateWork",
                ExistingPeriodicWorkPolicy.KEEP,
                updateWorkRequest
            )
            
            // Try to update yt-dlp in the background on startup
            GlobalScope.launch(Dispatchers.IO) {
                try {
                    val status = YoutubeDL.getInstance().updateYoutubeDL(this@YTDownloaderApp, YoutubeDL.UpdateChannel.NIGHTLY)
                    if (status != null) {
                        kotlinx.coroutines.withContext(Dispatchers.Main) {
                            // Suppress toast so it's not annoying, or just keep it
                            android.util.Log.d("YTDownloaderApp", "yt-dlp core verified & up-to-date")
                        }
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        } catch (e: Exception) {
            initError = e.message ?: e.toString()
            e.printStackTrace()
        }
    }
}
