import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """                        detectTapGestures(
                            onLongPress = {
                                clipboardManager.setText(AnnotatedString(download.errorMessage ?: ""))
                            }
                        )"""

replacement = """                        detectTapGestures(
                            onLongPress = {
                                clipboardManager.setText(AnnotatedString(download.errorMessage ?: ""))
                                android.widget.Toast.makeText(context, "Error copied to clipboard", android.widget.Toast.LENGTH_SHORT).show()
                            }
                        )"""

content = content.replace(target, replacement)

target_log_toast = """                                    onLongPress = {
                                        clipboardManager.setText(AnnotatedString(logText))
                                    }
                                )"""
replacement_log_toast = """                                    onLongPress = {
                                        clipboardManager.setText(AnnotatedString(logText))
                                        android.widget.Toast.makeText(context, "Log copied to clipboard", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                )"""
content = content.replace(target_log_toast, replacement_log_toast)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
