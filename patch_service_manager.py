with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

manager_code = """import java.util.concurrent.ConcurrentHashMap
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

object DownloadManager {
    private val _progressMap = MutableStateFlow<Map<String, Float>>(emptyMap())
    val progressMap: StateFlow<Map<String, Float>> = _progressMap.asStateFlow()

    fun updateProgress(id: String, progress: Float) {
        _progressMap.update { it + (id to progress) }
    }
    
    fun removeProgress(id: String) {
        _progressMap.update { it - id }
    }
}
"""
text = text.replace("import java.util.concurrent.ConcurrentHashMap", manager_code)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)

