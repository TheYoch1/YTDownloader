import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target_process = '''        try {
            val itemInfo = _downloadQueue.value.find { it.id == id }
            if (itemInfo == null || itemInfo.status == "Cancelled") return'''

rep_process = '''        try {
            val itemInfo = _downloadQueue.value.find { it.id == id }
            if (itemInfo == null || itemInfo.status == "Cancelled") return
            
            if (_appConfig.value.wifiOnly && !NetworkMonitor.isWifiConnected.value) {
                _downloadQueue.update { q -> q.map { if (it.id == id) it.copy(status = "Error", errorMessage = "Wi-Fi connection required.") else it } }
                return
            }'''

content = content.replace(target_process, rep_process)

target_add = '''        if (!NetworkMonitor.isConnected.value) {
            val newDownload = QueuedDownload(
                id = java.util.UUID.randomUUID().toString(),
                title = initialTitle ?: url,
                url = url,
                isPlaylist = url.contains("list="),
                status = "Error",
                errorMessage = "No internet connection available.",
                settings = specificSettings ?: _currentSettings.value.copy()
            )
            _downloadQueue.update { it + newDownload }
            return
        }'''

rep_add = '''        if (!NetworkMonitor.isConnected.value) {
            val newDownload = QueuedDownload(
                id = java.util.UUID.randomUUID().toString(),
                title = initialTitle ?: url,
                url = url,
                isPlaylist = url.contains("list="),
                status = "Error",
                errorMessage = "No internet connection available.",
                settings = specificSettings ?: _currentSettings.value.copy()
            )
            _downloadQueue.update { it + newDownload }
            return
        }
        
        if (_appConfig.value.wifiOnly && !NetworkMonitor.isWifiConnected.value) {
            val newDownload = QueuedDownload(
                id = java.util.UUID.randomUUID().toString(),
                title = initialTitle ?: url,
                url = url,
                isPlaylist = url.contains("list="),
                status = "Error",
                errorMessage = "Wi-Fi connection required.",
                settings = specificSettings ?: _currentSettings.value.copy()
            )
            _downloadQueue.update { it + newDownload }
            return
        }'''

content = content.replace(target_add, rep_add)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
