import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target_state = "    val isStorageFull by viewModel.isStorageFull.collectAsState()"
rep_state = """    val isStorageFull by viewModel.isStorageFull.collectAsState()
    var dismissedStorageDialog by remember(isStorageFull) { mutableStateOf(false) }"""
content = content.replace(target_state, rep_state)

target_dialog = """    if (isStorageFull) {
        AlertDialog(
            onDismissRequest = { },"""
rep_dialog = """    if (isStorageFull && !dismissedStorageDialog) {
        AlertDialog(
            onDismissRequest = { dismissedStorageDialog = true },"""
content = content.replace(target_dialog, rep_dialog)

target_dismiss = """            dismissButton = {
                TextButton(onClick = { /* keep showing if they dismiss? well, we let them dismiss if they want to ignore it */ }) {
                    Text("Dismiss")
                }
            }"""
rep_dismiss = """            dismissButton = {
                TextButton(onClick = { dismissedStorageDialog = true }) {
                    Text("Dismiss")
                }
            }"""
content = content.replace(target_dismiss, rep_dismiss)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
