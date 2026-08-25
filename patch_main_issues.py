import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

# 1. Dialog LazyColumn height
old_lazy = "LazyColumn(modifier = Modifier.height(150.dp)) {"
new_lazy = "LazyColumn(modifier = Modifier.heightIn(max = 400.dp)) {"
text = text.replace(old_lazy, new_lazy)

# 2. Sorting dropdown removal
old_sort_ui = """            } else {
                var sortMenuExpanded by remember { mutableStateOf(false) }
                val sortOptions = listOf("Newest First", "Oldest First", "Alphabetical")
                var selectedSort by remember { mutableStateOf(sortOptions[0]) }

                Row(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp, vertical = 4.dp),
                    horizontalArrangement = Arrangement.End,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Sort: ", style = MaterialTheme.typography.bodyMedium)
                    Box {
                        TextButton(onClick = { sortMenuExpanded = true }) {
                            Text(selectedSort)
                            Icon(Icons.Default.ArrowDropDown, contentDescription = "Sort Options")
                        }
                        DropdownMenu(
                            expanded = sortMenuExpanded,
                            onDismissRequest = { sortMenuExpanded = false }
                        ) {
                            sortOptions.forEach { option ->
                                DropdownMenuItem(
                                    text = { Text(option) },
                                    onClick = {
                                        selectedSort = option
                                        sortMenuExpanded = false
                                        viewModel.sortQueue(option)
                                    }
                                )
                            }
                        }
                    }
                }
                
                val lazyListState = rememberLazyListState()"""

new_sort_ui = """            } else {
                val lazyListState = rememberLazyListState()"""
text = text.replace(old_sort_ui, new_sort_ui)

# 3. Download card stability (filteredActiveDownloads)
old_filtered = 'val filteredActiveDownloads = downloads.filter { it.status == "Downloading" || it.status == "Extracting" || it.status == "Queued" || it.status == "Paused" || it.status == "Completed" || it.status == "Error" }'
new_filtered = 'val filteredActiveDownloads = downloads.filter { it.status != "Cancelled" }'
text = text.replace(old_filtered, new_filtered)

# 4. Global progress bar fix
old_avg_prog = """                val avgProgress = activeDownloads.map { it.progress }.average().toFloat()"""
new_avg_prog = """                val totalFiles = activeDownloads.sumOf { if (it.isPlaylist && it.totalItems > 0) it.totalItems else 1 }
                val completedFilesProgress = activeDownloads.sumOf { 
                    val items = if (it.isPlaylist && it.totalItems > 0) it.totalItems else 1
                    (it.progress.toDouble() / 100.0) * items
                }
                val avgProgress = if (totalFiles > 0) (completedFilesProgress / totalFiles.toDouble() * 100.0).toFloat() else 0f"""
text = text.replace(old_avg_prog, new_avg_prog)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)

print("Main patched")
