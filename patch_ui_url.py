import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target_url = """                            if (isUrl) {
                                formatDialogUrl = urlInput
                                formatDialogTitle = null
                            } else {"""
rep_url = """                            if (isUrl) {
                                if (urlInput.contains("list=")) {
                                    viewModel.addDownload(urlInput, null, null)
                                    urlInput = ""
                                } else {
                                    formatDialogUrl = urlInput
                                    formatDialogTitle = null
                                }
                            } else {"""
content = content.replace(target_url, rep_url)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
