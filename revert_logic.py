import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Revert fetchAvailableFormats extractor-args
text = re.sub(r' *// UPDATED: Prioritize mobile clients to bypass JS challenges\n *request\.addOption\("--extractor-args", "youtube:player-client=android,ios,web"\)\n', '', text)

# Revert processDownload extractor-args and ffmpeg-location
text = re.sub(r' *val ffmpegPath = File\(app\.applicationInfo\.nativeLibraryDir, "libffmpeg\.so"\)\.absolutePath\n *request\.addOption\("--ffmpeg-location", ffmpegPath\)\n', '', text)

# Revert format string
old_format_block = """                    // UPDATED: Strict MP4/M4A matching for better FFmpeg compatibility on Android
                    val qHeight = item.settings.quality.label.replace("p", "")
                    request.addOption("-f", "bestvideo[ext=mp4][height<=$qHeight]+bestaudio[ext=m4a]/bestvideo[height<=$qHeight]+bestaudio/best")"""
new_format_block = """                    val qHeight = item.settings.quality.label.replace("p", "")
                    request.addOption("-f", "bestvideo[height<=$qHeight]+bestaudio/best")"""
text = text.replace(old_format_block, new_format_block)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
