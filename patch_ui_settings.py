import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update Theme Logic to support accents
target_theme = """        setContent {
            val viewModel: DownloaderViewModel = viewModel()
            val config by viewModel.appConfig.collectAsState()
            
            val isDarkTheme = when (config.theme) {
                "Light" -> false
                "Dark" -> true
                else -> isSystemInDarkTheme()
            }
            
            MaterialTheme(
                colorScheme = if (isDarkTheme) darkColorScheme() else lightColorScheme()
            ) {"""
rep_theme = """        setContent {
            val viewModel: DownloaderViewModel = viewModel()
            val config by viewModel.appConfig.collectAsState()
            
            val isDarkTheme = when (config.theme) {
                "Light" -> false
                "Dark" -> true
                else -> isSystemInDarkTheme()
            }
            
            // Build accent color scheme
            val baseColor = when (config.accent) {
                "Red" -> Color(0xFFE53935)
                "Green" -> Color(0xFF43A047)
                "Purple" -> Color(0xFF8E24AA)
                "Orange" -> Color(0xFFF4511E)
                else -> Color(0xFF1E88E5) // Blue
            }
            
            val colorScheme = if (isDarkTheme) {
                darkColorScheme(
                    primary = baseColor,
                    secondary = baseColor,
                    tertiary = baseColor
                )
            } else {
                lightColorScheme(
                    primary = baseColor,
                    secondary = baseColor,
                    tertiary = baseColor
                )
            }
            
            MaterialTheme(
                colorScheme = colorScheme
            ) {"""
content = content.replace(target_theme, rep_theme)

# 2. Update TopAppBar to remove Theme toggle
target_top_bar = """            TopAppBar(
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
                },"""
rep_top_bar = """            TopAppBar(
                title = { Text("YT Downloader") },
                actions = {
                    IconButton(onClick = { showSettings = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                },"""
content = content.replace(target_top_bar, rep_top_bar)

# 3. Update SettingsBottomSheet definition and ModalBottomSheet invocation
target_sheet_open = "    ModalBottomSheet(onDismissRequest = onDismiss) {"
rep_sheet_open = """    val sheetState = androidx.compose.material3.rememberModalBottomSheetState(skipPartiallyExpanded = true)
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        modifier = Modifier.fillMaxHeight(0.9f)
    ) {"""
content = content.replace(target_sheet_open, rep_sheet_open)

# 4. Highlight selected button and add theme/accent buttons
# Let's replace the Row of Save Directory buttons.
target_save_row = """            Row(
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                FilledTonalButton(onClick = { onConfigChanged(config.copy(saveDirectory = "Default")) }, modifier = Modifier.weight(1f), contentPadding = PaddingValues(0.dp)) { 
                    Text("Auto", fontSize = 11.sp, maxLines = 1) 
                }
                FilledTonalButton(onClick = { onConfigChanged(config.copy(saveDirectory = "/storage/emulated/0/Download/YT Downloader")) }, modifier = Modifier.weight(1f), contentPadding = PaddingValues(0.dp)) { 
                    Text("Downloads", fontSize = 11.sp, maxLines = 1) 
                }
                FilledTonalButton(onClick = { onConfigChanged(config.copy(saveDirectory = "/storage/emulated/0/Movies/YT Downloader")) }, modifier = Modifier.weight(1f), contentPadding = PaddingValues(0.dp)) { 
                    Text("Movies", fontSize = 11.sp, maxLines = 1) 
                }
                FilledTonalButton(onClick = { onConfigChanged(config.copy(saveDirectory = "/storage/emulated/0/Music/YT Downloader")) }, modifier = Modifier.weight(1f), contentPadding = PaddingValues(0.dp)) { 
                    Text("Music", fontSize = 11.sp, maxLines = 1) 
                }
                Button(onClick = { dirPickerLauncher.launch(null) }, modifier = Modifier.weight(1f), contentPadding = PaddingValues(0.dp)) { 
                    Text("Custom", fontSize = 11.sp, maxLines = 1) 
                }
            }"""
rep_save_row = """            @Composable
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
            
            Text("Accent Color", style = MaterialTheme.typography.labelMedium)
            Row(modifier = Modifier.fillMaxWidth().padding(top = 4.dp, bottom = 16.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                listOf(
                    "Blue" to Color(0xFF1E88E5), 
                    "Red" to Color(0xFFE53935), 
                    "Green" to Color(0xFF43A047), 
                    "Purple" to Color(0xFF8E24AA), 
                    "Orange" to Color(0xFFF4511E)
                ).forEach { (colorName, colorValue) ->
                    val isSelected = config.accent == colorName
                    androidx.compose.foundation.layout.Box(
                        modifier = Modifier
                            .size(36.dp)
                            .androidx.compose.foundation.background(colorValue, androidx.compose.foundation.shape.CircleShape)
                            .androidx.compose.foundation.border(if (isSelected) 3.dp else 0.dp, if (isSelected) MaterialTheme.colorScheme.onSurface else Color.Transparent, androidx.compose.foundation.shape.CircleShape)
                            .androidx.compose.foundation.clickable { onConfigChanged(config.copy(accent = colorName)) }
                    )
                }
            }"""
content = content.replace(target_save_row, rep_save_row)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
