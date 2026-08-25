import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Add progress notification in execute
old_execute = """                _downloadQueue.update { q -> 
                    q.map { 
                        if (it.id == id && it.status != "Cancelled" && it.status != "Paused") {
                            val currentIndex = if (newIndex != -1) newIndex else it.currentItemIndex
                            val total = if (newTotal != -1) newTotal else it.totalItems
                            val activeTitle = newTitle ?: it.currentItemTitle
                            
                            val globalProgress = if (it.isPlaylist && total > 0 && currentIndex > 0) {
                                ((currentIndex - 1).toFloat() / total.toFloat()) * 100f
                            } else {
                                progress
                            }
                            
                            it.copy(
                                progress = globalProgress, 
                                downloadSpeed = speed,
                                currentItemIndex = currentIndex,
                                totalItems = total,
                                currentItemTitle = activeTitle,
                                currentItemProgress = progress
                            )
                        } else it 
                    }
                }
            }"""

new_execute = """                _downloadQueue.update { q -> 
                    q.map { 
                        if (it.id == id && it.status != "Cancelled" && it.status != "Paused") {
                            val currentIndex = if (newIndex != -1) newIndex else it.currentItemIndex
                            val total = if (newTotal != -1) newTotal else it.totalItems
                            val activeTitle = newTitle ?: it.currentItemTitle
                            
                            val globalProgress = if (it.isPlaylist && total > 0 && currentIndex > 0) {
                                ((currentIndex - 1).toFloat() / total.toFloat()) * 100f
                            } else {
                                progress
                            }
                            
                            it.copy(
                                progress = globalProgress, 
                                downloadSpeed = speed,
                                currentItemIndex = currentIndex,
                                totalItems = total,
                                currentItemTitle = activeTitle,
                                currentItemProgress = progress
                            )
                        } else it 
                    }
                }
                
                val currentQ = _downloadQueue.value.find { it.id == id }
                if (currentQ != null && currentQ.status != "Cancelled" && currentQ.status != "Paused") {
                    showProgressNotification("Downloading ${currentQ.title}", "${currentQ.progress.toInt()}%", currentQ.progress, id.hashCode(), getPendingIntent())
                }
            }"""

text = text.replace(old_execute, new_execute)

# Add completion notification
old_completion = """            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 100f, downloadSpeed = "Done", localFilePath = finalFileUri) else it }
            }
            
        } catch (e: Exception) {"""

new_completion = """            _downloadQueue.update { q -> 
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 100f, downloadSpeed = "Done", localFilePath = finalFileUri) else it }
            }
            cancelProgressNotification(id.hashCode())
            showNotification("Completed: ${item.title}", "Download finished.", id.hashCode(), getPendingIntent())
            
        } catch (e: Exception) {"""

text = text.replace(old_completion, new_completion)

# Add error notification
old_error = """        } catch (e: Exception) {
            tmpDir?.deleteRecursively()
            val currentStatus = _downloadQueue.value.find { it.id == id }?.status
            if (currentStatus != "Cancelled" && currentStatus != "Paused") {
                val errorMsg = e.message ?: "Unknown error"
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id) it.copy(status = "Error", progress = 0f, downloadSpeed = "", errorMessage = errorMsg) else it }
                }
            }
        }"""

new_error = """        } catch (e: Exception) {
            tmpDir?.deleteRecursively()
            cancelProgressNotification(id.hashCode())
            val currentStatus = _downloadQueue.value.find { it.id == id }?.status
            if (currentStatus != "Cancelled" && currentStatus != "Paused") {
                val errorMsg = e.message ?: "Unknown error"
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id) it.copy(status = "Error", progress = 0f, downloadSpeed = "", errorMessage = errorMsg) else it }
                }
                showNotification("Error: ${item?.title ?: "Download"}", errorMsg, id.hashCode(), getPendingIntent())
            }
        }"""

text = text.replace(old_error, new_error)

# Add cancel notification
old_cancel = """    fun cancelDownload(id: String) {
        val item = _downloadQueue.value.find { it.id == id }"""

new_cancel = """    fun cancelDownload(id: String) {
        cancelProgressNotification(id.hashCode())
        val item = _downloadQueue.value.find { it.id == id }"""

text = text.replace(old_cancel, new_cancel)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
