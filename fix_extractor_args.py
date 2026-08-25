import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target1 = '''            val req = com.yausername.youtubedl_android.YoutubeDLRequest(url)
            req.addOption("--extractor-args", "youtube:player_client=android")
            val info = YoutubeDL.getInstance().getInfo(req)'''

rep1 = '''            val req = com.yausername.youtubedl_android.YoutubeDLRequest(url)
            req.addOption("--extractor-args", "youtube:player_client=android,web")
            val info = YoutubeDL.getInstance().getInfo(req)'''

content = content.replace(target1, rep1)

target2 = '''                val request = YoutubeDLRequest(url)
                request.addOption("--extractor-args", "youtube:player_client=android")'''

rep2 = '''                val request = YoutubeDLRequest(url)
                request.addOption("--extractor-args", "youtube:player_client=android,web")'''
                
content = content.replace(target2, rep2)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
