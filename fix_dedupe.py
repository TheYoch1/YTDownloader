import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                        var destFile = File(destDir, fileToCopy.name)
                        if (destFile.exists()) {
                            val deleted = destFile.delete()
                            if (!deleted) {
                                val nameWithoutExtension = fileToCopy.nameWithoutExtension
                                val extension = fileToCopy.extension
                                var counter = 1
                                do {
                                    destFile = File(destDir, "${nameWithoutExtension} ($counter).$extension")
                                    counter++
                                } while (destFile.exists())
                            }
                        }
                        fileToCopy.copyTo(destFile, overwrite = true)'''

rep = '''                        var destFile = File(destDir, fileToCopy.name)
                        if (destFile.exists()) {
                            val nameWithoutExtension = fileToCopy.nameWithoutExtension
                            val extension = fileToCopy.extension
                            var counter = 1
                            do {
                                destFile = File(destDir, "${nameWithoutExtension} ($counter).$extension")
                                counter++
                            } while (destFile.exists())
                        }
                        fileToCopy.copyTo(destFile, overwrite = false)'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
print("done dedupe")
