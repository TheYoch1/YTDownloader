import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

text = text.replace(
    'const val ACTION_STOP_DOWNLOAD = "ACTION_STOP_DOWNLOAD"',
    'const val ACTION_STOP_DOWNLOAD = "ACTION_STOP_DOWNLOAD"\n        const val ACTION_CHECK_QUEUE = "ACTION_CHECK_QUEUE"'
)

text = text.replace(
    '        return START_NOT_STICKY\n    }',
    '        } else if (action == ACTION_CHECK_QUEUE) {\n            checkQueue()\n        }\n\n        return START_NOT_STICKY\n    }'
)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

old_config_change = """                onValueChange = { 
                    onConfigChanged(config.copy(maxConcurrentDownloads = it.toInt()))
                },"""
new_config_change = """                onValueChange = { 
                    onConfigChanged(config.copy(maxConcurrentDownloads = it.toInt()))
                    val intent = android.content.Intent(context, DownloadService::class.java).apply {
                        action = DownloadService.ACTION_CHECK_QUEUE
                    }
                    androidx.core.content.ContextCompat.startForegroundService(context, intent)
                },"""
text = text.replace(old_config_change, new_config_change)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
