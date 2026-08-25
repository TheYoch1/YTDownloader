with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target1 = '''            val isPlaylist = itemInfo.isPlaylist
            var titleStr = itemInfo.title
            
            withContext(Dispatchers.IO) {'''
rep1 = '''            val isPlaylist = itemInfo.isPlaylist
            var titleStr = itemInfo.title
            var finalSaveDirStr = ""
            var savedFileUri: String? = null
            
            withContext(Dispatchers.IO) {'''
content = content.replace(target1, rep1)

target2 = '''                val finalSaveDirStr = if (isPlaylist) {'''
rep2 = '''                finalSaveDirStr = if (isPlaylist) {'''
content = content.replace(target2, rep2)

target3 = '''                var savedFileUri: String? = null
                tmpDir?.walkTopDown()?.filter { it.isFile }?.forEach { fileToCopy ->'''
rep3 = '''                tmpDir?.walkTopDown()?.filter { it.isFile }?.forEach { fileToCopy ->'''
content = content.replace(target3, rep3)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
