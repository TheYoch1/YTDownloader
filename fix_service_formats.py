with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

old_audio = """                if (item.settings.customFormatId != null) {
                    request.addOption("-f", item.settings.customFormatId!!)
                } else {
                    request.addOption("-f", "bestaudio")
                }"""

new_audio = """                if (item.settings.customFormatId != null && !item.isPlaylist) {
                    request.addOption("-f", item.settings.customFormatId!!)
                } else {
                    request.addOption("-f", "bestaudio")
                }"""
text = text.replace(old_audio, new_audio)

old_video = """            } else {
                if (item.settings.customFormatId != null) {
                    if (!item.settings.customFormatId!!.contains("+")) {
                        request.addOption("-f", "${item.settings.customFormatId}+bestaudio/best")
                    } else {
                        request.addOption("-f", item.settings.customFormatId!!)
                    }
                } else {
                    request.addOption("-f", "bestvideo+bestaudio/best")
                }"""

new_video = """            } else {
                if (item.isPlaylist && item.settings.selectedHeight > 0) {
                    request.addOption("-f", "bestvideo[height<=${item.settings.selectedHeight}]+bestaudio/best")
                } else if (item.settings.customFormatId != null) {
                    if (!item.settings.customFormatId!!.contains("+")) {
                        request.addOption("-f", "${item.settings.customFormatId}+bestaudio/best")
                    } else {
                        request.addOption("-f", item.settings.customFormatId!!)
                    }
                } else {
                    request.addOption("-f", "bestvideo+bestaudio/best")
                }"""
text = text.replace(old_video, new_video)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)
