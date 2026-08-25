with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

content = content.replace('file.appendText("${System.currentTimeMillis()}: $error\\n")', 'file.appendText("${System.currentTimeMillis()}: $error\\n")')
# Actually wait, let's just use re to replace the specific block

target = '''            file.appendText("${System.currentTimeMillis()}: $error
")'''

replacement = '''            file.appendText("${System.currentTimeMillis()}: $error\\n")'''

content = content.replace(target, replacement)
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)

