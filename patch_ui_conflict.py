import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target_imports = "import androidx.compose.material.icons.filled.Refresh"
rep_imports = "import androidx.compose.material.icons.filled.Refresh\nimport androidx.compose.material.icons.filled.WarningAmber"
content = content.replace(target_imports, rep_imports)

target_state = "    val isConnected by NetworkMonitor.isConnected.collectAsState()"
rep_state = """    val isConnected by NetworkMonitor.isConnected.collectAsState()
    val conflictState by viewModel.fileConflictState.collectAsState()"""
content = content.replace(target_state, rep_state)

# Insert the conflict dialog at the end of MainScreen
target_end = """        }
    }

    if (showSettings) {"""
rep_end = """        }
    }
    
    conflictState?.let { conflict ->
        AlertDialog(
            onDismissRequest = { /* Must choose an action */ },
            icon = { Icon(Icons.Default.WarningAmber, contentDescription = null) },
            title = { Text("File Already Exists") },
            text = { Text("The file '${conflict.fileName}' already exists in this folder. What would you like to do?") },
            confirmButton = {
                TextButton(onClick = { viewModel.resolveConflict(ConflictResolution.OVERWRITE) }) {
                    Text("Overwrite")
                }
            },
            dismissButton = {
                Row {
                    TextButton(onClick = { viewModel.resolveConflict(ConflictResolution.SKIP) }) {
                        Text("Skip")
                    }
                    TextButton(onClick = { viewModel.resolveConflict(ConflictResolution.KEEP_BOTH) }) {
                        Text("Keep Both")
                    }
                }
            }
        )
    }

    if (showSettings) {"""
content = content.replace(target_end, rep_end)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
