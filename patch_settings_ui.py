import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Tag Audio File")"""

replacement = """            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Max Concurrent Downloads: ${config.maxConcurrentDownloads}")
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = { if (config.maxConcurrentDownloads > 1) onConfigChanged(config.copy(maxConcurrentDownloads = config.maxConcurrentDownloads - 1)) }) {
                        Text("-", style = MaterialTheme.typography.titleLarge)
                    }
                    IconButton(onClick = { if (config.maxConcurrentDownloads < 5) onConfigChanged(config.copy(maxConcurrentDownloads = config.maxConcurrentDownloads + 1)) }) {
                        Text("+", style = MaterialTheme.typography.titleLarge)
                    }
                }
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Tag Audio File")"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
