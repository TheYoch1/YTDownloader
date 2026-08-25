package com.aistudio.ytdownloader
import android.app.Application
import androidx.test.core.app.ApplicationProvider
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest

@RunWith(RobolectricTestRunner::class)
class DownloadTest {
    @Test
    fun testDownload() {
        val app = ApplicationProvider.getApplicationContext<Application>()
        YoutubeDL.getInstance().init(app)
        
        val req = YoutubeDLRequest("https://www.youtube.com/watch?v=BaW_jenozKc")
        req.addOption("-f", "bestvideo[res<=720]+bestaudio/best[res<=720]/best")
        req.addOption("--extractor-args", "youtube:player_client=android,web")
        req.addOption("--verbose")
        
        try {
            val res = YoutubeDL.getInstance().execute(req, "test") { progress, eta, line ->
                println("YTDL: $line")
            }
            println("OUT: " + res.out)
            println("ERR: " + res.err)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
