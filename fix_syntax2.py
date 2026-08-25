with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("androidx.compose.foundation.shape.CircleShape", "androidx.compose.foundation.shape.CircleShape")

# We just need to make sure `.background` is properly imported.
if "import androidx.compose.foundation.background" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.background\nimport androidx.compose.foundation.border\nimport androidx.compose.foundation.shape.CircleShape")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
