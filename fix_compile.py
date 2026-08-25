import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
    "import androidx.compose.ui.Modifier",
    "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.draw.clip"
)

content = content.replace(
    "    onViewErrorLog: () -> Unit = {}",
    "    onViewErrorLog: () -> Unit = {},\n    onViewHistoryLog: () -> Unit = {}"
)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
