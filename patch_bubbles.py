with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target1 = 'onConfigChanged(config.copy(saveDirectory = "/storage/emulated/0/Download"))'
rep1 = 'onConfigChanged(config.copy(saveDirectory = "/storage/emulated/0/Download/YT Downloader"))'

target2 = 'onConfigChanged(config.copy(saveDirectory = "/storage/emulated/0/Movies"))'
rep2 = 'onConfigChanged(config.copy(saveDirectory = "/storage/emulated/0/Movies/YT Downloader"))'

target3 = 'onConfigChanged(config.copy(saveDirectory = "/storage/emulated/0/Music"))'
rep3 = 'onConfigChanged(config.copy(saveDirectory = "/storage/emulated/0/Music/YT Downloader"))'

content = content.replace(target1, rep1).replace(target2, rep2).replace(target3, rep3)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
