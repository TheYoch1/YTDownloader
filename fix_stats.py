import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

stats_funcs = '''
    private fun recordDownloadStats() {
        val context = getApplication<Application>()
        val prefs = context.getSharedPreferences("download_stats", Context.MODE_PRIVATE)
        val today = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
        
        val countKey = "count_$today"
        val count = prefs.getInt(countKey, 0)
        prefs.edit().putInt(countKey, count + 1).apply()
    }
'''

content = content + stats_funcs

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
print("done stats")
