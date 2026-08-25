import re
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

playlist_opt = """            if (item.isPlaylist) {
                request.addOption("--yes-playlist")
            } else {
                request.addOption("--no-playlist")
            }
            
            // Name format natively handled by yt-dlp to fix issues"""

text = text.replace("            // Name format natively handled by yt-dlp to fix issues", playlist_opt)

old_callback = """            YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->
                val speed = if (etaInSeconds > 0) "ETA: ${etaInSeconds}s" else ""
                _downloadQueue.update { q -> 
                    q.map { if (it.id == id && it.status != "Cancelled" && it.status != "Paused") it.copy(progress = progress, downloadSpeed = speed) else it }
                }
            }"""

new_callback = """            YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->
                val speed = if (etaInSeconds > 0) "ETA: ${etaInSeconds}s" else ""
                
                var newIndex = -1
                var newTotal = -1
                var newTitle: String? = null
                
                val matchPlaylist = Regex("\\[download\\] Downloading video (\\\\d+) of (\\\\d+)").find(line)
                if (matchPlaylist != null) {
                    newIndex = matchPlaylist.groupValues[1].toInt()
                    newTotal = matchPlaylist.groupValues[2].toInt()
                }
                
                if (line.contains("[download] Destination: ")) {
                    val dest = line.substringAfter("[download] Destination: ")
                    newTitle = File(dest).nameWithoutExtension
                } else if (line.contains("has already been downloaded")) {
                    val dest = line.substringAfter("[download] ").substringBefore(" has already been")
                    newTitle = File(dest).nameWithoutExtension
                }

                _downloadQueue.update { q -> 
                    q.map { 
                        if (it.id == id && it.status != "Cancelled" && it.status != "Paused") {
                            it.copy(
                                progress = progress, 
                                downloadSpeed = speed,
                                currentItemIndex = if (newIndex != -1) newIndex else it.currentItemIndex,
                                totalItems = if (newTotal != -1) newTotal else it.totalItems,
                                currentItemTitle = newTitle ?: it.currentItemTitle
                            )
                        } else it 
                    }
                }
            }"""

text = text.replace(old_callback, new_callback)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
