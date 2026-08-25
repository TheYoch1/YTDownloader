with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """    if (formatDialogUrl != null) {
        var isAudio by remember { mutableStateOf(false) }
        var selectedQuality by remember { mutableStateOf(VideoQuality.High1080) }
        var downloadSubtitles by remember { mutableStateOf(false) }
        var availableQualities by remember { mutableStateOf<List<VideoQuality>?>(null) }
        var isLoadingQualities by remember { mutableStateOf(true) }

        LaunchedEffect(formatDialogUrl) {
            isLoadingQualities = true
            val qualities = viewModel.fetchAvailableQualities(formatDialogUrl!!)
            availableQualities = qualities
            selectedQuality = qualities.lastOrNull() ?: VideoQuality.High1080
            isLoadingQualities = false
        }"""

replacement = """    if (formatDialogUrl != null) {
        var isAudio by remember(formatDialogUrl) { mutableStateOf(settings.audioOnly) }
        var selectedQuality by remember(formatDialogUrl) { mutableStateOf(settings.quality) }
        var downloadSubtitles by remember(formatDialogUrl) { mutableStateOf(settings.downloadSubtitles) }
        var availableQualities by remember { mutableStateOf<List<VideoQuality>?>(null) }
        var isLoadingQualities by remember(formatDialogUrl) { mutableStateOf(true) }

        LaunchedEffect(formatDialogUrl) {
            isLoadingQualities = true
            val qualities = viewModel.fetchAvailableQualities(formatDialogUrl!!)
            availableQualities = qualities
            
            if (formatDialogUrl?.contains("list=") == true) {
                isAudio = false
                selectedQuality = VideoQuality.High720
                downloadSubtitles = true
            } else {
                if (!qualities.contains(selectedQuality)) {
                    selectedQuality = qualities.lastOrNull() ?: VideoQuality.High1080
                }
            }
            
            isLoadingQualities = false
        }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
