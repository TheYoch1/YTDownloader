with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = "    val context = LocalContext.current"
rep = "    val context = LocalContext.current\n    val clipboardManager = LocalClipboardManager.current"

content = content.replace(target, rep, 1)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
