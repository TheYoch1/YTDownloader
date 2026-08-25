with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

text = text.replace(
    """                    if (urls.size > 1) {
                        urls.forEach { u ->
                            viewModel.addDownload(u, "Unknown Title", false, customSettings)
                        }
                    } else {
                        viewModel.addDownload(formatDialogUrl!!.trim(), formatDialogTitle ?: "Unknown Title", false, customSettings)
                    }""",
    """                    if (urls.size > 1) {
                        urls.forEach { u ->
                            viewModel.addDownload(u, "Unknown Title", u.contains("list="), customSettings)
                        }
                    } else {
                        val urlStr = formatDialogUrl!!.trim()
                        viewModel.addDownload(urlStr, formatDialogTitle ?: "Unknown Title", urlStr.contains("list="), customSettings)
                    }"""
)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
