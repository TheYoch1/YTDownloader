package com.aistudio.ytdownloader
import sh.calvin.reorderable.*
import androidx.compose.foundation.lazy.rememberLazyListState

import android.Manifest
import androidx.compose.foundation.border
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.background
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.compose.BackHandler
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.material3.FilledTonalButton
import androidx.core.content.ContextCompat
import androidx.lifecycle.viewmodel.compose.viewModel
import android.net.Uri
import androidx.compose.ui.text.style.TextOverflow
import kotlinx.coroutines.launch
import kotlin.math.roundToInt
import androidx.compose.foundation.horizontalScroll

import androidx.compose.foundation.clickable
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.VideoLibrary
import androidx.compose.material.icons.filled.FileOpen

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.material3.SwipeToDismissBox
import androidx.compose.material3.rememberSwipeToDismissBoxState
import androidx.compose.material3.SwipeToDismissBoxValue
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import java.io.File




val AppAccentColors = listOf(
    "Red" to Color(0xFFF44336), 
    "Deep Orange" to Color(0xFFFF5722),
    "Orange" to Color(0xFFFF9800),
    "Amber" to Color(0xFFFFC107),
    "Yellow" to Color(0xFFFFEB3B),
    "Lime" to Color(0xFFCDDC39),
    "Light Green" to Color(0xFF8BC34A),
    "Green" to Color(0xFF4CAF50),
    "Teal" to Color(0xFF009688),
    "Cyan" to Color(0xFF00BCD4),
    "Light Blue" to Color(0xFF03A9F4),
    "Blue" to Color(0xFF2196F3),
    "Indigo" to Color(0xFF3F51B5),
    "Deep Purple" to Color(0xFF673AB7),
    "Purple" to Color(0xFF9C27B0),
    "Pink" to Color(0xFFE91E63),
    "Rose" to Color(0xFFF43F5E),
    "Cherry" to Color(0xFFD81B60),
    "Crimson" to Color(0xFFC62828),
    "Rust" to Color(0xFFD84315),
    "Gold" to Color(0xFFFFD700),
    "Olive" to Color(0xFF827717),
    "Emerald" to Color(0xFF2E7D32),
    "Mint" to Color(0xFF00BFA5),
    "Sky" to Color(0xFF80D8FF),
    "Ocean" to Color(0xFF0277BD),
    "Navy" to Color(0xFF1A237E),
    "Grape" to Color(0xFF4A148C),
    "Magenta" to Color(0xFFC51162),
    "Brown" to Color(0xFF795548),
    "Grey" to Color(0xFF9E9E9E),
    "Blue Grey" to Color(0xFF607D8B)
)

class MainActivity : ComponentActivity() {
    private lateinit var downloaderViewModel: DownloaderViewModel

    override fun onStop() {
        super.onStop()
        if (::downloaderViewModel.isInitialized) {
            downloaderViewModel.saveQueue()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val viewModel: DownloaderViewModel = viewModel()
            this.downloaderViewModel = viewModel
            val config by viewModel.appConfig.collectAsState()
            
            val isDarkTheme = when (config.theme) {
                "Light" -> false
                "Dark" -> true
                else -> isSystemInDarkTheme()
            }
            
            // Build accent color scheme
            val baseColor = if (config.accent.startsWith("#")) {
                Color(android.graphics.Color.parseColor(config.accent))
            } else {
                AppAccentColors.find { it.first == config.accent }?.second ?: Color(0xFF009688)
            }
            
            val colorScheme = if (isDarkTheme) {
                darkColorScheme(
                    primary = baseColor,
                    onPrimary = Color.White,
                    primaryContainer = baseColor.copy(alpha = 0.3f),
                    onPrimaryContainer = Color.White,
                    secondary = baseColor,
                    tertiary = baseColor
                )
            } else {
                lightColorScheme(
                    primary = baseColor,
                    onPrimary = Color.White,
                    primaryContainer = baseColor.copy(alpha = 0.2f),
                    onPrimaryContainer = Color.Black,
                    secondary = baseColor,
                    tertiary = baseColor
                )
            }
            
            MaterialTheme(
                colorScheme = colorScheme
            ) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    MainScreen(viewModel, config)
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(viewModel: DownloaderViewModel, config: AppConfig) {
    val downloads by viewModel.downloadQueue.collectAsState()
    val individualProgressMap by DownloadManager.progressMap.collectAsState()
    val settings by viewModel.currentSettings.collectAsState()
    var urlInput by remember { mutableStateOf("") }
    var showSettings by remember { mutableStateOf(false) }
    
    var updateAvailable by remember { mutableStateOf<GithubRelease?>(null) }
    val context = LocalContext.current
    
    LaunchedEffect(Unit) {
        try {
            val release = checkGithubUpdate()
            if (release != null) {
                val currentVersion = BuildConfig.VERSION_NAME
                val remoteVersion = release.tag_name.removePrefix("v")
                if (remoteVersion != currentVersion && release.tag_name != currentVersion) {
                    updateAvailable = release
                }
            }
        } catch(e: Exception) {
            // Ignore failure
        }
    }
    
    if (updateAvailable != null) {
        val release = updateAvailable!!
        AlertDialog(
            onDismissRequest = { updateAvailable = null },
            title = { Text("Update Available") },
            text = { Text("A new version (${release.tag_name}) is available. Would you like to download it?") },
            confirmButton = {
                TextButton(onClick = {
                    try {
                        val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(release.html_url))
                        context.startActivity(intent)
                    } catch(e: Exception) {}
                    updateAvailable = null
                }) {
                    Text("Download")
                }
            },
            dismissButton = {
                TextButton(onClick = { updateAvailable = null }) {
                    Text("Later")
                }
            }
        )
    }

    var formatDialogUrl by remember { mutableStateOf<String?>(null) }
    var formatDialogTitle by remember { mutableStateOf<String?>(null) }
    var showErrorLog by remember { mutableStateOf(false) }
    var showHistoryLog by remember { mutableStateOf(false) }
    val keyboardController = LocalSoftwareKeyboardController.current
    val clipboardManager = LocalClipboardManager.current


    var searchResults by remember { mutableStateOf<List<SearchResult>>(emptyList()) }
    var isSearchLoading by remember { mutableStateOf(false) }
    var searchError by remember { mutableStateOf<String?>(null) }
    val coroutineScope = rememberCoroutineScope()
    
    BackHandler {
        (context as? android.app.Activity)?.moveTaskToBack(true)
    }

    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        val context = LocalContext.current
        var hasNotificationPermission by remember {
            mutableStateOf(
                ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS) == android.content.pm.PackageManager.PERMISSION_GRANTED
            )
        }
        val permissionLauncher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { isGranted ->
            hasNotificationPermission = isGranted
        }
        LaunchedEffect(Unit) {
            if (!hasNotificationPermission) {
                permissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("YT Downloader") },
                actions = {
                    Text("Yoch", fontFamily = androidx.compose.ui.text.font.FontFamily.Cursive, fontSize = 24.sp, modifier = Modifier.padding(end = 8.dp))
                    IconButton(onClick = { showSettings = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            // URL Input Section
            val isUrl = urlInput.contains("http://") || urlInput.contains("https://") || urlInput.contains("youtube.com") || urlInput.contains("youtu.be")
            Column(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    OutlinedTextField(
                        value = urlInput,
                        onValueChange = { 
                            urlInput = it 
                            if (it.isBlank()) {
                                searchResults = emptyList<SearchResult>()
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
                        maxLines = 5,
                        leadingIcon = {
                            IconButton(onClick = {
                                clipboardManager.getText()?.text?.let { urlInput = it }
                            }) {
                                Icon(if (isUrl || urlInput.isBlank()) Icons.Default.Link else Icons.Default.Search, contentDescription = "Paste from Clipboard")
                            }
                        },
                        trailingIcon = {
                            if (urlInput.isNotEmpty()) {
                                IconButton(onClick = { 
                                    urlInput = ""
                                    searchResults = emptyList<SearchResult>()
                                    searchError = null
                                }) {
                                    Icon(Icons.Default.Clear, contentDescription = "Clear")
                                }
                            }
                        }
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Button(
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
                        },
                        enabled = urlInput.isNotBlank() && !isSearchLoading,
                        modifier = Modifier.height(56.dp)
                    ) {
                        if (isSearchLoading) {
                            CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.onPrimary)
                        } else {
                            Icon(if (isUrl) Icons.Default.Add else Icons.Default.Search, contentDescription = if (isUrl) "Add Download" else "Search")
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(if (isUrl) "Add" else "Search")
                        }
                    }
                }
                
                AnimatedVisibility(visible = searchResults.isNotEmpty() || searchError != null) {
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 8.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f))
                    ) {
                        Column(modifier = Modifier.fillMaxWidth()) {
                            if (searchError != null) {
                                Text(
                                    text = searchError ?: "Unknown error",
                                    color = MaterialTheme.colorScheme.error,
                                    modifier = Modifier.padding(16.dp)
                                )
                            } else {
                                Text(
                                    text = "Search Results",
                                    style = MaterialTheme.typography.labelMedium,
                                    modifier = Modifier.padding(start = 16.dp, top = 12.dp, bottom = 4.dp, end = 16.dp),
                                    color = MaterialTheme.colorScheme.primary
                                )
                                searchResults.forEach { result ->
                                    ListItem(
                                        headlineContent = { Text(result.title, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                                        supportingContent = { Text(result.url, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                                        leadingContent = {
                                            if (result.thumbnailUrl != null) {
                                                coil3.compose.AsyncImage(
                                                    model = result.thumbnailUrl,
                                                    contentDescription = "Thumbnail",
                                                    modifier = Modifier.size(64.dp, 36.dp),
                                                    contentScale = androidx.compose.ui.layout.ContentScale.Crop
                                                )
                                            } else {
                                                Icon(Icons.Default.VideoLibrary, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                                            }
                                        },
                                        modifier = Modifier.pointerInput(Unit) {
                                            detectTapGestures(
                                                onTap = {
                                                    formatDialogUrl = result.url
                                                    formatDialogTitle = result.title
                                                },
                                                onLongPress = {

                                                    clipboardManager.setText(AnnotatedString(result.url))
                                                    android.widget.Toast.makeText(context, "Link copied!", android.widget.Toast.LENGTH_SHORT).show()
                                                }
                                            )
                                        },
                                        colors = ListItemDefaults.colors(containerColor = Color.Transparent)
                                    )
                                }
                            }
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            
            val activeDownloads = downloads.filter { it.status != "Cancelled" }
            if (activeDownloads.isNotEmpty()) {
                val totalFiles = activeDownloads.sumOf { if (it.isPlaylist && it.totalItems > 0) it.totalItems else 1 }
                val completedFilesProgress = activeDownloads.sumOf { 
                    val items = if (it.isPlaylist && it.totalItems > 0) it.totalItems else 1
                    (it.progress.toDouble() / 100.0) * items
                }
                val avgProgress = if (totalFiles > 0) (completedFilesProgress / totalFiles.toDouble() * 100.0).toFloat() else 0f
                Column(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text(
                            "Overall Progress (${activeDownloads.size} active)",
                            style = MaterialTheme.typography.labelMedium
                        )
                        Text(
                            "${avgProgress.toInt()}%",
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.Bold
                        )
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    LinearProgressIndicator(
                        progress = { if (avgProgress.isNaN()) 0f else (avgProgress / 100f).coerceIn(0f, 1f) },
                        modifier = Modifier.fillMaxWidth().height(8.dp),
                        color = MaterialTheme.colorScheme.primary,
                        trackColor = MaterialTheme.colorScheme.primaryContainer
                    )
                }
            }

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(
                    "Active Downloads",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(bottom = 8.dp)
                )
                
                if (downloads.any { it.status == "Completed" || it.status == "Error" || it.status == "Cancelled" }) {
                    TextButton(onClick = { viewModel.clearFinishedDownloads() }) {
                        Text("Clear Finished")
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            val filteredActiveDownloads = downloads.filter { it.status != "Cancelled" }
            
            if (filteredActiveDownloads.isEmpty()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            Icons.Default.Download,
                            contentDescription = null,
                            modifier = Modifier.size(64.dp),
                            tint = MaterialTheme.colorScheme.outline
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            "No active downloads.",
                            color = MaterialTheme.colorScheme.outline
                        )
                        Text(
                            "Paste a link above to get started.",
                            color = MaterialTheme.colorScheme.outline
                        )
                    }
                }
            } else {
                val lazyListState = rememberLazyListState()
                val reorderableLazyColumnState = rememberReorderableLazyColumnState(
                    lazyListState,
                    onMove = { from, to ->
                        viewModel.reorderQueue(from.index, to.index)
                    }
                )
                LazyColumn(
                    modifier = Modifier.weight(1f),
                    state = lazyListState,
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(filteredActiveDownloads, key = { it.id }) { download ->
                        ReorderableItem(reorderableLazyColumnState, key = download.id) { isDragging ->
                            val dismissState = rememberSwipeToDismissBoxState(
                                confirmValueChange = { dismissValue ->
                                    if (dismissValue == SwipeToDismissBoxValue.EndToStart || dismissValue == SwipeToDismissBoxValue.StartToEnd) {
                                        viewModel.removeDownload(download.id)
                                        true
                                    } else {
                                        false
                                    }
                                }
                            )
                            
                            SwipeToDismissBox(
                                state = dismissState,
                                backgroundContent = {
                                    val color by animateColorAsState(
                                        targetValue = when (dismissState.targetValue) {
                                            SwipeToDismissBoxValue.Settled -> Color.Transparent
                                            else -> MaterialTheme.colorScheme.errorContainer
                                        },
                                        label = "dismissColor"
                                    )
                                    Box(
                                        modifier = Modifier
                                            .fillMaxSize()
                                            .background(color, RoundedCornerShape(12.dp))
                                            .padding(horizontal = 20.dp),
                                        contentAlignment = Alignment.CenterEnd
                                    ) {
                                        if (dismissState.targetValue != SwipeToDismissBoxValue.Settled) {
                                            Icon(
                                                Icons.Default.Delete,
                                                contentDescription = "Delete",
                                                tint = MaterialTheme.colorScheme.onErrorContainer
                                            )
                                        }
                                    }
                                },
                                content = {
                                    DownloadItemCard(
                                        download = download,
                                        individualProgress = individualProgressMap[download.id],
                                        onRemove = { viewModel.removeDownload(download.id) },
                                        onCancel = { viewModel.cancelDownload(download.id) },
                                        onPause = { viewModel.pauseDownload(download.id) },
                                        onResume = { viewModel.resumeDownload(download.id) },
                                        onRetry = { viewModel.retryDownload(download.id) },
                                        dragModifier = Modifier.draggableHandle(
                                            onDragStarted = {
                                                // optional
                                            },
                                            onDragStopped = {
                                                // optional
                                            },
                                        )
                                    )
                                }
                            )
                        }
                    }
                }
            }
        }
        
    
    if (formatDialogUrl != null) {
        var isAudio by remember(formatDialogUrl) { mutableStateOf(false) }
        var selectedFormatId by remember(formatDialogUrl) { mutableStateOf<String?>(null) }
        if (formatDialogUrl?.contains("list=") == true) {
            isAudio = false
            
        }
        var downloadSubtitles by remember(formatDialogUrl) { mutableStateOf(settings.downloadSubtitles) }
        var availableFormats by remember { mutableStateOf<List<FormatOption>?>(null) }
        var isLoadingQualities by remember(formatDialogUrl) { mutableStateOf(true) }

        LaunchedEffect(formatDialogUrl) {
            isLoadingQualities = true
            val (title, qualities) = viewModel.fetchAvailableFormats(formatDialogUrl!!)
            formatDialogTitle = title
            availableFormats = qualities
            
            isAudio = false
            downloadSubtitles = false
            if (qualities.isNotEmpty()) {
                val defaultVideoFormat = qualities.find { it.height == 720 && !it.isAudioOnly }
                    ?: qualities.firstOrNull { !it.isAudioOnly }
                    ?: qualities.firstOrNull()
                selectedFormatId = defaultVideoFormat?.formatId
            }
            
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
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("Available Formats:")
                        LazyColumn(modifier = Modifier.heightIn(max = 400.dp)) {
                            val filteredFormats = availableFormats?.filter { it.isAudioOnly == isAudio } ?: emptyList()
                            items(filteredFormats) { formatOpt ->
                                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable { selectedFormatId = formatOpt.formatId }.fillMaxWidth()) {
                                    RadioButton(selected = selectedFormatId == formatOpt.formatId, onClick = { selectedFormatId = formatOpt.formatId })
                                    Text(if (formatOpt.sizeStr.isNotEmpty()) "${formatOpt.label} (~${formatOpt.sizeStr})" else formatOpt.label)
                                }
                            }
                        }
                        if (!isAudio) {
                            Spacer(modifier = Modifier.height(8.dp))
                            if (settings.downloadSubtitles) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Checkbox(checked = downloadSubtitles, onCheckedChange = { downloadSubtitles = it })
                                    Text("Download English Subtitles")
                                }
                            }
                        }
                    }
                }
            },
            confirmButton = {
                Button(
                    enabled = !isLoadingQualities,
                    onClick = {
                    val selectedFormat = availableFormats?.find { it.formatId == selectedFormatId }
                    val saveFmt = if (isAudio) {
                        if (selectedFormat?.label?.contains("M4A") == true) "m4a" else "mp3"
                    } else "mp4"

                    val customSettings = DownloadSettings(
                        audioOnly = isAudio,
                        downloadSubtitles = downloadSubtitles,
                        saveFormat = saveFmt,
                        customFormatId = selectedFormatId,
                        formatLabel = if (isAudio) "Audio ($saveFmt)" else "Video (${selectedFormat?.label ?: "Auto"})",
                        selectedHeight = selectedFormat?.height ?: 0
                    )
                    val urls = formatDialogUrl!!.split(Regex("\\s+")).filter { it.isNotBlank() && (it.startsWith("http://") || it.startsWith("https://") || it.contains("youtu")) }
                    if (urls.size > 1) {
                        urls.forEach { u ->
                            viewModel.addDownload(u, "Unknown Title", u.contains("list="), customSettings)
                        }
                    } else {
                        val urlStr = formatDialogUrl!!.trim()
                        viewModel.addDownload(urlStr, formatDialogTitle ?: "Unknown Title", urlStr.contains("list="), customSettings)
                    }
                    urlInput = ""
                    searchResults = emptyList<SearchResult>()
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
    
    if (showHistoryLog) {
        AlertDialog(
            onDismissRequest = { showHistoryLog = false },
            title = { Text("Download History") },
            text = {
                val historyFile = File(context.filesDir, "history.log")
                val logText = if (historyFile.exists()) historyFile.readText() else "No history recorded."
                val clipboardManager = LocalClipboardManager.current
                
                LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp)) {
                    item {
                        Text(
                            text = logText,
                            style = MaterialTheme.typography.bodySmall,
                            modifier = Modifier.pointerInput(Unit) {
                                detectTapGestures(
                                    onLongPress = {
                                        clipboardManager.setText(AnnotatedString(logText))
                                        android.widget.Toast.makeText(context, "Copied to clipboard", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                )
                            }
                        )
                    }
                }
            },
            confirmButton = {
                Button(onClick = { showHistoryLog = false }) { Text("Close") }
            },
            dismissButton = {
                TextButton(onClick = {
                    File(context.filesDir, "history.log").delete()
                    showHistoryLog = false
                }) { Text("Clear History") }
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
                
                SelectionContainer {
                    LazyColumn {
                        val lines = logText.split("\n").filter { it.isNotBlank() }
                        if (lines.isEmpty()) {
                            item { Text("No errors recorded.") }
                        } else {
                            items(lines) { line ->
                                Text(
                                    text = line, 
                                    style = MaterialTheme.typography.bodySmall,
                                    modifier = Modifier.padding(bottom = 8.dp).fillMaxWidth().clickable {
                                        clipboardManager.setText(AnnotatedString(line))
                                        android.widget.Toast.makeText(context, "Copied error line", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                )
                            }
                        }
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

    if (showSettings) {
            SettingsBottomSheet(
                downloads = downloads,
                viewModel = viewModel,
                settings = settings,
                config = config,
                onDismiss = { showSettings = false },
                onSettingsChanged = { viewModel.updateCurrentSettings(it) },
                onConfigChanged = { viewModel.updateConfig(it) },
                onViewErrorLog = { showErrorLog = true },
                onViewHistoryLog = { showHistoryLog = true }
            )
        }
}
}
@Composable
fun DownloadItemCard(
    download: QueuedDownload,
    individualProgress: Float? = null,
    onRemove: () -> Unit,
    onCancel: () -> Unit,
    onPause: () -> Unit,
    onResume: () -> Unit,
    onRetry: () -> Unit,
    dragModifier: Modifier = Modifier
) {
    val context = LocalContext.current
    Card(
        modifier = Modifier.fillMaxWidth().then(
            if (download.status == "Completed" && download.localFilePath != null) {
                Modifier.clickable {
                    val uriStr = download.localFilePath!!
                    val intent = android.content.Intent(android.content.Intent.ACTION_VIEW)
                    val uri = android.net.Uri.parse(uriStr)
                    
                    val file = java.io.File(if (uriStr.startsWith("file://")) uri.path!! else uriStr)
                    if (file.exists()) {
                        val contentUri = androidx.core.content.FileProvider.getUriForFile(context, "${context.packageName}.provider", file)
                        val mime = if (uriStr.endsWith(".mp4") || uriStr.endsWith(".webm") || uriStr.endsWith(".mkv")) "video/*" else "audio/*"
                        intent.setDataAndType(contentUri, mime)
                        intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    } else if (uriStr.startsWith("content://")) {
                        val mime = if (uriStr.endsWith(".mp4") || uriStr.endsWith(".webm") || uriStr.endsWith(".mkv")) "video/*" else "audio/*"
                        intent.setDataAndType(uri, mime)
                        intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    }
                    try {
                        context.startActivity(intent)
                    } catch (e: Exception) {
                        android.widget.Toast.makeText(context, "Could not open file", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }
            } else Modifier
        ),
        colors = CardDefaults.cardColors(
            containerColor = when (download.status) {
                "Completed" -> Color(0xFF4CAF50).copy(alpha = 0.2f)
                "Downloading", "Extracting" -> Color(0xFF2196F3).copy(alpha = 0.2f)
                "Queued", "Paused" -> Color(0xFFFFC107).copy(alpha = 0.2f)
                "Error", "Cancelled" -> Color(0xFFF44336).copy(alpha = 0.2f)
                else -> MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f)
            }
        )
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = if (download.isPlaylist && download.currentDownloadingTitle.isNotEmpty() && download.status == "Downloading") download.currentDownloadingTitle else download.title,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = download.url,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f),
                        maxLines = 1
                    )
                    
                    // Show format explicitly (so they know what quality was chosen when queued)
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = if (download.settings.formatLabel.isNotEmpty()) "Format: ${download.settings.formatLabel}" else if (download.settings.audioOnly) "Format: Audio (MP3)" else "Format: Video (${download.settings.quality.label})",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.primary
                    )
                    
                    if (download.isPlaylist && download.totalItems > 0) {
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "Downloading ${download.currentItemIndex} of ${download.totalItems}: ${download.currentDownloadingTitle}",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.secondary,
                            maxLines = 1,
                            overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                        )
                    }
                }
                Icon(
                    Icons.Default.DragHandle,
                    contentDescription = "Drag to reorder",
                    modifier = dragModifier.size(24.dp).padding(end = 8.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
                IconButton(onClick = onRemove, modifier = Modifier.size(24.dp)) {
                    Icon(
                        Icons.Default.Close,
                        contentDescription = "Remove",
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = download.status,
                    style = MaterialTheme.typography.bodyMedium,
                    color = when (download.status) {
                        "Completed" -> Color(0xFF388E3C)
                        "Cancelled", "Error" -> MaterialTheme.colorScheme.error
                        "Paused" -> MaterialTheme.colorScheme.outline
                        else -> MaterialTheme.colorScheme.primary
                    }
                )
                
                val progressText = if (download.isPlaylist && download.totalItems > 0 && download.status == "Downloading") {
                    "${download.progress.toInt()}% Overall (${download.currentItemProgress.toInt()}% file)"
                } else {
                    "${download.progress.toInt()}%"
                }
                
                Text(
                    text = progressText,
                    style = MaterialTheme.typography.bodySmall,
                    fontWeight = FontWeight.Bold
                )
            }
            
            Spacer(modifier = Modifier.height(4.dp))
            
            if (download.status == "Error" && download.errorMessage != null) {
                val clipboardManager = LocalClipboardManager.current
                Text(
                    text = download.errorMessage ?: "",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.error,
                    modifier = Modifier.padding(bottom = 8.dp).pointerInput(Unit) {
                        detectTapGestures(
                            onLongPress = {
                                clipboardManager.setText(AnnotatedString(download.errorMessage ?: ""))
                                android.widget.Toast.makeText(context, "Error copied to clipboard", android.widget.Toast.LENGTH_SHORT).show()
                            }
                        )
                    }
                )
            }
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                LinearProgressIndicator(
                    progress = { 
                        val itemProgress = individualProgress ?: download.progress
                        if (itemProgress.isNaN()) 0f else (itemProgress / 100f).coerceIn(0f, 1f) 
                    },
                    modifier = Modifier.weight(1f),
                    color = if (download.status == "Completed") 
                        Color(0xFF4CAF50) 
                    else if (download.status == "Cancelled" || download.status == "Error")
                        MaterialTheme.colorScheme.error
                    else if (download.status == "Paused")
                        MaterialTheme.colorScheme.outline
                    else 
                        MaterialTheme.colorScheme.primary,
                    trackColor = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f)
                )
                
                if (download.downloadSpeed.isNotEmpty()) {
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = download.downloadSpeed,
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                if (download.status == "Downloading" || download.status == "Extracting" || download.status == "Queued" || download.status == "Paused") {
                    Spacer(modifier = Modifier.width(8.dp))
                    if (download.status == "Downloading") {
                        IconButton(onClick = onPause, modifier = Modifier.size(24.dp)) {
                            Icon(Icons.Default.Pause, contentDescription = "Pause", tint = MaterialTheme.colorScheme.primary)
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                    } else if (download.status == "Paused") {
                        IconButton(onClick = onResume, modifier = Modifier.size(24.dp)) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Resume", tint = MaterialTheme.colorScheme.primary)
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                    }
                    IconButton(
                        onClick = onCancel,
                        modifier = Modifier.size(24.dp)
                    ) {
                        Icon(
                            Icons.Default.Stop,
                            contentDescription = "Cancel",
                            tint = MaterialTheme.colorScheme.error
                        )
                    }
                } else if (download.status == "Error") {
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(
                        onClick = onRetry,
                        modifier = Modifier.size(24.dp)
                    ) {
                        Icon(
                            Icons.Default.Refresh,
                            contentDescription = "Retry",
                            tint = MaterialTheme.colorScheme.error
                        )
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsBottomSheet(
    downloads: List<QueuedDownload>,
    viewModel: DownloaderViewModel,
    settings: DownloadSettings,
    config: AppConfig,
    onDismiss: () -> Unit,
    onSettingsChanged: (DownloadSettings) -> Unit,
    onConfigChanged: (AppConfig) -> Unit,
    onViewErrorLog: () -> Unit = {},
    onViewHistoryLog: () -> Unit = {}
) {
    val context = LocalContext.current
    val dirPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenDocumentTree()
    ) { uri ->
        if (uri != null) {
            val takeFlags = android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION or android.content.Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            try {
                context.contentResolver.takePersistableUriPermission(uri, takeFlags)
            } catch (e: Exception) {}
            onConfigChanged(config.copy(saveDirectory = uri.toString()))
        }
    }

    val sheetState = androidx.compose.material3.rememberModalBottomSheetState(skipPartiallyExpanded = true)
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        // modifier = Modifier.fillMaxHeight(0.9f) removed to anchor bottom naturally
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp, vertical = 16.dp)
                .padding(bottom = 48.dp)
                .verticalScroll(rememberScrollState())
        ) {
            Text(
                "App Settings",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )
            
            // Calculate storage used by YT Downloader
            var totalYtSize by remember { mutableStateOf(0L) }
            val stat = android.os.StatFs(android.os.Environment.getExternalStorageDirectory().path)
            val totalSpace = stat.totalBytes
            val availableSpace = stat.availableBytes
            val context = androidx.compose.ui.platform.LocalContext.current
            
            LaunchedEffect(config.saveDirectory) {
                kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
                    var size = 0L
                    val pathsToScan = mutableListOf<String>()
                    if (config.saveDirectory == "Default") {
                        pathsToScan.addAll(listOf(
                            "/storage/emulated/0/Download/YT Downloader",
                            "/storage/emulated/0/Movies/YT Downloader",
                            "/storage/emulated/0/Music/YT Downloader"
                        ))
                    } else {
                        pathsToScan.add(config.saveDirectory)
                    }

                    pathsToScan.forEach { path ->
                        if (path.startsWith("content://")) {
                            try {
                                val treeUri = android.net.Uri.parse(path)
                                val docFile = androidx.documentfile.provider.DocumentFile.fromTreeUri(context, treeUri)
                                if (docFile != null && docFile.isDirectory) {
                                    fun calculateSize(df: androidx.documentfile.provider.DocumentFile): Long {
                                        var s = 0L
                                        df.listFiles().forEach {
                                            if (it.isDirectory) s += calculateSize(it) else s += it.length()
                                        }
                                        return s
                                    }
                                    size += calculateSize(docFile)
                                }
                            } catch (e: Exception) {
                                e.printStackTrace()
                            }
                        } else {
                            val dir = java.io.File(path)
                            if (dir.exists() && dir.isDirectory) {
                                dir.walkTopDown().filter { it.isFile }.forEach { size += it.length() }
                            }
                        }
                    }
                    totalYtSize = size
                }
            }
            
            Card(
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
                colors = androidx.compose.material3.CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    val sizeMB = totalYtSize / (1024f * 1024f)
                    val sizeGB = totalYtSize / (1024f * 1024f * 1024f)
                    val displaySize = if (sizeGB >= 1.0) String.format("%.2f GB", sizeGB) else String.format("%.1f MB", sizeMB)
                    val folderName = if (config.saveDirectory == "Default") "Auto Folders" else if (config.saveDirectory.startsWith("content://")) "Custom Folder" else java.io.File(config.saveDirectory).name
                    
                    Text("Storage Used in $folderName: $displaySize", fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(8.dp))
                    LinearProgressIndicator(
                        progress = (totalYtSize.toFloat() / totalSpace.toFloat().coerceAtLeast(1f)).coerceIn(0f, 1f),
                        modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp))
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        "Available Storage: ${String.format("%.1f GB", availableSpace / (1024f * 1024f * 1024f))} / ${String.format("%.1f GB", totalSpace / (1024f * 1024f * 1024f))}", 
                        style = MaterialTheme.typography.bodySmall, 
                        modifier = Modifier.align(Alignment.End)
                    )
                }
            }
            
            Text("Save Directory", style = MaterialTheme.typography.labelMedium)
            val decodedPath = if (config.saveDirectory == "Default") {
                "Auto (Movies & Music)"
            } else {
                try { Uri.decode(config.saveDirectory) } catch(e: Exception) { config.saveDirectory }
            }
            Text(
                text = decodedPath,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(top = 4.dp, bottom = 8.dp),
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            @Composable
            fun DirBtn(label: String, path: String, isCustom: Boolean = false) {
                val isSelected = config.saveDirectory == path || (isCustom && !listOf("Default", "/storage/emulated/0/Download/YT Downloader", "/storage/emulated/0/Movies/YT Downloader", "/storage/emulated/0/Music/YT Downloader").contains(config.saveDirectory))
                val colors = if (isSelected) androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.onPrimary) else androidx.compose.material3.ButtonDefaults.filledTonalButtonColors()
                androidx.compose.material3.Button(
                    onClick = { if (isCustom) dirPickerLauncher.launch(null) else onConfigChanged(config.copy(saveDirectory = path)) },
                    modifier = Modifier.weight(1f).padding(horizontal = 2.dp),
                    contentPadding = PaddingValues(0.dp),
                    colors = colors
                ) {
                    Text(label, fontSize = 11.sp, maxLines = 1)
                }
            }
            Row(
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
            ) {
                DirBtn("Auto", "Default")
                DirBtn("Downloads", "/storage/emulated/0/Download/YT Downloader")
                DirBtn("Movies", "/storage/emulated/0/Movies/YT Downloader")
                DirBtn("Music", "/storage/emulated/0/Music/YT Downloader")
                DirBtn("Custom", "", isCustom = true)
            }
            
            // Add Theme and Accent picker
            Text("App Theme", style = MaterialTheme.typography.labelMedium)
            Row(modifier = Modifier.fillMaxWidth().padding(top = 4.dp, bottom = 16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                listOf("System", "Light", "Dark").forEach { themeName ->
                    val isSelected = config.theme == themeName
                    androidx.compose.material3.FilterChip(
                        selected = isSelected,
                        onClick = { onConfigChanged(config.copy(theme = themeName)) },
                        label = { Text(themeName) }
                    )
                }
            }
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Accent Color", style = MaterialTheme.typography.labelMedium)
                val closestIndex = if (config.colorOffset >= 0f) {
                    (config.colorOffset * AppAccentColors.size).roundToInt() % AppAccentColors.size
                } else {
                    AppAccentColors.indexOfFirst { it.first == config.accent }.coerceAtLeast(0)
                }
                Text(AppAccentColors[closestIndex].first, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
            }
            androidx.compose.foundation.layout.BoxWithConstraints(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 8.dp, bottom = 24.dp)
                    .height(40.dp)
            ) {
                val cycleWidthPx = 1500f
                var scrollOffset by remember { 
                    mutableStateOf(
                        if (config.colorOffset >= 0f) config.colorOffset * cycleWidthPx
                        else (AppAccentColors.indexOfFirst { it.first == config.accent }.coerceAtLeast(0).toFloat() / AppAccentColors.size) * cycleWidthPx
                    )
                }

                androidx.compose.foundation.Canvas(
                    modifier = Modifier
                        .fillMaxSize()
                        .pointerInput(Unit) {
                            detectHorizontalDragGestures { change, dragAmount: Float ->
                                change.consume()
                                scrollOffset = (scrollOffset - dragAmount + cycleWidthPx) % cycleWidthPx
                                
                                val offsetFraction = scrollOffset / cycleWidthPx
                                val floatIndex = offsetFraction * AppAccentColors.size
                                val index1 = floatIndex.toInt() % AppAccentColors.size
                                val index2 = (index1 + 1) % AppAccentColors.size
                                val fraction = floatIndex - floatIndex.toInt()
                                
                                val c1 = AppAccentColors[index1].second
                                val c2 = AppAccentColors[index2].second
                                val blended = androidx.compose.ui.graphics.lerp(c1, c2, fraction)
                                
                                val hex = String.format("#%08X", blended.toArgb())
                                
                                onConfigChanged(config.copy(accent = hex, colorOffset = offsetFraction))
                            }
                        }
                ) {
                    val colors = AppAccentColors.map { it.second } + AppAccentColors.first().second
                    val startX = (size.width / 2f) - scrollOffset
                    val endX = startX + cycleWidthPx
                    val brush = androidx.compose.ui.graphics.Brush.horizontalGradient(
                        colors = colors,
                        startX = startX,
                        endX = endX,
                        tileMode = androidx.compose.ui.graphics.TileMode.Repeated
                    )
                    drawRoundRect(
                        brush = brush,
                        cornerRadius = androidx.compose.ui.geometry.CornerRadius(20.dp.toPx())
                    )
                    
                    val center = size.width / 2f
                    drawLine(
                        color = Color.White,
                        start = androidx.compose.ui.geometry.Offset(center, 0f),
                        end = androidx.compose.ui.geometry.Offset(center, size.height),
                        strokeWidth = 4.dp.toPx()
                    )
                }
                androidx.compose.foundation.layout.Box(
                    modifier = Modifier
                        .align(Alignment.Center)
                        .fillMaxHeight()
                        .width(20.dp) // wide enough to be clickable
                        .clickable(
                            interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                            indication = null,
                            onClick = {
                                val tealFraction = (AppAccentColors.indexOfFirst { it.first == "Teal" }.coerceAtLeast(0).toFloat() / AppAccentColors.size)
                                scrollOffset = tealFraction * cycleWidthPx
                                onConfigChanged(config.copy(accent = "Teal", colorOffset = tealFraction))
                            }
                        )
                )
            }
            Text(text = "Max Concurrent Downloads: ${config.maxConcurrentDownloads}", modifier = Modifier.padding(top = 16.dp))
            androidx.compose.material3.Slider(
                value = config.maxConcurrentDownloads.toFloat(),
                onValueChange = { 
                    onConfigChanged(config.copy(maxConcurrentDownloads = it.toInt()))
                    val intent = android.content.Intent(context, DownloadService::class.java).apply {
                        action = DownloadService.ACTION_CHECK_QUEUE
                    }
                    androidx.core.content.ContextCompat.startForegroundService(context, intent)
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
                Text("Tag Audio File")
                Switch(
                    checked = settings.tagAudioFile,
                    onCheckedChange = { 
                        onSettingsChanged(settings.copy(tagAudioFile = it))
                    }
                )
            }
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Download Subtitles")
                Switch(
                    checked = settings.downloadSubtitles,
                    onCheckedChange = { 
                        onSettingsChanged(settings.copy(downloadSubtitles = it))
                    }
                )
            }
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Wi-Fi Only")
                Switch(
                    checked = config.wifiOnly,
                    onCheckedChange = { 
                        onConfigChanged(config.copy(wifiOnly = it))
                    }
                )
            }
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Push Notifications")
                Switch(
                    checked = config.notifyOnComplete,
                    onCheckedChange = { 
                        onConfigChanged(config.copy(notifyOnComplete = it))
                    }
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            OutlinedTextField(
                value = settings.filenamePattern,
                onValueChange = { onSettingsChanged(settings.copy(filenamePattern = it)) },
                label = { Text("Filename Pattern") },
                modifier = Modifier.fillMaxWidth()
            )
            Text(
                "Available tags: \$title, \$artist, \$channel, \$playlist",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(top = 4.dp, bottom = 16.dp)
            )
            
            TextButton(
                onClick = { onDismiss(); onViewHistoryLog() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("View History Log")
            }
            
            TextButton(
                onClick = { onDismiss(); onViewErrorLog() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("View Error Log")
            }
            
            TextButton(
                onClick = { 
                    android.widget.Toast.makeText(context, "Updating engine in background...", android.widget.Toast.LENGTH_SHORT).show()
                    kotlinx.coroutines.GlobalScope.launch(kotlinx.coroutines.Dispatchers.IO) {
                        try {
                            com.yausername.youtubedl_android.YoutubeDL.getInstance().updateYoutubeDL(context, com.yausername.youtubedl_android.YoutubeDL.UpdateChannel.NIGHTLY)
                            kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                                android.widget.Toast.makeText(context, "Engine updated successfully", android.widget.Toast.LENGTH_SHORT).show()
                            }
                        } catch (e: Exception) {
                            kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                                android.widget.Toast.makeText(context, "Update failed: ${e.message}", android.widget.Toast.LENGTH_LONG).show()
                            }
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Force Update Engine")
            }
            Button(
                onClick = onDismiss,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Done")
            }
        }
    }
}

data class GithubRelease(val tag_name: String, val html_url: String)

suspend fun checkGithubUpdate(): GithubRelease? {
    return kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
        try {
            val client = okhttp3.OkHttpClient()
            val request = okhttp3.Request.Builder()
                .url("https://api.github.com/repos/TheYoch1/YTDownloader/releases/latest")
                .header("User-Agent", "YTDownloader-Update-Checker")
                .build()
            val response = client.newCall(request).execute()
            if (response.isSuccessful) {
                response.body?.string()?.let {
                    com.google.gson.Gson().fromJson(it, GithubRelease::class.java)
                }
            } else null
        } catch (e: Exception) {
            null
        }
    }
}
