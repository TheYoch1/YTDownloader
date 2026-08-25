with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

sort_func = """    fun sortQueue(sortType: String) {
        DownloadRepository.updateQueue { q ->
            when (sortType) {
                "Alphabetical" -> q.sortedBy { it.title.lowercase() }
                "Newest First" -> q.reversed() // Assumes the list was appended to, wait, we don't have timestamps. The user can drag and drop. 
                // Let's just reverse it for 'Newest First' / 'Oldest First' if we don't have timestamps?
                // Actually, if we just reverse, it toggles. But wait. Let's add timestamp to QueuedDownload!
                else -> q
            }
        }
        saveQueue()
    }
"""
text = text.replace("fun reorderQueue(fromIndex: Int, toIndex: Int) {", sort_func + "\n    fun reorderQueue(fromIndex: Int, toIndex: Int) {")
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
