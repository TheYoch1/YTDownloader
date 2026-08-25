import re

with open("/app/applet/app/src/main/java/com/aistudio/ytdownloader/YTDownloaderApp.kt", "r") as f:
    content = f.read()

target1 = '''    private fun extractFFmpeg() {
        try {
            val internalFfmpeg = java.io.File(filesDir, "ffmpeg")
            if (!internalFfmpeg.exists()) {
                val inputStream = assets.open("ffmpeg")
                val outputStream = java.io.FileOutputStream(internalFfmpeg)
                inputStream.copyTo(outputStream)
                inputStream.close()
                outputStream.close()
            }
            internalFfmpeg.setExecutable(true, false)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    @OptIn(DelicateCoroutinesApi::class)'''

rep1 = '''    @OptIn(DelicateCoroutinesApi::class)'''

content = content.replace(target1, rep1)

target2 = '''        super.onCreate()
        try {
            extractFFmpeg()
            YoutubeDL.getInstance().init(this)'''

rep2 = '''        super.onCreate()
        try {
            YoutubeDL.getInstance().init(this)'''

content = content.replace(target2, rep2)

with open("/app/applet/app/src/main/java/com/aistudio/ytdownloader/YTDownloaderApp.kt", "w") as f:
    f.write(content)
