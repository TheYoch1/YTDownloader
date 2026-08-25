import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# Top App Bar
content = content.replace(
    'containerColor = MaterialTheme.colorScheme.primaryContainer,',
    'containerColor = MaterialTheme.colorScheme.primary,'
)
content = content.replace(
    'titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer',
    'titleContentColor = MaterialTheme.colorScheme.onPrimary'
)

# Download Cards
content = content.replace(
    'colors = CardDefaults.cardColors(\n            containerColor = MaterialTheme.colorScheme.surfaceVariant\n        )',
    'colors = CardDefaults.cardColors(\n            containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f)\n        )'
)
content = content.replace(
    'colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)',
    'colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f))'
)

# Update color scheme generation to generate proper primaryContainer based on primary
target_scheme = '''            val colorScheme = if (isDarkTheme) {
                darkColorScheme(
                    primary = baseColor,
                    secondary = baseColor,
                    tertiary = baseColor
                )
            } else {
                lightColorScheme(
                    primary = baseColor,
                    secondary = baseColor,
                    tertiary = baseColor
                )
            }'''
            
rep_scheme = '''            val colorScheme = if (isDarkTheme) {
                darkColorScheme(
                    primary = baseColor,
                    onPrimary = Color.White,
                    primaryContainer = baseColor.copy(alpha = 0.3f),
                    onPrimaryContainer = Color.White,
                    secondary = baseColor,
                    tertiary = baseColor
                )
            } else {
                lightColorScheme(
                    primary = baseColor,
                    onPrimary = Color.White,
                    primaryContainer = baseColor.copy(alpha = 0.2f),
                    onPrimaryContainer = Color.Black,
                    secondary = baseColor,
                    tertiary = baseColor
                )
            }'''
            
content = content.replace(target_scheme, rep_scheme)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
