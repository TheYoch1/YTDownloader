with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

old_sort = """    fun sortQueue(sortType: String) {
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
    }"""

new_sort = """    fun sortQueue(sortType: String) {
        DownloadRepository.updateQueue { q ->
            when (sortType) {
                "Alphabetical" -> q.sortedBy { it.title.lowercase() }
                "Newest First" -> q.sortedByDescending { it.timestamp }
                "Oldest First" -> q.sortedBy { it.timestamp }
                else -> q
            }
        }
        saveQueue()
    }"""

text = text.replace(old_sort, new_sort)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
