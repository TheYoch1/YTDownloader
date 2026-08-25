import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = '''            TextButton(
                onClick = { onDismiss(); onViewErrorLog() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("View Error Log")
            }'''

rep = '''            TextButton(
                onClick = { onDismiss(); onViewErrorLog() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("View Error Log")
            }
            
            TextButton(
                onClick = { 
                    android.widget.Toast.makeText(context, "Updating engine in background...", android.widget.Toast.LENGTH_SHORT).show()
                    kotlinx.coroutines.GlobalScope.launch(kotlinx.coroutines.Dispatchers.IO) {
                        try {
                            com.yausername.youtubedl_android.YoutubeDL.getInstance().updateYoutubeDL(context, com.yausername.youtubedl_android.YoutubeDL.UpdateChannel.NIGHTLY)
                            kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                                android.widget.Toast.makeText(context, "Engine updated successfully", android.widget.Toast.LENGTH_SHORT).show()
                            }
                        } catch (e: Exception) {
                            kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                                android.widget.Toast.makeText(context, "Update failed: ${e.message}", android.widget.Toast.LENGTH_LONG).show()
                            }
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Force Update Engine")
            }'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
