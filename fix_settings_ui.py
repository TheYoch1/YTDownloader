import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# I will replace from 'Text("App Settings"' down to 'Text("Save Directory"'

start_str = '            Text(\n                "App Settings",\n                style = MaterialTheme.typography.headlineSmall,'
end_str = '            Text("Save Directory", style = MaterialTheme.typography.labelMedium)'

idx1 = content.find(start_str)
idx2 = content.find(end_str)

new_section = """            Text(
                "App Settings",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )
            
            // Calculate storage used by YT Downloader
            var totalYtSize by remember { mutableStateOf(0L) }
            val stat = android.os.StatFs(android.os.Environment.getExternalStorageDirectory().path)
            val totalSpace = stat.totalBytes
            
            LaunchedEffect(Unit) {
                kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
                    var size = 0L
                    listOf(
                        "/storage/emulated/0/Download/YT Downloader",
                        "/storage/emulated/0/Movies/YT Downloader",
                        "/storage/emulated/0/Music/YT Downloader"
                    ).forEach { path ->
                        val dir = java.io.File(path)
                        if (dir.exists() && dir.isDirectory) {
                            dir.walkTopDown().filter { it.isFile }.forEach { size += it.length() }
                        }
                    }
                    totalYtSize = size
                }
            }
            
            Card(
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
                colors = androidx.compose.material3.CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    val sizeMB = totalYtSize / (1024f * 1024f)
                    val sizeGB = totalYtSize / (1024f * 1024f * 1024f)
                    val displaySize = if (sizeGB > 1.0) String.format("%.2f GB", sizeGB) else String.format("%.1f MB", sizeMB)
                    
                    Text("YT Downloader Storage Used: $displaySize", fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(8.dp))
                    LinearProgressIndicator(
                        progress = (totalYtSize.toFloat() / totalSpace.toFloat().coerceAtLeast(1f)).coerceIn(0f, 1f),
                        modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp))
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        "Total Device Storage: ${String.format("%.1f GB", totalSpace / (1024f * 1024f * 1024f))}", 
                        style = MaterialTheme.typography.bodySmall, 
                        modifier = Modifier.align(Alignment.End)
                    )
                }
            }
            
"""

if idx1 != -1 and idx2 != -1:
    content = content[:idx1] + new_section + content[idx2:]

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
