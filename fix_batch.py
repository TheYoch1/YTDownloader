import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target_imports = '''import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.ViewModelProvider'''

rep_imports = target_imports + '''
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import java.io.BufferedReader
import java.io.InputStreamReader'''

content = content.replace(target_imports, rep_imports)

target_icons = '''import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.VideoLibrary'''

rep_icons = target_icons + '''
import androidx.compose.material.icons.filled.FileOpen'''

content = content.replace(target_icons, rep_icons)


target_ui = '''                        trailingIcon = {
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
                            if (isUrl) {
                                formatDialogUrl = urlInput
                            } else {
                                isSearchLoading = true
                                searchError = null
                                coroutineScope.launch {
                                    try {
                                        searchResults = viewModel.searchYouTube(urlInput)
                                        if (searchResults.isEmpty()) {
                                            searchError = "No results found"
                                        }
                                    } catch (e: Exception) {
                                        searchError = "Search failed: ${e.message}"
                                    } finally {
                                        isSearchLoading = false
                                    }
                                }
                            }
                        },
                        modifier = Modifier.height(56.dp)
                    ) {
                        Text(if (isUrl) "Download" else "Search")
                    }
                }'''

rep_ui = '''                        trailingIcon = {
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
                    
                    val filePickerLauncher = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri ->
                        if (uri != null) {
                            coroutineScope.launch(kotlinx.coroutines.Dispatchers.IO) {
                                try {
                                    context.contentResolver.openInputStream(uri)?.use { inputStream ->
                                        BufferedReader(InputStreamReader(inputStream)).use { reader ->
                                            var line = reader.readLine()
                                            while (line != null) {
                                                if (line.trim().isNotEmpty() && (line.contains("youtube.com") || line.contains("youtu.be"))) {
                                                    viewModel.addDownload(line.trim())
                                                }
                                                line = reader.readLine()
                                            }
                                        }
                                    }
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                }
                            }
                        }
                    }
                    
                    IconButton(onClick = { filePickerLauncher.launch("text/plain") }, modifier = Modifier.height(56.dp).padding(end = 4.dp)) {
                        Icon(Icons.Default.FileOpen, contentDescription = "Batch Download from TXT")
                    }

                    Button(
                        onClick = {
                            if (isUrl) {
                                formatDialogUrl = urlInput
                            } else {
                                isSearchLoading = true
                                searchError = null
                                coroutineScope.launch {
                                    try {
                                        searchResults = viewModel.searchYouTube(urlInput)
                                        if (searchResults.isEmpty()) {
                                            searchError = "No results found"
                                        }
                                    } catch (e: Exception) {
                                        searchError = "Search failed: ${e.message}"
                                    } finally {
                                        isSearchLoading = false
                                    }
                                }
                            }
                        },
                        modifier = Modifier.height(56.dp)
                    ) {
                        Text(if (isUrl) "Download" else "Search")
                    }
                }'''
content = content.replace(target_ui, rep_ui)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)

print("done batch")
