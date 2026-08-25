import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# Define the global color list right before MainActivity
colors_list = '''
val AppAccentColors = listOf(
    "Red" to Color(0xFFF44336), "Red Dark" to Color(0xFFD32F2F), "Red Light" to Color(0xFFE57373),
    "Pink" to Color(0xFFE91E63), "Pink Dark" to Color(0xFFC2185B), "Pink Light" to Color(0xFFF06292),
    "Purple" to Color(0xFF9C27B0), "Purple Dark" to Color(0xFF7B1FA2), "Purple Light" to Color(0xFFBA68C8),
    "Deep Purple" to Color(0xFF673AB7), "Deep Purple Dark" to Color(0xFF512DA8),
    "Indigo" to Color(0xFF3F51B5), "Indigo Dark" to Color(0xFF303F9F),
    "Blue" to Color(0xFF2196F3), "Blue Dark" to Color(0xFF1976D2), "Blue Light" to Color(0xFF64B5F6),
    "Light Blue" to Color(0xFF03A9F4), "Light Blue Dark" to Color(0xFF0288D1),
    "Cyan" to Color(0xFF00BCD4), "Cyan Dark" to Color(0xFF0097A7),
    "Teal" to Color(0xFF009688), "Teal Dark" to Color(0xFF00796B),
    "Green" to Color(0xFF4CAF50), "Green Dark" to Color(0xFF388E3C), "Green Light" to Color(0xFF81C784),
    "Amber" to Color(0xFFFFC107), "Amber Dark" to Color(0xFFFFA000),
    "Orange" to Color(0xFFFF9800), "Orange Dark" to Color(0xFFF57C00),
    "Deep Orange" to Color(0xFFFF5722)
)

class MainActivity : ComponentActivity() {'''
content = content.replace('class MainActivity : ComponentActivity() {', colors_list)

# Replace baseColor mapping
target_base_color = re.compile(r'val baseColor = when \(config\.accent\) \{[\s\S]*?else -> Color\(0xFF1E88E5\) // Blue\n\s*\}')
rep_base_color = '''val baseColor = AppAccentColors.find { it.first == config.accent }?.second ?: Color(0xFF2196F3)'''
content = target_base_color.sub(rep_base_color, content)

# Replace the color picker row
target_row = re.compile(r'Text\("Accent Color", style = MaterialTheme.typography.labelMedium\)\s*Row\(modifier = Modifier\.fillMaxWidth\(\)\.padding\(top = 4\.dp, bottom = 16\.dp\), horizontalArrangement = Arrangement\.spacedBy\(12\.dp\)\) \{[\s\S]*?\}\s*\}\s*Row\(\s*modifier = Modifier\.fillMaxWidth\(\),')

rep_row = '''Text("Accent Color", style = MaterialTheme.typography.labelMedium)
            androidx.compose.foundation.lazy.LazyRow(
                modifier = Modifier.fillMaxWidth().padding(top = 8.dp, bottom = 24.dp), 
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(AppAccentColors) { (colorName, colorValue) ->
                    val isSelected = config.accent == colorName
                    androidx.compose.foundation.layout.Box(
                        modifier = Modifier
                            .size(42.dp)
                            .background(colorValue, androidx.compose.foundation.shape.CircleShape)
                            .border(if (isSelected) 3.dp else 0.dp, if (isSelected) MaterialTheme.colorScheme.onSurface else Color.Transparent, androidx.compose.foundation.shape.CircleShape)
                            .clickable { onConfigChanged(config.copy(accent = colorName)) }
                    )
                }
            }
            Row(
                modifier = Modifier.fillMaxWidth(),'''

content = target_row.sub(rep_row, content)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
