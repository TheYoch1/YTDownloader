import re
import os

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Add imports
imports_to_add = """import androidx.compose.ui.text.input.ImeAction
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import java.io.File
"""
if "ImeAction" not in content:
    content = content.replace("import androidx.compose.foundation.shape.RoundedCornerShape", "import androidx.compose.foundation.shape.RoundedCornerShape\n" + imports_to_add)

# 2. State variables inside MainScreen
state_target = """    var showSettings by remember { mutableStateOf(false) }"""
state_replacement = """    var showSettings by remember { mutableStateOf(false) }
    var formatDialogUrl by remember { mutableStateOf<String?>(null) }
    var formatDialogTitle by remember { mutableStateOf<String?>(null) }
    var showErrorLog by remember { mutableStateOf(false) }
    val keyboardController = LocalSoftwareKeyboardController.current
    val context = LocalContext.current"""
if "formatDialogUrl" not in content:
    content = content.replace(state_target, state_replacement)

# 3. OutlinedTextField
textfield_target = """                    OutlinedTextField(
                        value = urlInput,
                        onValueChange = { 
                            urlInput = it 
                            if (it.isBlank()) {
                                searchResults = emptyList()
                                searchError = null
                            }
                        },
                        label = { Text("YouTube URL or Search Query") },
                        modifier = Modifier.weight(1f),
                        singleLine = true,
                        leadingIcon = {
                            Icon(if (isUrl || urlInput.isBlank()) Icons.Default.Link else Icons.Default.Search, contentDescription = "Input Icon")
                        },
                        trailingIcon = {
                            if (urlInput.isNotEmpty()) {
                                IconButton(onClick = { 
                                    urlInput = ""
                                    searchResults = emptyList()
                                    searchError = null
                                }) {
                                    Icon(Icons.Default.Clear, contentDescription = "Clear")
                                }
                            }
                        }
                    )"""
textfield_replacement = """                    OutlinedTextField(
                        value = urlInput,
                        onValueChange = { 
                            urlInput = it 
                            if (it.isBlank()) {
                                searchResults = emptyList()
                                searchError = null
                            }
                        },
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                        keyboardActions = KeyboardActions(onSearch = {
                            keyboardController?.hide()
                            if (isUrl) {
                                formatDialogUrl = urlInput
                                formatDialogTitle = null
                            } else {
                                isSearchLoading = true
                                searchError = null
                                coroutineScope.launch {
                                    try {
                                        searchResults = searchYouTubeVideos(urlInput)
                                    } catch (e: Exception) {
                                        searchError = e.message
                                    } finally {
                                        isSearchLoading = false
                                    }
                                }
                            }
                        }),
                        label = { Text("YouTube URL or Search Query") },
                        modifier = Modifier.weight(1f),
                        singleLine = true,
                        leadingIcon = {
                            Icon(if (isUrl || urlInput.isBlank()) Icons.Default.Link else Icons.Default.Search, contentDescription = "Input Icon")
                        },
                        trailingIcon = {
                            if (urlInput.isNotEmpty()) {
                                IconButton(onClick = { 
                                    urlInput = ""
                                    searchResults = emptyList()
                                    searchError = null
                                }) {
                                    Icon(Icons.Default.Clear, contentDescription = "Clear")
                                }
                            }
                        }
                    )"""
content = content.replace(textfield_target, textfield_replacement)

# 4. Search/Add Button
button_target = """                    Button(
                        onClick = {
                            if (isUrl) {
                                viewModel.addDownload(urlInput)
                                urlInput = ""
                                searchResults = emptyList()
                            } else {
                                isSearchLoading = true
                                searchError = null
                                coroutineScope.launch {
                                    try {
                                        searchResults = searchYouTubeVideos(urlInput)
                                    } catch (e: Exception) {
                                        searchError = e.message
                                    } finally {
                                        isSearchLoading = false
                                    }
                                }
                            }
                        },"""
button_replacement = """                    Button(
                        onClick = {
                            keyboardController?.hide()
                            if (isUrl) {
                                formatDialogUrl = urlInput
                                formatDialogTitle = null
                            } else {
                                isSearchLoading = true
                                searchError = null
                                coroutineScope.launch {
                                    try {
                                        searchResults = searchYouTubeVideos(urlInput)
                                    } catch (e: Exception) {
                                        searchError = e.message
                                    } finally {
                                        isSearchLoading = false
                                    }
                                }
                            }
                        },"""
content = content.replace(button_target, button_replacement)

# 5. Search Results Click
search_click_target = """                                        modifier = Modifier.clickable {
                                            viewModel.addDownload(result.url, result.title)
                                            urlInput = ""
                                            searchResults = emptyList()
                                        },"""
search_click_replacement = """                                        modifier = Modifier.clickable {
                                            formatDialogUrl = result.url
                                            formatDialogTitle = result.title
                                        },"""
content = content.replace(search_click_target, search_click_replacement)

# 6. Remove Quick Settings from MainScreen (optional, but requested options dialog replaces it, we can leave it or remove it)
quick_settings_target = """                // Quick Settings (Format and Quality) right before adding
                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RadioButton(
                            selected = !settings.audioOnly,
                            onClick = { viewModel.updateSettings(settings.copy(audioOnly = false)) }
                        )
                        Text("Video", style = MaterialTheme.typography.bodySmall)
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RadioButton(
                            selected = settings.audioOnly,
                            onClick = { viewModel.updateSettings(settings.copy(audioOnly = true)) }
                        )
                        Text("Audio", style = MaterialTheme.typography.bodySmall)
                    }
                    Spacer(modifier = Modifier.weight(1f))
                    IconButton(onClick = { showSettings = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                }"""
quick_settings_replacement = """                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                    horizontalArrangement = Arrangement.End
                ) {
                    IconButton(onClick = { showSettings = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                }"""
content = content.replace(quick_settings_target, quick_settings_replacement)

# 7. Add Format Dialog inside Scaffold (bottom)
scaffold_bottom_target = """    if (showSettings) {"""
format_dialog_code = """
    if (formatDialogUrl != null) {
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
            },
            confirmButton = {
                Button(onClick = {
                    val customSettings = DownloadSettings(
                        audioOnly = isAudio,
                        quality = selectedQuality,
                        downloadSubtitles = downloadSubtitles,
                        saveFormat = "mp3"
                    )
                    viewModel.addDownload(formatDialogUrl!!, formatDialogTitle, customSettings)
                    urlInput = ""
                    searchResults = emptyList()
                    formatDialogUrl = null
                    formatDialogTitle = null
                }) {
                    Text("Download")
                }
            },
            dismissButton = {
                TextButton(onClick = { formatDialogUrl = null }) { Text("Cancel") }
            }
        )
    }
    
    if (showErrorLog) {
        AlertDialog(
            onDismissRequest = { showErrorLog = false },
            title = { Text("Error Log") },
            text = {
                val errorFile = File(context.filesDir, "error_log.txt")
                val logText = if (errorFile.exists()) errorFile.readText() else "No errors recorded."
                val clipboardManager = LocalClipboardManager.current
                
                LazyColumn {
                    item {
                        Text(
                            text = logText, 
                            style = MaterialTheme.typography.bodySmall,
                            modifier = Modifier.pointerInput(Unit) {
                                detectTapGestures(
                                    onLongPress = {
                                        clipboardManager.setText(AnnotatedString(logText))
                                    }
                                )
                            }
                        )
                    }
                }
            },
            confirmButton = {
                Button(onClick = { showErrorLog = false }) { Text("Close") }
            },
            dismissButton = {
                TextButton(onClick = {
                    File(context.filesDir, "error_log.txt").delete()
                    showErrorLog = false
                }) { Text("Clear Log") }
            }
        )
    }

    if (showSettings) {"""
content = content.replace(scaffold_bottom_target, format_dialog_code)


# 8. DownloadItem Error Text click-to-copy
error_item_target = """        if (download.status == "Error" && download.errorMessage != null) {
                Text(
                    text = download.errorMessage ?: "",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.error,
                    modifier = Modifier.padding(bottom = 8.dp)
                )
            }"""
error_item_replacement = """        if (download.status == "Error" && download.errorMessage != null) {
                val clipboardManager = LocalClipboardManager.current
                Text(
                    text = download.errorMessage ?: "",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.error,
                    modifier = Modifier.padding(bottom = 8.dp).pointerInput(Unit) {
                        detectTapGestures(
                            onLongPress = {
                                clipboardManager.setText(AnnotatedString(download.errorMessage ?: ""))
                            }
                        )
                    }
                )
            }"""
content = content.replace(error_item_target, error_item_replacement)


# 9. Add Error Log Button in Settings
settings_bottom_target = """            Button(
                onClick = onDismiss,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Done")
            }"""
settings_bottom_replacement = """            TextButton(
                onClick = { onDismiss(); }, // Needs to trigger showErrorLog, but we don't have access to it directly from here easily without a callback. Let's just add it to MainActivity's main menu or pass a callback. 
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("View Error Log")
            }
            Button(
                onClick = onDismiss,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Done")
            }"""

# Wait, instead of hacking it in SettingsBottomSheet without a callback, I will add an `onViewErrorLog: () -> Unit` parameter.
settings_func_target = """@Composable
fun SettingsBottomSheet(
    settings: DownloadSettings,
    config: AppConfig,
    onDismiss: () -> Unit,
    onSettingsChanged: (DownloadSettings) -> Unit,
    onConfigChanged: (AppConfig) -> Unit
) {"""
settings_func_replacement = """@Composable
fun SettingsBottomSheet(
    settings: DownloadSettings,
    config: AppConfig,
    onDismiss: () -> Unit,
    onSettingsChanged: (DownloadSettings) -> Unit,
    onConfigChanged: (AppConfig) -> Unit,
    onViewErrorLog: () -> Unit = {}
) {"""
content = content.replace(settings_func_target, settings_func_replacement)

settings_bottom_replacement_real = """            TextButton(
                onClick = { onDismiss(); onViewErrorLog() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("View Error Log")
            }
            Button(
                onClick = onDismiss,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Done")
            }"""
content = content.replace(settings_bottom_target, settings_bottom_replacement_real)

# 10. Update SettingsBottomSheet call in MainScreen
call_settings_target = """        SettingsBottomSheet(
            settings = settings,
            config = config,
            onDismiss = { showSettings = false },
            onSettingsChanged = { viewModel.updateSettings(it) },
            onConfigChanged = { viewModel.updateConfig(it) }
        )"""
call_settings_replacement = """        SettingsBottomSheet(
            settings = settings,
            config = config,
            onDismiss = { showSettings = false },
            onSettingsChanged = { viewModel.updateSettings(it) },
            onConfigChanged = { viewModel.updateConfig(it) },
            onViewErrorLog = { showErrorLog = true }
        )"""
content = content.replace(call_settings_target, call_settings_replacement)


with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)

