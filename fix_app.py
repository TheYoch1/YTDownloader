import re

# 1. Update Models.kt (AppConfig theme default to "System")
with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "r") as f:
    models_content = f.read()
models_content = models_content.replace('var theme: String = "Dark"', 'var theme: String = "System"')
with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "w") as f:
    f.write(models_content)


# 2. Update MainActivity.kt
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    main_content = f.read()

# Fix default 720p selection for playlists and single videos
old_selection_logic = """            if (formatDialogUrl?.contains("list=") == true) {
                isAudio = false
                selectedFormatId = null
                
            } else {
                downloadSubtitles = false
                if (qualities.isNotEmpty()) {
                    val defaultVideoFormat = qualities.find { it.height == 720 && !it.isAudioOnly }
                        ?: qualities.firstOrNull { !it.isAudioOnly }
                        ?: qualities.firstOrNull()
                    selectedFormatId = defaultVideoFormat?.formatId
                }
            }"""

new_selection_logic = """            isAudio = false
            downloadSubtitles = false
            if (qualities.isNotEmpty()) {
                val defaultVideoFormat = qualities.find { it.height == 720 && !it.isAudioOnly }
                    ?: qualities.firstOrNull { !it.isAudioOnly }
                    ?: qualities.firstOrNull()
                selectedFormatId = defaultVideoFormat?.formatId
            }"""
main_content = main_content.replace(old_selection_logic, new_selection_logic)

# Add Slider for max concurrent downloads
old_settings_ui = """            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Tag Audio File")"""

new_settings_ui = """            Text(text = "Max Concurrent Downloads: ${config.maxConcurrentDownloads}", modifier = Modifier.padding(top = 16.dp))
            androidx.compose.material3.Slider(
                value = config.maxConcurrentDownloads.toFloat(),
                onValueChange = { 
                    onConfigChanged(config.copy(maxConcurrentDownloads = it.toInt()))
                },
                valueRange = 1f..10f,
                steps = 8,
                modifier = Modifier.padding(bottom = 16.dp)
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Tag Audio File")"""
main_content = main_content.replace(old_settings_ui, new_settings_ui)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(main_content)


# 3. Update DownloadService.kt for History logging
with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    ds_content = f.read()

old_complete_log = """            DownloadRepository.updateQueue { q ->
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 100f, downloadSpeed = "Done", localFilePath = finalFileUri) else it }
            }
            cancelProgressNotification(id)
            showCompletionNotification("Completed: ${item.title}", "Download finished.", id)"""

new_complete_log = """            DownloadRepository.updateQueue { q ->
                q.map { if (it.id == id) it.copy(status = "Completed", progress = 100f, downloadSpeed = "Done", localFilePath = finalFileUri) else it }
            }
            try {
                val historyFile = File(app.filesDir, "history.log")
                val dateStr = java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(java.util.Date())
                historyFile.appendText("[$dateStr] Completed: ${item.title}\\n")
            } catch (e: Exception) {}
            cancelProgressNotification(id)
            showCompletionNotification("Completed: ${item.title}", "Download finished.", id)"""
ds_content = ds_content.replace(old_complete_log, new_complete_log)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(ds_content)

