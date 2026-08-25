import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

old_prog = """                            val globalProgress = if (it.isPlaylist && total > 0 && currentIndex > 0) {
                                ((currentIndex - 1).toFloat() / total.toFloat()) * 100f
                            } else {
                                progress
                            }"""

new_prog = """                            val globalProgress = if (it.isPlaylist && total > 0 && currentIndex > 0) {
                                (((currentIndex - 1).toFloat() * 100f) + progress) / total.toFloat()
                            } else {
                                progress
                            }"""

text = text.replace(old_prog, new_prog)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
