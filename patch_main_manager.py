with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

# Add progressMap collection
old_downloads = "val downloads by viewModel.downloads.collectAsStateWithLifecycle()"
new_downloads = """val downloads by viewModel.downloads.collectAsStateWithLifecycle()
            val individualProgressMap by DownloadManager.progressMap.collectAsStateWithLifecycle()"""
text = text.replace(old_downloads, new_downloads)

old_progress = "progress = { if (download.progress.isNaN()) 0f else (download.progress / 100f).coerceIn(0f, 1f) },"
new_progress = """progress = { 
                        val itemProgress = individualProgressMap[download.id] ?: download.progress
                        if (itemProgress.isNaN()) 0f else (itemProgress / 100f).coerceIn(0f, 1f) 
                    },"""
text = text.replace(old_progress, new_progress)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)

