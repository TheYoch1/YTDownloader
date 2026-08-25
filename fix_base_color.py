import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = '''            val baseColor = AppAccentColors.find { it.first == config.accent }?.second ?: Color(0xFF2196F3)'''

rep = '''            val baseColor = if (config.accent.startsWith("#")) {
                Color(android.graphics.Color.parseColor(config.accent))
            } else {
                AppAccentColors.find { it.first == config.accent }?.second ?: Color(0xFF009688)
            }'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
