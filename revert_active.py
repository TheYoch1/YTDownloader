with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

old_active = """val activeDownloads = downloads.filter { it.status == "Downloading" || it.status == "Extracting" || it.status == "Finishing" || it.status == "Queued" }"""
new_active = """val activeDownloads = downloads.filter { it.status != "Cancelled" }"""
text = text.replace(old_active, new_active)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
