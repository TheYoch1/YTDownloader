import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

old_audio = """            if (item.settings.audioOnly) {
                request.addOption("-x")
                request.addOption("--audio-format", item.settings.saveFormat)
                if (item.settings.customFormatId != null) {
                    request.addOption("-f", item.settings.customFormatId!!)
                } else {
                    request.addOption("-f", "bestaudio")
                }
            }"""

new_audio = """            if (item.settings.audioOnly) {
                request.addOption("-x")
                request.addOption("--audio-format", item.settings.saveFormat)
                if (item.settings.saveFormat == "mp3") {
                    request.addOption("--audio-quality", "0")
                }
                if (item.settings.customFormatId != null) {
                    request.addOption("-f", item.settings.customFormatId!!)
                } else {
                    request.addOption("-f", "bestaudio")
                }
            }"""

text = text.replace(old_audio, new_audio)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)

