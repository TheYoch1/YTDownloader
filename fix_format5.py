import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                    val formatStr = when (settings.quality.name) {
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
                    // request.addOption("--merge-output-format", "mp4") // removed to prevent transcoding failures
                }'''

rep = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                        "High1440" -> "bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                        "High1080" -> "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                        "High720" -> "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                        "Medium480" -> "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                        "Medium360" -> "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                        "Low240" -> "bestvideo[height<=240][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                        "Low144" -> "bestvideo[height<=144][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                        else -> "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                    }
                    request.addOption("-f", formatStr)
                    request.addOption("--merge-output-format", "mp4")
                }'''

content = content.replace(target, rep)
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
