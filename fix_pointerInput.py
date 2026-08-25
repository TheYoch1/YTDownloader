import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace('.androidx.compose.ui.input.pointer.pointerInput(Unit)', '.pointerInput(Unit)')

if 'import androidx.compose.ui.input.pointer.pointerInput' not in content:
    content = content.replace('import androidx.compose.ui.graphics.Color', 'import androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.input.pointer.pointerInput')

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
