import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = re.compile(r'            Text\(\s*"Downloads",\s*style = MaterialTheme\.typography\.titleLarge,\s*fontWeight = FontWeight\.Bold,\s*modifier = Modifier\.padding\(bottom = 8\.dp\)\s*\)\s*if \(downloads\.isEmpty\(\)\) \{', re.MULTILINE)

rep = '''            var selectedTabIndex by remember { mutableStateOf(0) }
            val tabs = listOf("Active", "History")
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(
                    "Downloads",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(bottom = 8.dp)
                )
                if (selectedTabIndex == 1 && downloads.any { it.status == "Completed" || it.status == "Cancelled" || it.status == "Error" }) {
                    TextButton(onClick = { 
                        val historyIds = downloads.filter { it.status == "Completed" || it.status == "Cancelled" || it.status == "Error" }.map { it.id }
                        historyIds.forEach { viewModel.removeDownload(it) }
                    }) {
                        Text("Clear History")
                    }
                }
            }
            
            TabRow(selectedTabIndex = selectedTabIndex) {
                tabs.forEachIndexed { index, title ->
                    Tab(
                        text = { Text(title) },
                        selected = selectedTabIndex == index,
                        onClick = { selectedTabIndex = index }
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            val filteredDownloads = if (selectedTabIndex == 0) {
                downloads.filter { it.status == "Downloading" || it.status == "Extracting" || it.status == "Queued" || it.status == "Paused" }
            } else {
                downloads.filter { it.status == "Completed" || it.status == "Cancelled" || it.status == "Error" }
            }
            
            if (filteredDownloads.isEmpty()) {'''

content = target.sub(rep, content)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
print("done2")
