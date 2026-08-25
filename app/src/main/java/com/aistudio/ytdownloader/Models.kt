package com.aistudio.ytdownloader

enum class VideoQuality(val label: String, val fps: Int) {
    Medium480("480p", 30),
    High720("720p", 30),
    High1080("1080p", 30),
    High1440("1440p", 30),
    High2160("2160p", 30)
}

data class DownloadSettings(
    var saveFormat: String = "mp3",
    var audioOnly: Boolean = true,
    var quality: VideoQuality = VideoQuality.High720,
    var tagAudioFile: Boolean = true,
    var filenamePattern: String = "\$title",
    var openDestinationFolderWhenDone: Boolean = false,
    var convert: Boolean = false,
    var downloadSubtitles: Boolean = false,
    var customFormatId: String? = null
)

data class AppConfig(
    var theme: String = "Dark",
    var accent: String = "Teal",
    var saveDirectory: String = "Default",
    var maxConcurrentDownloads: Int = 1,
    var colorOffset: Float = -1f,
    var confirmExit: Boolean = true,
    var wifiOnly: Boolean = false,
    var notifyOnComplete: Boolean = true
)

data class QueuedDownload(
    val id: String,
    val title: String,
    val url: String,
    val isPlaylist: Boolean,
    var progress: Float = 0f,
    var status: String = "Queued",
    var downloadSpeed: String = "",
    val settings: DownloadSettings,
    var errorMessage: String? = null,
    var localFilePath: String? = null
)

data class QualityOption(val quality: VideoQuality, val sizeStr: String)

data class FormatOption(
    val formatId: String,
    val label: String,
    val sizeStr: String,
    val isAudioOnly: Boolean,
    val height: Int = 0
)
