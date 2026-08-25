import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = '''        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp, vertical = 16.dp)
                .padding(bottom = 48.dp)
        ) {
            Text(
                "More Settings",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )'''

rep = '''        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp, vertical = 16.dp)
                .padding(bottom = 48.dp)
                .verticalScroll(rememberScrollState())
        ) {
            Text(
                "Dashboard & History",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )
            
            val prefs = context.getSharedPreferences("download_stats", android.content.Context.MODE_PRIVATE)
            val dateFormat = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault())
            val todayDate = java.util.Date()
            val calendar = java.util.Calendar.getInstance()
            calendar.time = todayDate
            
            var maxCount = 1
            val daysData = mutableListOf<Pair<String, Int>>()
            var totalSaved = 0L
            
            for (i in 6 downTo 0) {
                calendar.time = todayDate
                calendar.add(java.util.Calendar.DAY_OF_YEAR, -i)
                val dateStr = dateFormat.format(calendar.time)
                val displayStr = java.text.SimpleDateFormat("E", java.util.Locale.getDefault()).format(calendar.time)
                
                val count = prefs.getInt("count_$dateStr", 0)
                val size = prefs.getLong("size_$dateStr", 0L)
                totalSaved += size
                if (count > maxCount) maxCount = count
                daysData.add(Pair(displayStr, count))
            }
            
            Card(
                modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp),
                colors = androidx.compose.material3.CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Total Storage Saved: ${String.format("%.1f MB", totalSaved / (1024.0 * 1024.0))}", fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth().height(120.dp),
                        horizontalArrangement = Arrangement.SpaceEvenly,
                        verticalAlignment = Alignment.Bottom
                    ) {
                        daysData.forEach { (day, count) ->
                            Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Bottom) {
                                Text(count.toString(), style = MaterialTheme.typography.labelSmall)
                                Spacer(modifier = Modifier.height(4.dp))
                                androidx.compose.foundation.layout.Box(
                                    modifier = Modifier
                                        .width(20.dp)
                                        .height((100 * (count.toFloat() / maxCount.toFloat())).dp)
                                        .background(MaterialTheme.colorScheme.primary, shape = RoundedCornerShape(topStart = 4.dp, topEnd = 4.dp))
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(day, style = MaterialTheme.typography.labelSmall)
                            }
                        }
                    }
                }
            }
            
            Text(
                "App Settings",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )'''

content = content.replace(target, rep)

target2 = "import androidx.compose.foundation.lazy.items"
rep2 = "import androidx.compose.foundation.lazy.items\nimport androidx.compose.foundation.rememberScrollState\nimport androidx.compose.foundation.verticalScroll"

if "import androidx.compose.foundation.rememberScrollState" not in content:
    content = content.replace(target2, rep2)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
print("done dashboard")
