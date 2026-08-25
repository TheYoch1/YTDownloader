import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

# Add --force-overwrites
target_options = '''                request.addOption("--retries", "infinite")'''
rep_options = '''                request.addOption("--force-overwrites")
                request.addOption("--retries", "infinite")'''
content = content.replace(target_options, rep_options)

# Update execute block
target_exec = '''                YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->
                    var currentStatus = _downloadQueue.value.find { it.id == id }?.status
                    if (currentStatus == "Cancelled") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else if (currentStatus == "Paused") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else {
                        val speedStr = if (etaInSeconds > 0) "${etaInSeconds}s left" else ""
                        _downloadQueue.update { q -> 
                            q.map { if (it.id == id) it.copy(progress = progress / 100f, downloadSpeed = speedStr) else it } 
                        }
                        updateNotificationProgress(id, titleStr, progress / 100f, speedStr)
                    }
                }'''

rep_exec = '''                var currentItemTitle = titleStr
                YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->
                    if (isPlaylist && line != null && line.contains("[download] Destination: ")) {
                        val fileName = line.substringAfter("[download] Destination: ").substringAfterLast("/")
                        currentItemTitle = fileName
                    }
                    var currentStatus = _downloadQueue.value.find { it.id == id }?.status
                    if (currentStatus == "Cancelled") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else if (currentStatus == "Paused") {
                        YoutubeDL.getInstance().destroyProcessById(id)
                    } else {
                        val speedStr = if (etaInSeconds > 0) "${etaInSeconds}s left" else ""
                        val displayTitle = if (isPlaylist) currentItemTitle else titleStr
                        _downloadQueue.update { q -> 
                            q.map { if (it.id == id) it.copy(title = displayTitle, progress = progress / 100f, downloadSpeed = speedStr) else it } 
                        }
                        updateNotificationProgress(id, displayTitle, progress / 100f, speedStr)
                    }
                }'''

content = content.replace(target_exec, rep_exec)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
