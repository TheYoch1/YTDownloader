import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target_format = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[res<=2160]+bestaudio/best[res<=2160]/best"
                        "High1440" -> "bestvideo[res<=1440]+bestaudio/best[res<=1440]/best"
                        "High1080" -> "bestvideo[res<=1080]+bestaudio/best[res<=1080]/best"
                        "High720" -> "bestvideo[res<=720]+bestaudio/best[res<=720]/best"
                        "Medium480" -> "bestvideo[res<=480]+bestaudio/best[res<=480]/best"
                        "Medium360" -> "bestvideo[res<=360]+bestaudio/best[res<=360]/best"
                        "Low240" -> "bestvideo[res<=240]+bestaudio/best[res<=240]/best"
                        "Low144" -> "bestvideo[res<=144]+bestaudio/best[res<=144]/best"
                        else -> "bestvideo+bestaudio/best"
                    }
                    request.addOption("-f", formatStr)
                    request.addOption("--merge-output-format", "mkv")
                    request.addOption("--remux-video", "mp4")'''

rep_format = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[res<=2160][ext=mp4]+bestaudio[ext=m4a]/best[res<=2160][ext=mp4]/best"
                        "High1440" -> "bestvideo[res<=1440][ext=mp4]+bestaudio[ext=m4a]/best[res<=1440][ext=mp4]/best"
                        "High1080" -> "bestvideo[res<=1080][ext=mp4]+bestaudio[ext=m4a]/best[res<=1080][ext=mp4]/best"
                        "High720" -> "bestvideo[res<=720][ext=mp4]+bestaudio[ext=m4a]/best[res<=720][ext=mp4]/best"
                        "Medium480" -> "bestvideo[res<=480][ext=mp4]+bestaudio[ext=m4a]/best[res<=480][ext=mp4]/best"
                        "Medium360" -> "bestvideo[res<=360][ext=mp4]+bestaudio[ext=m4a]/best[res<=360][ext=mp4]/best"
                        "Low240" -> "bestvideo[res<=240][ext=mp4]+bestaudio[ext=m4a]/best[res<=240][ext=mp4]/best"
                        "Low144" -> "bestvideo[res<=144][ext=mp4]+bestaudio[ext=m4a]/best[res<=144][ext=mp4]/best"
                        else -> "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                    }
                    request.addOption("-f", formatStr)'''

content = content.replace(target_format, rep_format)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/aistudio/ytdownloader/YTDownloaderApp.kt", "r") as f:
    app_content = f.read()

app_content = app_content.replace("YoutubeDL.UpdateChannel.STABLE", "YoutubeDL.UpdateChannel.NIGHTLY")
with open("app/src/main/java/com/aistudio/ytdownloader/YTDownloaderApp.kt", "w") as f:
    f.write(app_content)

print("done")
