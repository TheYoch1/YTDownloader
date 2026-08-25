import re

with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "r") as f:
    content = f.read()

target = '''data class AppConfig(
    var theme: String = "Dark",
    var accent: String = "Teal",
    var saveDirectory: String = "Default",
    var maxConcurrentDownloads: Int = 1,
    var colorOffset: Float = -1f,
    var confirmExit: Boolean = true
)'''

rep = '''data class AppConfig(
    var theme: String = "Dark",
    var accent: String = "Teal",
    var saveDirectory: String = "Default",
    var maxConcurrentDownloads: Int = 1,
    var colorOffset: Float = -1f,
    var confirmExit: Boolean = true,
    var wifiOnly: Boolean = false,
    var notifyOnComplete: Boolean = true
)'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "w") as f:
    f.write(content)
