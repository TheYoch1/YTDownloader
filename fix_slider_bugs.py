import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# Fix Int * Dp
content = content.replace('(initialIndex * itemWidthDp)', '(itemWidthDp * initialIndex)')

# Fix kotlin.math.roundToInt()
content = content.replace('.kotlin.math.roundToInt()', '.roundToInt()')
if 'import kotlin.math.roundToInt' not in content:
    content = content.replace('import kotlinx.coroutines.launch', 'import kotlinx.coroutines.launch\nimport kotlin.math.roundToInt\nimport androidx.compose.foundation.horizontalScroll')

# Fix extension function
content = content.replace('.androidx.compose.foundation.horizontalScroll', '.horizontalScroll')

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
