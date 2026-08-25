import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Import BackHandler
if "import androidx.activity.compose.BackHandler" not in content:
    content = content.replace("import androidx.activity.compose.setContent", "import androidx.activity.compose.setContent\nimport androidx.activity.compose.BackHandler")

# 2. Update formatDialogUrl defaults
target_format_dialog = """    if (formatDialogUrl != null) {
        var isAudio by remember(formatDialogUrl) { mutableStateOf(settings.audioOnly) }"""
replacement_format_dialog = """    if (formatDialogUrl != null) {
        var isAudio by remember(formatDialogUrl) { mutableStateOf(false) }"""
if target_format_dialog in content:
    content = content.replace(target_format_dialog, replacement_format_dialog)
else:
    print("Could not find formatDialogUrl target")

# 3. Add BackHandler
target_backhandler = """    val coroutineScope = rememberCoroutineScope()"""
replacement_backhandler = """    val coroutineScope = rememberCoroutineScope()
    
    BackHandler {
        (context as? android.app.Activity)?.moveTaskToBack(true)
    }"""
if target_backhandler in content:
    content = content.replace(target_backhandler, replacement_backhandler)
else:
    print("Could not find backhandler target")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
