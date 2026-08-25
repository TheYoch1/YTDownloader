import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """    if (formatDialogUrl != null) {
        var isAudio by remember { mutableStateOf(false) }
        var selectedQuality by remember { mutableStateOf(VideoQuality.High1080) }
        var downloadSubtitles by remember { mutableStateOf(false) }
        
        AlertDialog(
            onDismissRequest = { formatDialogUrl = null },
            title = { Text("Download Options") },
            text = {
                Column {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RadioButton(selected = !isAudio, onClick = { isAudio = false })
                        Text("Video (MP4)")
                        Spacer(modifier = Modifier.width(16.dp))
                        RadioButton(selected = isAudio, onClick = { isAudio = true })
                        Text("Audio (MP3)")
                    }
                    if (!isAudio) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("Quality:")
                        LazyColumn(modifier = Modifier.height(150.dp)) {
                            items(VideoQuality.values()) { quality ->
                                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable { selectedQuality = quality }.fillMaxWidth()) {
                                    RadioButton(selected = selectedQuality == quality, onClick = { selectedQuality = quality })
                                    Text(quality.label)
                                }
                            }
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(checked = downloadSubtitles, onCheckedChange = { downloadSubtitles = it })
                            Text("Download English Subtitles")
                        }
                    } else {
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("Format will be MP3 (Best Quality)")
                    }
                }
            },"""

replacement = """    if (formatDialogUrl != null) {
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
        }
        
        AlertDialog(
            onDismissRequest = { formatDialogUrl = null },
            title = { Text("Download Options") },
            text = {
                if (isLoadingQualities) {
                    Column(
                        modifier = Modifier.fillMaxWidth().padding(16.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        CircularProgressIndicator()
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Fetching available qualities...")
                    }
                } else {
                    Column {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            RadioButton(selected = !isAudio, onClick = { isAudio = false })
                            Text("Video (MP4)")
                            Spacer(modifier = Modifier.width(16.dp))
                            RadioButton(selected = isAudio, onClick = { isAudio = true })
                            Text("Audio (MP3)")
                        }
                        if (!isAudio) {
                            Spacer(modifier = Modifier.height(8.dp))
                            Text("Quality:")
                            LazyColumn(modifier = Modifier.height(150.dp)) {
                                items(availableQualities ?: VideoQuality.values().toList()) { quality ->
                                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable { selectedQuality = quality }.fillMaxWidth()) {
                                        RadioButton(selected = selectedQuality == quality, onClick = { selectedQuality = quality })
                                        Text(quality.label)
                                    }
                                }
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Checkbox(checked = downloadSubtitles, onCheckedChange = { downloadSubtitles = it })
                                Text("Download English Subtitles")
                            }
                        } else {
                            Spacer(modifier = Modifier.height(8.dp))
                            Text("Format will be MP3 (Best Quality)")
                        }
                    }
                }
            },"""

content = content.replace(target, replacement)

# We also need to fix the confirm button to use selectedQuality, which is already there, but disable if loading
target_button = """            confirmButton = {
                Button(onClick = {
                    val customSettings = DownloadSettings("""

replacement_button = """            confirmButton = {
                Button(
                    enabled = !isLoadingQualities,
                    onClick = {
                    val customSettings = DownloadSettings("""

content = content.replace(target_button, replacement_button)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
