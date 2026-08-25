import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                        fileToCopy.copyTo(destFile, overwrite = false)
                        if (savedFileUri == null || (!fileToCopy.name.endsWith(".vtt") && !fileToCopy.name.endsWith(".srt"))) {
                            savedFileUri = "file://" + destFile.absolutePath
                        }
                    }
                }
            }'''

rep = '''                        fileToCopy.copyTo(destFile, overwrite = false)
                        if (savedFileUri == null || (!fileToCopy.name.endsWith(".vtt") && !fileToCopy.name.endsWith(".srt"))) {
                            savedFileUri = "file://" + destFile.absolutePath
                            recordDownloadStatsSize(destFile.length())
                        }
                    }
                }
            }'''

content = content.replace(target, rep)

stats_target = '''    private fun recordDownloadStats() {
        val context = getApplication<Application>()
        val prefs = context.getSharedPreferences("download_stats", Context.MODE_PRIVATE)
        val today = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
        
        val countKey = "count_$today"
        val count = prefs.getInt(countKey, 0)
        prefs.edit().putInt(countKey, count + 1).apply()
    }'''

stats_rep = '''    private fun recordDownloadStats() {
        // Called in finally, can be used for general cleanup if needed. Count is now handled in recordDownloadStatsSize.
    }
    
    private fun recordDownloadStatsSize(bytes: Long) {
        val context = getApplication<Application>()
        val prefs = context.getSharedPreferences("download_stats", Context.MODE_PRIVATE)
        val today = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
        
        val countKey = "count_$today"
        val count = prefs.getInt(countKey, 0)
        
        val sizeKey = "size_$today"
        val size = prefs.getLong(sizeKey, 0L)
        
        prefs.edit()
            .putInt(countKey, count + 1)
            .putLong(sizeKey, size + bytes)
            .apply()
    }'''

content = content.replace(stats_target, stats_rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
print("done stats size")
