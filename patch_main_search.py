import sys

with open('app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt', 'r') as f:
    content = f.read()

# Add imports
imports = '''
import androidx.compose.foundation.clickable
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.VideoLibrary
'''
content = content.replace('import androidx.compose.ui.text.style.TextOverflow', 'import androidx.compose.ui.text.style.TextOverflow' + imports)

# Add state variables
state_vars = '''    var urlInput by remember { mutableStateOf("") }
    var showSettings by remember { mutableStateOf(false) }

    var isSearching by remember { mutableStateOf(false) }
    var searchQuery by remember { mutableStateOf("") }
    var searchResults by remember { mutableStateOf<List<SearchResult>>(emptyList()) }
    var isSearchLoading by remember { mutableStateOf(false) }
    var searchError by remember { mutableStateOf<String?>(null) }
    val coroutineScope = rememberCoroutineScope()'''

content = content.replace('    var urlInput by remember { mutableStateOf("") }\n    var showSettings by remember { mutableStateOf(false) }', state_vars)

# Replace TopAppBar
top_bar_old = '''    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("YT Downloader") },
                actions = {
                    IconButton(onClick = { 
                        val nextTheme = when (config.theme) {
                            "System" -> "Dark"
                            "Dark" -> "Light"
                            else -> "System"
                        }
                        viewModel.updateConfig(config.copy(theme = nextTheme))
                    }) {
                        val icon = when (config.theme) {
                            "System" -> Icons.Default.BrightnessAuto
                            "Dark" -> Icons.Default.DarkMode
                            else -> Icons.Default.LightMode
                        }
                        Icon(icon, contentDescription = "Toggle Theme")
                    }
                    IconButton(onClick = { showSettings = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        }
    ) { paddingValues ->'''

top_bar_new = '''    Scaffold(
        topBar = {
            if (isSearching) {
                SearchBar(
                    query = searchQuery,
                    onQueryChange = { searchQuery = it },
                    onSearch = { 
                        isSearchLoading = true
                        searchError = null
                        coroutineScope.launch {
                            try {
                                searchResults = searchYouTubeVideos(searchQuery)
                            } catch (e: Exception) {
                                searchError = e.message
                            } finally {
                                isSearchLoading = false
                            }
                        }
                    },
                    active = true,
                    onActiveChange = { if (!it) isSearching = false },
                    placeholder = { Text("Search YouTube...") },
                    leadingIcon = {
                        IconButton(onClick = { isSearching = false }) {
                            Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                        }
                    },
                    trailingIcon = {
                        if (searchQuery.isNotEmpty()) {
                            IconButton(onClick = { searchQuery = "" }) {
                                Icon(Icons.Default.Clear, contentDescription = "Clear")
                            }
                        }
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    if (isSearchLoading) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            CircularProgressIndicator()
                        }
                    } else if (searchError != null) {
                        Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.Center) {
                            Text(searchError ?: "", color = MaterialTheme.colorScheme.error)
                        }
                    } else {
                        LazyColumn(modifier = Modifier.fillMaxSize()) {
                            items(searchResults) { result ->
                                ListItem(
                                    headlineContent = { Text(result.title) },
                                    supportingContent = { Text(result.url) },
                                    leadingContent = { Icon(Icons.Default.VideoLibrary, contentDescription = null) },
                                    modifier = Modifier.clickable {
                                        viewModel.addDownload(result.url, result.title)
                                        isSearching = false
                                    }
                                )
                            }
                        }
                    }
                }
            } else {
                TopAppBar(
                    title = { Text("YT Downloader") },
                    actions = {
                        IconButton(onClick = { isSearching = true }) {
                            Icon(Icons.Default.Search, contentDescription = "Search")
                        }
                        IconButton(onClick = { 
                            val nextTheme = when (config.theme) {
                                "System" -> "Dark"
                                "Dark" -> "Light"
                                else -> "System"
                            }
                            viewModel.updateConfig(config.copy(theme = nextTheme))
                        }) {
                            val icon = when (config.theme) {
                                "System" -> Icons.Default.BrightnessAuto
                                "Dark" -> Icons.Default.DarkMode
                                else -> Icons.Default.LightMode
                            }
                            Icon(icon, contentDescription = "Toggle Theme")
                        }
                        IconButton(onClick = { showSettings = true }) {
                            Icon(Icons.Default.Settings, contentDescription = "Settings")
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.primaryContainer,
                        titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                )
            }
        }
    ) { paddingValues ->'''

content = content.replace(top_bar_old, top_bar_new)

with open('app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt', 'w') as f:
    f.write(content)
