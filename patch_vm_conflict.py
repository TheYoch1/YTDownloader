import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target_imports = "import kotlinx.coroutines.flow.MutableStateFlow"
rep_imports = """import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.CompletableDeferred
import androidx.documentfile.provider.DocumentFile"""
content = content.replace(target_imports, rep_imports)

target_class_start = "class DownloaderViewModel(application: Application) : AndroidViewModel(application) {"
rep_class_start = """enum class ConflictResolution { SKIP, OVERWRITE, KEEP_BOTH }
data class ConflictDialogState(val fileName: String, val deferred: CompletableDeferred<ConflictResolution>)

class DownloaderViewModel(application: Application) : AndroidViewModel(application) {
    val fileConflictState = MutableStateFlow<ConflictDialogState?>(null)
    
    fun resolveConflict(resolution: ConflictResolution) {
        fileConflictState.value?.deferred?.complete(resolution)
    }"""
content = content.replace(target_class_start, rep_class_start)

# Now, we need to update the file copy loop.
# It currently is:
target_loop = """                tmpDir?.walkTopDown()?.filter { it.isFile }?.forEach { fileToCopy ->
                    if (finalSaveDirStr.startsWith("content://")) {
                        val treeUri = Uri.parse(finalSaveDirStr)
                        var docFile = DocumentFile.fromTreeUri(application, treeUri)
                        
                        if (docFile != null && docFile.name != "YT Downloader") {
                            var ytFolder = docFile.findFile("YT Downloader")
                            if (ytFolder == null) {
                                ytFolder = docFile.createDirectory("YT Downloader")
                            }
                            if (ytFolder != null) docFile = ytFolder
                        }
                        
                        if (isPlaylist && docFile != null) {
                            val playlistFolderName = titleStr.replace(Regex("[\\\\/:*?\"<>|]"), "_")
                            var playlistFolder = docFile.findFile(playlistFolderName)
                            if (playlistFolder == null) {
                                playlistFolder = docFile.createDirectory(playlistFolderName)
                            }
                            docFile = playlistFolder
                        }
                        
                        if (docFile != null) {
                            var mimeType = "application/octet-stream"
                            if (fileToCopy.name.endsWith(".mp3") || fileToCopy.name.endsWith(".m4a")) mimeType = "audio/*"
                            else if (fileToCopy.name.endsWith(".mp4") || fileToCopy.name.endsWith(".webm") || fileToCopy.name.endsWith(".mkv")) mimeType = "video/*"
                            else if (fileToCopy.name.endsWith(".vtt") || fileToCopy.name.endsWith(".srt")) mimeType = "text/plain"
                            
                            val newFile = docFile.createFile(mimeType, fileToCopy.name)
                            if (newFile != null) {
                                application.contentResolver.openOutputStream(newFile.uri)?.use { out ->
                                    fileToCopy.inputStream().use { input ->
                                        input.copyTo(out)
                                    }
                                }
                            }
                        }
                    } else {
                        // Fallback for standard paths
                        val destDir = File(finalSaveDirStr)
                        if (!destDir.exists()) destDir.mkdirs()
                        val destFile = File(destDir, fileToCopy.name)
                        fileToCopy.copyTo(destFile, overwrite = true)
                    }
                }"""

rep_loop = """                tmpDir?.walkTopDown()?.filter { it.isFile }?.forEach { fileToCopy ->
                    if (finalSaveDirStr.startsWith("content://")) {
                        val treeUri = Uri.parse(finalSaveDirStr)
                        var docFile = DocumentFile.fromTreeUri(application, treeUri)
                        
                        if (docFile != null && docFile.name != "YT Downloader") {
                            var ytFolder = docFile.findFile("YT Downloader")
                            if (ytFolder == null) {
                                ytFolder = docFile.createDirectory("YT Downloader")
                            }
                            if (ytFolder != null) docFile = ytFolder
                        }
                        
                        if (isPlaylist && docFile != null) {
                            val playlistFolderName = titleStr.replace(Regex("[\\\\/:*?\"<>|]"), "_")
                            var playlistFolder = docFile.findFile(playlistFolderName)
                            if (playlistFolder == null) {
                                playlistFolder = docFile.createDirectory(playlistFolderName)
                            }
                            docFile = playlistFolder
                        }
                        
                        if (docFile != null) {
                            var mimeType = "application/octet-stream"
                            if (fileToCopy.name.endsWith(".mp3") || fileToCopy.name.endsWith(".m4a")) mimeType = "audio/*"
                            else if (fileToCopy.name.endsWith(".mp4") || fileToCopy.name.endsWith(".webm") || fileToCopy.name.endsWith(".mkv")) mimeType = "video/*"
                            else if (fileToCopy.name.endsWith(".vtt") || fileToCopy.name.endsWith(".srt")) mimeType = "text/plain"
                            
                            val existingFile = docFile.findFile(fileToCopy.name)
                            var resolution = ConflictResolution.OVERWRITE
                            if (existingFile != null) {
                                val deferred = CompletableDeferred<ConflictResolution>()
                                fileConflictState.value = ConflictDialogState(fileToCopy.name, deferred)
                                resolution = kotlinx.coroutines.runBlocking { deferred.await() }
                                fileConflictState.value = null
                            }
                            
                            if (resolution == ConflictResolution.OVERWRITE || resolution == ConflictResolution.KEEP_BOTH) {
                                if (resolution == ConflictResolution.OVERWRITE && existingFile != null) {
                                    existingFile.delete()
                                }
                                
                                var finalName = fileToCopy.name
                                if (resolution == ConflictResolution.KEEP_BOTH) {
                                    val nameWithoutExt = fileToCopy.nameWithoutExtension
                                    val ext = fileToCopy.extension
                                    var i = 1
                                    while (docFile?.findFile("$nameWithoutExt ($i).$ext") != null) {
                                        i++
                                    }
                                    finalName = "$nameWithoutExt ($i).$ext"
                                }
                                
                                val newFile = docFile!!.createFile(mimeType, finalName)
                                if (newFile != null) {
                                    application.contentResolver.openOutputStream(newFile.uri)?.use { out ->
                                        fileToCopy.inputStream().use { input ->
                                            input.copyTo(out)
                                        }
                                    }
                                }
                            }
                        }
                    } else {
                        // Fallback for standard paths
                        val destDir = File(finalSaveDirStr)
                        if (!destDir.exists()) destDir.mkdirs()
                        val destFile = File(destDir, fileToCopy.name)
                        
                        var resolution = ConflictResolution.OVERWRITE
                        if (destFile.exists()) {
                            val deferred = CompletableDeferred<ConflictResolution>()
                            fileConflictState.value = ConflictDialogState(fileToCopy.name, deferred)
                            resolution = kotlinx.coroutines.runBlocking { deferred.await() }
                            fileConflictState.value = null
                        }
                        
                        if (resolution == ConflictResolution.OVERWRITE) {
                            fileToCopy.copyTo(destFile, overwrite = true)
                        } else if (resolution == ConflictResolution.KEEP_BOTH) {
                            val nameWithoutExt = fileToCopy.nameWithoutExtension
                            val ext = fileToCopy.extension
                            var i = 1
                            var newDestFile = File(destDir, "$nameWithoutExt ($i).$ext")
                            while (newDestFile.exists()) {
                                i++
                                newDestFile = File(destDir, "$nameWithoutExt ($i).$ext")
                            }
                            fileToCopy.copyTo(newDestFile, overwrite = false)
                        }
                    }
                }"""
content = content.replace(target_loop, rep_loop)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
