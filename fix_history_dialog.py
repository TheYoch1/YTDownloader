import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("var showErrorLog by remember { mutableStateOf(false) }", "var showErrorLog by remember { mutableStateOf(false) }\n    var showHistoryLog by remember { mutableStateOf(false) }")
content = content.replace("onViewErrorLog = { showErrorLog = true }", "onViewErrorLog = { showErrorLog = true },\n                onViewHistoryLog = { showHistoryLog = true }")
content = content.replace("val onViewErrorLog: () -> Unit", "val onViewErrorLog: () -> Unit,\n    val onViewHistoryLog: () -> Unit")
content = content.replace("onClick = { onDismiss(); onViewErrorLog() }", "onClick = { onDismiss(); onViewErrorLog() }")

# Add the dialog just below the Error Log dialog
dialog_str = """
    if (showHistoryLog) {
        val historyFile = java.io.File(LocalContext.current.filesDir, "history.log")
        val historyContent = remember { 
            if (historyFile.exists()) historyFile.readText().lines().filter { it.isNotBlank() }.reversed().take(50).joinToString("\\n")
            else "No download history found."
        }
        AlertDialog(
            onDismissRequest = { showHistoryLog = false },
            title = { Text("Download History") },
            text = {
                Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                    Text(historyContent, style = MaterialTheme.typography.bodySmall, modifier = Modifier.fillMaxWidth())
                }
            },
            confirmButton = {
                Button(onClick = { showHistoryLog = false }) { Text("Close") }
            },
            dismissButton = {
                TextButton(onClick = { 
                    if (historyFile.exists()) historyFile.delete()
                    showHistoryLog = false
                }) {
                    Text("Clear")
                }
            }
        )
    }
"""

# inject after showErrorLog dialog
error_log_close = "showErrorLog = false\n                }) {\n                    Text(\"Clear\")\n                }\n            }\n        )"
content = content.replace(error_log_close, error_log_close + dialog_str)

# add the button in settings
settings_btn_target = """            TextButton(
                onClick = { onDismiss(); onViewErrorLog() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("View Error Log")
            }"""
settings_btn_rep = """            TextButton(
                onClick = { onDismiss(); onViewHistoryLog() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("View History Log")
            }
            
            TextButton(
                onClick = { onDismiss(); onViewErrorLog() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("View Error Log")
            }"""
content = content.replace(settings_btn_target, settings_btn_rep)


with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
