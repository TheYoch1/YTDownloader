import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target_imports = "import kotlinx.coroutines.CompletableDeferred"
rep_imports = """import kotlinx.coroutines.CompletableDeferred
import android.os.Environment
import android.os.StatFs
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import android.content.Intent
import android.provider.Settings"""
content = content.replace(target_imports, rep_imports)

# Add Storage State to View Model
target_class = "class DownloaderViewModel(application: Application) : AndroidViewModel(application) {"
rep_class = """class DownloaderViewModel(application: Application) : AndroidViewModel(application) {
    val isStorageFull = MutableStateFlow(false)
    
    init {
        // Monitor storage space periodically
        viewModelScope.launch(Dispatchers.IO) {
            while (true) {
                try {
                    val stat = StatFs(Environment.getExternalStorageDirectory().path)
                    val bytesAvailable = stat.availableBlocksLong * stat.blockSizeLong
                    val isFull = bytesAvailable < 500 * 1024 * 1024 // 500 MB threshold
                    if (isFull != isStorageFull.value) {
                        isStorageFull.value = isFull
                        if (!isFull) {
                            // Storage freed, auto-resume any Paused downloads
                            _downloadQueue.update { q ->
                                q.map { if (it.status == "Paused") it.copy(status = "Downloading", downloadSpeed = "Resuming...") else it }
                            }
                        } else {
                            // Storage full, auto-pause active downloads
                            _downloadQueue.update { q ->
                                q.map { if (it.status == "Downloading") it.copy(status = "Paused", downloadSpeed = "No Space") else it }
                            }
                        }
                    }
                } catch (e: Exception) {}
                delay(5000)
            }
        }
    }"""
content = content.replace(target_class, rep_class)

# Pre-flight check inside execute loop
target_exec = "YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->"
rep_exec = """                while (isStorageFull.value && _downloadQueue.value.find { it.id == id }?.status != "Cancelled") {
                    kotlinx.coroutines.delay(2000)
                }
                
                YoutubeDL.getInstance().execute(request, id) { progress, etaInSeconds, line ->"""
content = content.replace(target_exec, rep_exec)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
