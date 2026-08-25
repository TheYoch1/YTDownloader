with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "r") as f:
    text = f.read()

import re
old = """data class DownloadSettings(
    var saveFormat: String = "mp3",
    var audioOnly: Boolean = false,
    var quality: VideoQuality = VideoQuality.High720,
    var tagAudioFile: Boolean = true,
    var filenamePattern: String = "\\$title",
    var openDestinationFolderWhenDone: Boolean = false,
    var convert: Boolean = false,
    var downloadSubtitles: Boolean = false,
    var customFormatId: String? = null
)"""
new = """data class DownloadSettings(
    var saveFormat: String = "mp3",
    var audioOnly: Boolean = false,
    var quality: VideoQuality = VideoQuality.High720,
    var tagAudioFile: Boolean = true,
    var filenamePattern: String = "\\$title",
    var openDestinationFolderWhenDone: Boolean = false,
    var convert: Boolean = false,
    var downloadSubtitles: Boolean = false,
    var customFormatId: String? = null,
    var formatLabel: String = "",
    var selectedHeight: Int = 0
)"""
text = text.replace(old, new)
with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "w") as f:
    f.write(text)
