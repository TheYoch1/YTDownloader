import sys

with open('app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt', 'r') as f:
    content = f.read()

# Add imports
imports_to_add = """
import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.material3.SwipeToDismissBox
import androidx.compose.material3.rememberSwipeToDismissBoxState
import androidx.compose.material3.SwipeToDismissBoxValue
import androidx.compose.foundation.shape.RoundedCornerShape
"""

content = content.replace(
    'import androidx.compose.ui.text.style.TextOverflow',
    'import androidx.compose.ui.text.style.TextOverflow' + imports_to_add
)

old_list = """                LazyColumn(
                    modifier = Modifier.weight(1f),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(downloads, key = { it.id }) { download ->
                        DownloadItemCard(
                            download = download,
                            onRemove = { viewModel.removeDownload(download.id) },
                            onCancel = { viewModel.cancelDownload(download.id) }
                        )
                    }
                }"""

new_list = """                LazyColumn(
                    modifier = Modifier.weight(1f),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(downloads, key = { it.id }) { download ->
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
                                    onRemove = { viewModel.removeDownload(download.id) },
                                    onCancel = { viewModel.cancelDownload(download.id) }
                                )
                            }
                        )
                    }
                }"""

content = content.replace(old_list, new_list)

with open('app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt', 'w') as f:
    f.write(content)
