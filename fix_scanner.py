import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """                    listOf(
                        "/storage/emulated/0/Download/YT Downloader",
                        "/storage/emulated/0/Movies/YT Downloader",
                        "/storage/emulated/0/Music/YT Downloader"
                    ).forEach { path ->"""

rep = """                    listOf(
                        "/storage/emulated/0/Download/YT Downloader"
                    ).forEach { path ->"""

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
