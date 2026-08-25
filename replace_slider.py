import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target_ui = re.compile(r'Row\(modifier = Modifier\.fillMaxWidth\(\), horizontalArrangement = Arrangement\.SpaceBetween, verticalAlignment = Alignment\.CenterVertically\) \{[\s\S]*?\}\s*\}\s*Row\(\s*modifier = Modifier\.fillMaxWidth\(\),')

rep_ui = '''Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Accent Color", style = MaterialTheme.typography.labelMedium)
                val closestIndex = if (config.colorOffset >= 0f) {
                    (config.colorOffset * AppAccentColors.size).roundToInt() % AppAccentColors.size
                } else {
                    AppAccentColors.indexOfFirst { it.first == config.accent }.coerceAtLeast(0)
                }
                Text(AppAccentColors[closestIndex].first, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
            }
            androidx.compose.foundation.layout.BoxWithConstraints(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 8.dp, bottom = 24.dp)
                    .height(40.dp)
            ) {
                val cycleWidthPx = 1500f
                var scrollOffset by remember { 
                    mutableStateOf(
                        if (config.colorOffset >= 0f) config.colorOffset * cycleWidthPx
                        else (AppAccentColors.indexOfFirst { it.first == config.accent }.coerceAtLeast(0).toFloat() / AppAccentColors.size) * cycleWidthPx
                    )
                }

                androidx.compose.foundation.Canvas(
                    modifier = Modifier
                        .fillMaxSize()
                        .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                            androidx.compose.foundation.gestures.detectHorizontalDragGestures { change, dragAmount ->
                                change.consume()
                                scrollOffset = (scrollOffset - dragAmount + cycleWidthPx) % cycleWidthPx
                                
                                val offsetFraction = scrollOffset / cycleWidthPx
                                val floatIndex = offsetFraction * AppAccentColors.size
                                val index1 = floatIndex.toInt() % AppAccentColors.size
                                val index2 = (index1 + 1) % AppAccentColors.size
                                val fraction = floatIndex - floatIndex.toInt()
                                
                                val c1 = AppAccentColors[index1].second
                                val c2 = AppAccentColors[index2].second
                                val blended = androidx.compose.ui.graphics.lerp(c1, c2, fraction)
                                
                                val hex = String.format("#%08X", blended.androidx.compose.ui.graphics.toArgb())
                                
                                onConfigChanged(config.copy(accent = hex, colorOffset = offsetFraction))
                            }
                        }
                ) {
                    val colors = AppAccentColors.map { it.second } + AppAccentColors.first().second
                    val startX = (size.width / 2f) - scrollOffset
                    val endX = startX + cycleWidthPx
                    val brush = androidx.compose.ui.graphics.Brush.horizontalGradient(
                        colors = colors,
                        startX = startX,
                        endX = endX,
                        tileMode = androidx.compose.ui.graphics.TileMode.Repeated
                    )
                    drawRoundRect(
                        brush = brush,
                        cornerRadius = androidx.compose.ui.geometry.CornerRadius(20.dp.toPx())
                    )
                    
                    val center = size.width / 2f
                    drawLine(
                        color = Color.White,
                        start = androidx.compose.ui.geometry.Offset(center, 0f),
                        end = androidx.compose.ui.geometry.Offset(center, size.height),
                        strokeWidth = 4.dp.toPx()
                    )
                }
            }
            Row(
                modifier = Modifier.fillMaxWidth(),'''

content = target_ui.sub(rep_ui, content)

# Fix toArgb call just in case
content = content.replace('.androidx.compose.ui.graphics.toArgb()', '.toArgb()')

if 'import androidx.compose.ui.graphics.toArgb' not in content:
    content = content.replace('import androidx.compose.ui.graphics.Color', 'import androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.graphics.toArgb')

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
