import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = 'request.addOption("--merge-output-format", "mp4")'
rep = '''request.addOption("--merge-output-format", "mp4")
                request.addOption("--extractor-args", "youtube:player_client=android")'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
print("done")
