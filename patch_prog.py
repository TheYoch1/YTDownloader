with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

old = """                        progress = { if (avgProgress.isNaN()) 0f else avgProgress / 100f },"""
new = """                        progress = { if (avgProgress.isNaN()) 0f else (avgProgress / 100f).coerceIn(0f, 1f) },"""
text = text.replace(old, new)

old_active = """val activeDownloads = downloads.filter { it.status != "Cancelled" }"""
new_active = """val activeDownloads = downloads.filter { it.status == "Downloading" || it.status == "Extracting" || it.status == "Finishing" || it.status == "Queued" }"""
text = text.replace(old_active, new_active)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
