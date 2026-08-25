import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = '''            if (formatDialogUrl?.contains("list=") == true) {
                isAudio = false
                selectedQuality = VideoQuality.High720
                downloadSubtitles = settings.downloadSubtitles
            } else {
                downloadSubtitles = false
                if (!qualities.contains(selectedQuality)) {
                    selectedQuality = qualities.lastOrNull() ?: VideoQuality.High720
                }
            }'''

rep = '''            if (formatDialogUrl?.contains("list=") == true) {
                isAudio = false
                selectedQuality = VideoQuality.High720
                downloadSubtitles = settings.downloadSubtitles
            } else {
                downloadSubtitles = false
                if (qualities.isNotEmpty()) {
                    selectedQuality = qualities.find { it == selectedQuality } ?: qualities.lastOrNull() ?: VideoQuality.High720
                }
            }'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
