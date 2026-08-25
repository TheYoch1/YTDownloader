import sys

with open('app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt', 'r') as f:
    content = f.read()

import_statement = "import android.os.Environment\n"
if "import android.os.Environment" not in content:
    content = content.replace("import android.net.Uri", "import android.os.Environment\nimport android.net.Uri")

save_logic_old = '''                // Finished downloading to tmpDir. Copy to actual save location.
                val saveDir = _appConfig.value.saveDirectory
                if (saveDir.startsWith("content://")) {
                    val treeUri = Uri.parse(saveDir)
                    val docFile = DocumentFile.fromTreeUri(application, treeUri)
                    tmpDir?.listFiles()?.forEach { fileToCopy ->
                        if (docFile != null) {
                            var mimeType = "application/octet-stream"
                            if (fileToCopy.name.endsWith(".mp3") || fileToCopy.name.endsWith(".m4a")) mimeType = "audio/*"
                            else if (fileToCopy.name.endsWith(".mp4") || fileToCopy.name.endsWith(".webm") || fileToCopy.name.endsWith(".mkv")) mimeType = "video/*"
                            
                            val newFile = docFile.createFile(mimeType, fileToCopy.name)
                            if (newFile != null) {
                                application.contentResolver.openOutputStream(newFile.uri)?.use { out ->
                                    fileToCopy.inputStream().use { input ->
                                        input.copyTo(out)
                                    }
                                }
                            }
                        }
                    }
                }'''

save_logic_new = '''                // Finished downloading to tmpDir. Copy to actual save location.
                val saveDir = _appConfig.value.saveDirectory
                tmpDir?.listFiles()?.forEach { fileToCopy ->
                    if (saveDir.startsWith("content://")) {
                        val treeUri = Uri.parse(saveDir)
                        val docFile = DocumentFile.fromTreeUri(application, treeUri)
                        if (docFile != null) {
                            var mimeType = "application/octet-stream"
                            if (fileToCopy.name.endsWith(".mp3") || fileToCopy.name.endsWith(".m4a")) mimeType = "audio/*"
                            else if (fileToCopy.name.endsWith(".mp4") || fileToCopy.name.endsWith(".webm") || fileToCopy.name.endsWith(".mkv")) mimeType = "video/*"
                            
                            val newFile = docFile.createFile(mimeType, fileToCopy.name)
                            if (newFile != null) {
                                application.contentResolver.openOutputStream(newFile.uri)?.use { out ->
                                    fileToCopy.inputStream().use { input ->
                                        input.copyTo(out)
                                    }
                                }
                            }
                        }
                    } else {
                        // Fallback for standard paths
                        val destDir = File(saveDir)
                        if (!destDir.exists()) destDir.mkdirs()
                        val destFile = File(destDir, fileToCopy.name)
                        fileToCopy.copyTo(destFile, overwrite = true)
                    }
                }'''

content = content.replace(save_logic_old, save_logic_new)

with open('app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt', 'w') as f:
    f.write(content)
