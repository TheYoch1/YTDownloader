import re

# 1. Update MainActivity for multi URL and Queue display
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    main = f.read()

main = main.replace("singleLine = true", "maxLines = 5")

confirm_target = """                    val customSettings = DownloadSettings(
                        audioOnly = isAudio,
                        quality = selectedQuality,
                        downloadSubtitles = downloadSubtitles,
                        saveFormat = "mp3"
                    )
                    viewModel.addDownload(formatDialogUrl!!, formatDialogTitle, customSettings)
                    urlInput = \"\""""
confirm_rep = """                    val customSettings = DownloadSettings(
                        audioOnly = isAudio,
                        quality = selectedQuality,
                        downloadSubtitles = downloadSubtitles,
                        saveFormat = "mp3"
                    )
                    val urls = formatDialogUrl!!.split(Regex("\\\\s+")).filter { it.isNotBlank() && (it.startsWith("http://") || it.startsWith("https://") || it.contains("youtu")) }
                    if (urls.size > 1) {
                        urls.forEach { u ->
                            viewModel.addDownload(u, null, customSettings)
                        }
                    } else {
                        viewModel.addDownload(formatDialogUrl!!.trim(), formatDialogTitle, customSettings)
                    }
                    urlInput = \"\""""
main = main.replace(confirm_target, confirm_rep)

# Ensure "Finished" or "Completed" stay in the queue
# We look for where activeDownloads is filtered
active_target = """    val activeDownloads = downloadQueue.filter { it.status != "Completed" && it.status != "Cancelled" }"""
active_rep = """    val activeDownloads = downloadQueue.filter { it.status != "Cancelled" }"""
main = main.replace(active_target, active_rep)

# Modify History/Storage Saved view
history_target = """            Text(
                "App Settings",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )"""
history_rep = """            Text(
                "App Settings",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )"""
# Wait, user wants to "the history option should not be how it is change it and take away storage saved"
# Let's remove the storage saved chart from the Dashboard/History completely
# I need to find the Storage Saved section in MainActivity
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(main)

