import re
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

# Update fetchAvailableFormats call
old_fetch = """        LaunchedEffect(formatDialogUrl) {
            isLoadingQualities = true
            val qualities = viewModel.fetchAvailableFormats(formatDialogUrl!!)
            availableFormats = qualities
            
            if (formatDialogUrl?.contains("list=") == true) {
                isAudio = false
                selectedFormatId = null
                
            } else {
                downloadSubtitles = false
                if (qualities.isNotEmpty()) {
                    selectedFormatId = qualities.firstOrNull()?.formatId
                }
            }
            
            isLoadingQualities = false
        }"""

new_fetch = """        LaunchedEffect(formatDialogUrl) {
            isLoadingQualities = true
            val (title, qualities) = viewModel.fetchAvailableFormats(formatDialogUrl!!)
            formatDialogTitle = title
            availableFormats = qualities
            
            if (formatDialogUrl?.contains("list=") == true) {
                isAudio = false
                selectedFormatId = null
                
            } else {
                downloadSubtitles = false
                if (qualities.isNotEmpty()) {
                    selectedFormatId = qualities.firstOrNull()?.formatId
                }
            }
            
            isLoadingQualities = false
        }"""

text = text.replace(old_fetch, new_fetch)

# Update Click to Open file
# Find where the Download Item is constructed
# Wait, let's grep for 'if (download.status == "Completed")' or 'Card(' in DownloadItem or wherever it is.
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
