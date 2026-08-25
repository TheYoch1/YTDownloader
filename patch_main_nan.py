import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

text = text.replace("progress = { if (avgProgress.isNaN()) 0f else (avgProgress / 100f).coerceIn(0f, 1f) }", "progress = { if (avgProgress.isNaN()) 0f else (avgProgress / 100f).coerceIn(0f, 1f) }")
text = text.replace("progress = { download.progress / 100f }", "progress = { if (download.progress.isNaN()) 0f else (download.progress / 100f).coerceIn(0f, 1f) }")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)

print("Main nan patched")
