import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace('.androidx.compose.foundation.clickable(', '.clickable(')

if 'import androidx.compose.foundation.clickable' not in content:
    content = content.replace('import androidx.compose.foundation.gestures.detectHorizontalDragGestures', 'import androidx.compose.foundation.gestures.detectHorizontalDragGestures\nimport androidx.compose.foundation.clickable')

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
