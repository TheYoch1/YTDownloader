import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = '''    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        )
    ) {'''

rep = '''    Card(
        modifier = Modifier.fillMaxWidth().then(
            if (download.status == "Completed" && download.localFilePath != null) {
                Modifier.clickable {
                    val uriStr = download.localFilePath!!
                    val intent = android.content.Intent(android.content.Intent.ACTION_VIEW)
                    val uri = android.net.Uri.parse(uriStr)
                    
                    if (uriStr.startsWith("content://") && download.isPlaylist) {
                        intent.data = uri
                    } else if (uriStr.startsWith("file://")) {
                        val file = java.io.File(uri.path!!)
                        val contentUri = androidx.core.content.FileProvider.getUriForFile(context, "${context.packageName}.provider", file)
                        val mime = if (uriStr.endsWith(".mp4") || uriStr.endsWith(".webm") || uriStr.endsWith(".mkv")) "video/*" else "audio/*"
                        intent.setDataAndType(contentUri, mime)
                        intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    } else {
                        val mime = if (uriStr.endsWith(".mp4") || uriStr.endsWith(".webm") || uriStr.endsWith(".mkv")) "video/*" else "audio/*"
                        intent.setDataAndType(uri, mime)
                        intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    }
                    try {
                        context.startActivity(intent)
                    } catch (e: Exception) {
                        android.widget.Toast.makeText(context, "Could not open file", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }
            } else Modifier
        ),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        )
    ) {'''
content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
