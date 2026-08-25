with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                tmpDir?.walkTopDown()?.filter { it.isFile }?.forEach { fileToCopy ->'''

rep = '''                var savedFileUri: String? = null
                tmpDir?.walkTopDown()?.filter { it.isFile }?.forEach { fileToCopy ->'''

content = content.replace(target, rep)

target_create_file = '''                            if (newFile != null) {
                                application.contentResolver.openOutputStream(newFile.uri)?.use { out ->
                                    fileToCopy.inputStream().use { input ->
                                        input.copyTo(out)
                                    }
                                }
                            }'''

rep_create_file = '''                            if (newFile != null) {
                                application.contentResolver.openOutputStream(newFile.uri)?.use { out ->
                                    fileToCopy.inputStream().use { input ->
                                        input.copyTo(out)
                                    }
                                }
                                if (savedFileUri == null || (!fileToCopy.name.endsWith(".vtt") && !fileToCopy.name.endsWith(".srt"))) {
                                    savedFileUri = newFile.uri.toString()
                                }
                            }'''
content = content.replace(target_create_file, rep_create_file)

target_fallback = '''                        fileToCopy.copyTo(destFile, overwrite = true)'''
rep_fallback = '''                        fileToCopy.copyTo(destFile, overwrite = true)
                        if (savedFileUri == null || (!fileToCopy.name.endsWith(".vtt") && !fileToCopy.name.endsWith(".srt"))) {
                            savedFileUri = "file://" + destFile.absolutePath
                        }'''
content = content.replace(target_fallback, rep_fallback)

target_completion = '''            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 1f, downloadSpeed = "") else it } 
            }
            
            val typeStr = if (isPlaylist) "Playlist" else "Video"
            showNotification("$typeStr Download Complete", "$titleStr has finished downloading.", id.hashCode())'''

rep_completion = '''            if (isPlaylist && finalSaveDirStr.startsWith("content://")) {
                savedFileUri = finalSaveDirStr // For playlists, link to the folder
            }
            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 1f, downloadSpeed = "", localFilePath = savedFileUri) else it } 
            }
            
            val typeStr = if (isPlaylist) "Playlist" else "Video"
            var pendingIntent: android.app.PendingIntent? = null
            if (savedFileUri != null) {
                val intent = android.content.Intent(android.content.Intent.ACTION_VIEW)
                val uri = Uri.parse(savedFileUri)
                if (savedFileUri!!.startsWith("content://") && isPlaylist) {
                    intent.data = uri
                } else if (savedFileUri!!.startsWith("file://")) {
                    val file = java.io.File(uri.path!!)
                    val contentUri = androidx.core.content.FileProvider.getUriForFile(application, "${application.packageName}.provider", file)
                    val mime = if (savedFileUri!!.endsWith(".mp4") || savedFileUri!!.endsWith(".webm") || savedFileUri!!.endsWith(".mkv")) "video/*" else "audio/*"
                    intent.setDataAndType(contentUri, mime)
                    intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                } else {
                    val mime = if (savedFileUri!!.endsWith(".mp4") || savedFileUri!!.endsWith(".webm") || savedFileUri!!.endsWith(".mkv")) "video/*" else "audio/*"
                    intent.setDataAndType(uri, mime)
                    intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                }
                
                val flags = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
                    android.app.PendingIntent.FLAG_IMMUTABLE or android.app.PendingIntent.FLAG_UPDATE_CURRENT
                } else {
                    android.app.PendingIntent.FLAG_UPDATE_CURRENT
                }
                pendingIntent = android.app.PendingIntent.getActivity(application, id.hashCode(), intent, flags)
            }
            
            showNotification("$typeStr Download Complete", "$titleStr has finished downloading.", id.hashCode(), pendingIntent)'''

content = content.replace(target_completion, rep_completion)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
