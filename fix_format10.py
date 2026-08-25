import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[height<=2160][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best[height<=2160]/best"
                        "High1440" -> "bestvideo[height<=1440][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best[height<=1440]/best"
                        "High1080" -> "bestvideo[height<=1080][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
                        "High720" -> "bestvideo[height<=720][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]/best"
                        "Medium480" -> "bestvideo[height<=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]/best"
                        "Medium360" -> "bestvideo[height<=360][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]/best"
                        "Low240" -> "bestvideo[height<=240][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=240]+bestaudio/best[height<=240]/best"
                        "Low144" -> "bestvideo[height<=144][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=144]+bestaudio/best[height<=144]/best"
                        else -> "bestvideo[vcodec^=avc]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
                    }
                    request.addOption("-f", formatStr)
                    request.addOption("--merge-output-format", "mp4")
                }'''

rep = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[height<=2160][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best[height<=2160]/best"
                        "High1440" -> "bestvideo[height<=1440][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best[height<=1440]/best"
                        "High1080" -> "bestvideo[height<=1080][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
                        "High720" -> "bestvideo[height<=720][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]/best"
                        "Medium480" -> "bestvideo[height<=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]/best"
                        "Medium360" -> "bestvideo[height<=360][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]/best"
                        "Low240" -> "bestvideo[height<=240][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=240]+bestaudio/best[height<=240]/best"
                        "Low144" -> "bestvideo[height<=144][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=144]+bestaudio/best[height<=144]/best"
                        else -> "bestvideo[vcodec^=avc]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
                    }
                    request.addOption("-f", formatStr)
                    request.addOption("--merge-output-format", "mkv")
                    request.addOption("--remux-video", "mp4")
                }'''

content = content.replace(target, rep)
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
