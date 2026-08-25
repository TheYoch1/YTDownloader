import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                        // Fallback for standard paths
                        val destDir = File(finalSaveDirStr)
                        if (!destDir.exists()) destDir.mkdirs()
                        val destFile = File(destDir, fileToCopy.name)
                        fileToCopy.copyTo(destFile, overwrite = true)
                        if (savedFileUri == null || (!fileToCopy.name.endsWith(".vtt") && !fileToCopy.name.endsWith(".srt"))) {
                            savedFileUri = "file://" + destFile.absolutePath
                        }'''

rep = '''                        // Fallback for standard paths
                        val destDir = File(finalSaveDirStr)
                        if (!destDir.exists()) destDir.mkdirs()
                        var destFile = File(destDir, fileToCopy.name)
                        if (destFile.exists()) {
                            val deleted = destFile.delete()
                            if (!deleted) {
                                val nameWithoutExtension = fileToCopy.nameWithoutExtension
                                val extension = fileToCopy.extension
                                destFile = File(destDir, "${nameWithoutExtension}_${System.currentTimeMillis()}.$extension")
                            }
                        }
                        fileToCopy.copyTo(destFile, overwrite = true)
                        if (savedFileUri == null || (!fileToCopy.name.endsWith(".vtt") && !fileToCopy.name.endsWith(".srt"))) {
                            savedFileUri = "file://" + destFile.absolutePath
                        }'''

content = content.replace(target, rep)

target2 = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[height<=2160][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best[height<=2160]/best"
                        "High1440" -> "bestvideo[height<=1440][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best[height<=1440]/best"
                        "High1080" -> "bestvideo[height<=1080][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
                        "High720" -> "bestvideo[height<=720][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]/best"
                        "Medium480" -> "bestvideo[height<=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]/best"
                        "Medium360" -> "bestvideo[height<=360][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]/best"
                        "Low240" -> "bestvideo[height<=240][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=240]+bestaudio/best[height<=240]/best"
                        "Low144" -> "bestvideo[height<=144][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=144]+bestaudio/best[height<=144]/best"
                        else -> "bestvideo[vcodec^=avc]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
                    }'''

rep2 = '''                    val formatStr = when (settings.quality.name) {
                        "High2160" -> "bestvideo[height<=2160][height>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=2160][height>=480]+bestaudio/best[height<=2160][height>=480]/best[height>=480]"
                        "High1440" -> "bestvideo[height<=1440][height>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1440][height>=480]+bestaudio/best[height<=1440][height>=480]/best[height>=480]"
                        "High1080" -> "bestvideo[height<=1080][height>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1080][height>=480]+bestaudio/best[height<=1080][height>=480]/best[height>=480]"
                        "High720" -> "bestvideo[height<=720][height>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=720][height>=480]+bestaudio/best[height<=720][height>=480]/best[height>=480]"
                        "Medium480" -> "bestvideo[height<=480][height>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=480][height>=480]+bestaudio/best[height<=480][height>=480]/best[height>=480]"
                        "Medium360" -> "bestvideo[height<=360][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]/best"
                        "Low240" -> "bestvideo[height<=240][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=240]+bestaudio/best[height<=240]/best"
                        "Low144" -> "bestvideo[height<=144][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=144]+bestaudio/best[height<=144]/best"
                        else -> "bestvideo[height>=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height>=480]+bestaudio/best[height>=480]"
                    }'''

content = content.replace(target2, rep2)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)

print(content.find(rep))
print(content.find(rep2))
