import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f)
        )"""

replacement = """        colors = CardDefaults.cardColors(
            containerColor = when (download.status) {
                "Completed" -> Color(0xFF4CAF50).copy(alpha = 0.2f)
                "Downloading", "Extracting" -> Color(0xFF2196F3).copy(alpha = 0.2f)
                "Queued", "Paused" -> Color(0xFFFFC107).copy(alpha = 0.2f)
                "Error", "Cancelled" -> Color(0xFFF44336).copy(alpha = 0.2f)
                else -> MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f)
            }
        )"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
