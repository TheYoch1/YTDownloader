with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

old_sig = """fun DownloadItemCard(
    download: QueuedDownload,
    onRemove: () -> Unit,
    onCancel: () -> Unit,
    onPause: () -> Unit,
    onResume: () -> Unit,
    onRetry: () -> Unit,
    dragModifier: Modifier = Modifier
) {"""

new_sig = """fun DownloadItemCard(
    download: QueuedDownload,
    individualProgress: Float? = null,
    onRemove: () -> Unit,
    onCancel: () -> Unit,
    onPause: () -> Unit,
    onResume: () -> Unit,
    onRetry: () -> Unit,
    dragModifier: Modifier = Modifier
) {"""

text = text.replace(old_sig, new_sig)

old_progress = """progress = { 
                        val itemProgress = individualProgressMap[download.id] ?: download.progress
                        if (itemProgress.isNaN()) 0f else (itemProgress / 100f).coerceIn(0f, 1f) 
                    },"""

new_progress = """progress = { 
                        val itemProgress = individualProgress ?: download.progress
                        if (itemProgress.isNaN()) 0f else (itemProgress / 100f).coerceIn(0f, 1f) 
                    },"""
text = text.replace(old_progress, new_progress)

old_call = """DownloadItemCard(
                                        download = download,"""
new_call = """DownloadItemCard(
                                        download = download,
                                        individualProgress = individualProgressMap[download.id],"""

text = text.replace(old_call, new_call)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)

