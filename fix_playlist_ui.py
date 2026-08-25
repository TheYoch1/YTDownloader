import re
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

target = """                    // Show format explicitly (so they know what quality was chosen when queued)
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = if (download.settings.audioOnly) "Format: Audio (MP3)" else "Format: Video (${download.settings.quality.label})",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.primary
                    )"""

replacement = """                    // Show format explicitly (so they know what quality was chosen when queued)
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = if (download.settings.audioOnly) "Format: Audio (MP3)" else "Format: Video (${download.settings.quality.label})",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.primary
                    )
                    
                    if (download.isPlaylist && download.totalItems > 0) {
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "Playlist: ${download.currentItemIndex} of ${download.totalItems}",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.secondary,
                            fontWeight = FontWeight.Bold
                        )
                        if (download.currentItemTitle.isNotEmpty()) {
                            Text(
                                text = "Current: ${download.currentItemTitle}",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.secondary,
                                maxLines = 1,
                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                            )
                        }
                    }"""

if target in text:
    text = text.replace(target, replacement)
    with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
        f.write(text)
    print("Replaced successfully")
else:
    print("Target not found")
