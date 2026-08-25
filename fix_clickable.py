import re
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

old_click = """                    if (uriStr.startsWith("content://") && download.isPlaylist) {
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
                    }"""

new_click = """                    val file = java.io.File(if (uriStr.startsWith("file://")) uri.path!! else uriStr)
                    if (file.exists()) {
                        val contentUri = androidx.core.content.FileProvider.getUriForFile(context, "${context.packageName}.provider", file)
                        val mime = if (uriStr.endsWith(".mp4") || uriStr.endsWith(".webm") || uriStr.endsWith(".mkv")) "video/*" else "audio/*"
                        intent.setDataAndType(contentUri, mime)
                        intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    } else if (uriStr.startsWith("content://")) {
                        val mime = if (uriStr.endsWith(".mp4") || uriStr.endsWith(".webm") || uriStr.endsWith(".mkv")) "video/*" else "audio/*"
                        intent.setDataAndType(uri, mime)
                        intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    }"""

text = text.replace(old_click, new_click)
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
