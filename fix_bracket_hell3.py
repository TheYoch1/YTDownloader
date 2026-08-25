import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Just literally find the catch and finally block and rewrite it
catch_start = text.find("        } catch (e: Exception) {")
if catch_start != -1:
    cancel_start = text.find("    fun cancelDownload(id: String) {")
    top_half = text[:catch_start]
    
    clean_catch = """        } catch (e: Exception) {
            tmpDir?.deleteRecursively()
            val currentStatus = _downloadQueue.value.find { it.id == id }?.status
            if (currentStatus == "Cancelled") {
                // already handled
            } else if (currentStatus == "Paused") {
                // keep paused
            } else {
                val errorMsg = e.message ?: e.cause?.message ?: "Unknown error occurred"
                logError(errorMsg)
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id) it.copy(status = "Error", progress = 0f, downloadSpeed = "", errorMessage = errorMsg) else it } 
                }
                val item = _downloadQueue.value.find { it.id == id }
                val typeStr = if (item?.isPlaylist == true) "Playlist" else "Video"
                val intent = android.content.Intent(application, MainActivity::class.java).apply {
                    flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TASK
                }
                val flags = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
                    android.app.PendingIntent.FLAG_IMMUTABLE or android.app.PendingIntent.FLAG_UPDATE_CURRENT
                } else {
                    android.app.PendingIntent.FLAG_UPDATE_CURRENT
                }
                val pendingIntent = android.app.PendingIntent.getActivity(application, id.hashCode(), intent, flags)
                showNotification("$typeStr Download Failed", "${item?.title} encountered an error: $errorMsg", id.hashCode(), pendingIntent)
            }
        } finally {
            stopForegroundServiceIfDone()
        }
    }
"""
    with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
        f.write(top_half + clean_catch + text[cancel_start:])
        
