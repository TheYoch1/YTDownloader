with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

old_code = """            } else {
                downloadSubtitles = false
                if (qualities.isNotEmpty()) {
                    selectedFormatId = qualities.firstOrNull()?.formatId
                }
            }"""

new_code = """            } else {
                downloadSubtitles = false
                if (qualities.isNotEmpty()) {
                    val defaultVideoFormat = qualities.find { it.height == 720 && !it.isAudioOnly }
                        ?: qualities.firstOrNull { !it.isAudioOnly }
                        ?: qualities.firstOrNull()
                    selectedFormatId = defaultVideoFormat?.formatId
                }
            }"""

text = text.replace(old_code, new_code)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
