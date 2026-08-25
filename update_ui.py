import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

# Make sure we don't change anything else unintentionally. 
# Update the UI inside DownloadItemCard:

old_ui = """                    if (download.isPlaylist && download.totalItems > 0) {
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "Downloading ${download.currentItemIndex} of ${download.totalItems}",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.secondary,
                            fontWeight = FontWeight.Bold
                        )
                        if (download.currentDownloadingTitle.isNotEmpty()) {
                            Text(
                                text = "Current: ${download.currentDownloadingTitle}",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.secondary,
                                maxLines = 1,
                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                            )
                        }
                    }"""

new_ui = """                    if (download.isPlaylist && download.totalItems > 0) {
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "Downloading ${download.currentItemIndex} of ${download.totalItems}: ${download.currentDownloadingTitle}",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.secondary,
                            maxLines = 1,
                            overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                        )
                    }"""

text = text.replace(old_ui, new_ui)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
