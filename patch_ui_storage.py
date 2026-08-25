import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target_state = "    val conflictState by viewModel.fileConflictState.collectAsState()"
rep_state = """    val conflictState by viewModel.fileConflictState.collectAsState()
    val isStorageFull by viewModel.isStorageFull.collectAsState()"""
content = content.replace(target_state, rep_state)

target_dialog = """    conflictState?.let { conflict ->"""
rep_dialog = """    if (isStorageFull) {
        AlertDialog(
            onDismissRequest = { },
            icon = { Icon(Icons.Default.WarningAmber, contentDescription = null) },
            title = { Text("Storage Full") },
            text = { Text("Your device has less than 500MB of free space. Downloads have been paused. Please free up some space, and downloads will automatically resume.") },
            confirmButton = {
                TextButton(onClick = { 
                    context.startActivity(android.content.Intent(android.provider.Settings.ACTION_INTERNAL_STORAGE_SETTINGS))
                }) {
                    Text("Free Up Space")
                }
            },
            dismissButton = {
                TextButton(onClick = { /* keep showing if they dismiss? well, we let them dismiss if they want to ignore it */ }) {
                    Text("Dismiss")
                }
            }
        )
    }

    conflictState?.let { conflict ->"""
content = content.replace(target_dialog, rep_dialog)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
