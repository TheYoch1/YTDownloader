import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[height<=2160][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio[ext=m4a]/best"
                        "High1440" -> "bestvideo[height<=1440][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio[ext=m4a]/best"
                        "High1080" -> "bestvideo[height<=1080][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio[ext=m4a]/best"
                        "High720" -> "bestvideo[height<=720][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio[ext=m4a]/best"
                        "Medium480" -> "bestvideo[height<=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio[ext=m4a]/best"
                        "Medium360" -> "bestvideo[height<=360][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio[ext=m4a]/best"
                        "Low240" -> "bestvideo[height<=240][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=240]+bestaudio[ext=m4a]/best"
                        "Low144" -> "bestvideo[height<=144][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=144]+bestaudio[ext=m4a]/best"
                        else -> "bestvideo[vcodec^=avc]+bestaudio[ext=m4a]/bestvideo+bestaudio[ext=m4a]/best"
                    }
                    request.addOption("-f", formatStr)
                    request.addOption("--remux-video", "mp4")
                }'''

rep = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[height<=2160]+bestaudio/best"
                        "High1440" -> "bestvideo[height<=1440]+bestaudio/best"
                        "High1080" -> "bestvideo[height<=1080]+bestaudio/best"
                        "High720" -> "bestvideo[height<=720]+bestaudio/best"
                        "Medium480" -> "bestvideo[height<=480]+bestaudio/best"
                        "Medium360" -> "bestvideo[height<=360]+bestaudio/best"
                        "Low240" -> "bestvideo[height<=240]+bestaudio/best"
                        "Low144" -> "bestvideo[height<=144]+bestaudio/best"
                        else -> "bestvideo+bestaudio/best"
                    }
                    request.addOption("-f", formatStr)
                    request.addOption("--merge-output-format", "mkv")
                    request.addOption("--remux-video", "mp4")
                    request.addOption("--postprocessor-args", "ffmpeg:-c copy -tag:v hvc1")
                }'''

content = content.replace(target, rep)
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
