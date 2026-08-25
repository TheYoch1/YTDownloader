with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target1 = '''            val baseColor = when (config.accent) {
                "Red" -> Color(0xFFE53935)
                "Green" -> Color(0xFF43A047)
                "Purple" -> Color(0xFF8E24AA)
                "Orange" -> Color(0xFFF4511E)
                else -> Color(0xFF1E88E5) // Blue
            }'''
rep1 = '''            val baseColor = when (config.accent) {
                "Red" -> Color(0xFFE53935)
                "Green" -> Color(0xFF43A047)
                "Purple" -> Color(0xFF8E24AA)
                "Orange" -> Color(0xFFF4511E)
                "Pink" -> Color(0xFFD81B60)
                "Teal" -> Color(0xFF00897B)
                "Amber" -> Color(0xFFFFB300)
                "Cyan" -> Color(0xFF00ACC1)
                "DeepOrange" -> Color(0xFFF4511E)
                "Indigo" -> Color(0xFF3949AB)
                "Lime" -> Color(0xFFC0CA33)
                else -> Color(0xFF1E88E5) // Blue
            }'''
content = content.replace(target1, rep1)

target2 = '''            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                listOf(
                    "Blue" to Color(0xFF1E88E5), 
                    "Red" to Color(0xFFE53935), 
                    "Green" to Color(0xFF43A047), 
                    "Purple" to Color(0xFF8E24AA), 
                    "Orange" to Color(0xFFF4511E)
                ).forEach { (colorName, colorValue) ->
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .background(colorValue, androidx.compose.foundation.shape.CircleShape)
                            .border(if (isSelected) 3.dp else 0.dp, if (isSelected) MaterialTheme.colorScheme.onSurface else Color.Transparent, androidx.compose.foundation.shape.CircleShape)
                            .clickable { onConfigChanged(config.copy(accent = colorName)) }
                    )
                }
            }'''
rep2 = '''            androidx.compose.foundation.lazy.LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                items(listOf(
                    "Blue" to Color(0xFF1E88E5), 
                    "Red" to Color(0xFFE53935), 
                    "Green" to Color(0xFF43A047), 
                    "Purple" to Color(0xFF8E24AA), 
                    "Orange" to Color(0xFFF4511E),
                    "Pink" to Color(0xFFD81B60),
                    "Teal" to Color(0xFF00897B),
                    "Amber" to Color(0xFFFFB300),
                    "Cyan" to Color(0xFF00ACC1),
                    "DeepOrange" to Color(0xFFF4511E),
                    "Indigo" to Color(0xFF3949AB),
                    "Lime" to Color(0xFFC0CA33)
                )) { (colorName, colorValue) ->
                    val isSelected = config.accent == colorName
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .background(colorValue, androidx.compose.foundation.shape.CircleShape)
                            .border(if (isSelected) 3.dp else 0.dp, if (isSelected) MaterialTheme.colorScheme.onSurface else Color.Transparent, androidx.compose.foundation.shape.CircleShape)
                            .clickable { onConfigChanged(config.copy(accent = colorName)) }
                    )
                }
            }'''
content = content.replace(target2, rep2)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
