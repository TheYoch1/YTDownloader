with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

import re

old_ui = """            } else {
                val lazyListState = rememberLazyListState()
                val reorderableLazyColumnState = rememberReorderableLazyColumnState(
                    lazyListState,
                    onMove = { from, to ->
                        viewModel.reorderQueue(from.index, to.index)
                    }
                )"""

new_ui = """            } else {
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
                
                val lazyListState = rememberLazyListState()
                val reorderableLazyColumnState = rememberReorderableLazyColumnState(
                    lazyListState,
                    onMove = { from, to ->
                        viewModel.reorderQueue(from.index, to.index)
                    }
                )"""

text = text.replace(old_ui, new_ui)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
