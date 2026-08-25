import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = '''                    drawLine(
                        color = Color.White,
                        start = androidx.compose.ui.geometry.Offset(center, 0f),
                        end = androidx.compose.ui.geometry.Offset(center, size.height),
                        strokeWidth = 4.dp.toPx()
                    )
                }
            }'''

rep = '''                    drawLine(
                        color = Color.White,
                        start = androidx.compose.ui.geometry.Offset(center, 0f),
                        end = androidx.compose.ui.geometry.Offset(center, size.height),
                        strokeWidth = 4.dp.toPx()
                    )
                }
                androidx.compose.foundation.layout.Box(
                    modifier = Modifier
                        .align(Alignment.Center)
                        .fillMaxHeight()
                        .width(20.dp) // wide enough to be clickable
                        .androidx.compose.foundation.clickable(
                            interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                            indication = null,
                            onClick = {
                                val tealFraction = (AppAccentColors.indexOfFirst { it.first == "Teal" }.coerceAtLeast(0).toFloat() / AppAccentColors.size)
                                scrollOffset = tealFraction * cycleWidthPx
                                onConfigChanged(config.copy(accent = "Teal", colorOffset = tealFraction))
                            }
                        )
                )
            }'''
            
content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
