import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = '''                    IconButton(onClick = { filePickerLauncher.launch("text/plain") }, modifier = Modifier.height(56.dp).padding(end = 4.dp)) {
                        Icon(Icons.Default.FileOpen, contentDescription = "Batch Download from TXT")
                    }'''

rep = '''                    OutlinedButton(
                        onClick = { filePickerLauncher.launch("text/plain") },
                        modifier = Modifier.height(56.dp).padding(end = 4.dp),
                        contentPadding = PaddingValues(horizontal = 12.dp)
                    ) {
                        Icon(Icons.Default.FileOpen, contentDescription = null, modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("TXT")
                    }'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)

print("done")
