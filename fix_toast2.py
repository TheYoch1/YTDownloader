import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """@Composable
fun DownloadItemCard(
    download: QueuedDownload,
    onRemove: () -> Unit,
    onCancel: () -> Unit,
    onPause: () -> Unit,
    onResume: () -> Unit
) {"""

replacement = """@Composable
fun DownloadItemCard(
    download: QueuedDownload,
    onRemove: () -> Unit,
    onCancel: () -> Unit,
    onPause: () -> Unit,
    onResume: () -> Unit
) {
    val context = LocalContext.current"""

if target in content:
    content = content.replace(target, replacement)
    print("Fixed")
else:
    print("Not found")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
