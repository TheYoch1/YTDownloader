import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# Fix imports
if 'import androidx.compose.foundation.gestures.detectHorizontalDragGestures' not in content:
    content = content.replace('import androidx.compose.ui.graphics.Color', 'import androidx.compose.ui.graphics.Color\nimport androidx.compose.foundation.gestures.detectHorizontalDragGestures')

content = content.replace(
    '.androidx.compose.ui.input.pointer.pointerInput(Unit) {',
    '.androidx.compose.ui.input.pointer.pointerInput(Unit) {'
)

content = content.replace(
    'androidx.compose.foundation.gestures.detectHorizontalDragGestures { change, dragAmount ->',
    'detectHorizontalDragGestures { change, dragAmount: Float ->'
)

# In compose 1.5.0+, change.consume() is available.
# But let's just make sure.

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
