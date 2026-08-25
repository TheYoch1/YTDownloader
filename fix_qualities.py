import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''            val maxHeight = heights.maxOrNull() ?: 1080
            VideoQuality.values().filter { it.label.replace("p", "").toInt() <= maxHeight }'''

rep = '''            val maxHeight = heights.maxOrNull() ?: 1080
            val filtered = VideoQuality.values().filter { it.label.replace("p", "").toInt() <= maxHeight }
            if (filtered.isEmpty()) VideoQuality.values().toList() else filtered'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
