with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# Make sure to import SelectionContainer
if "import androidx.compose.foundation.text.selection.SelectionContainer" not in content:
    content = content.replace("import androidx.compose.foundation.text.KeyboardOptions", "import androidx.compose.foundation.text.KeyboardOptions\nimport androidx.compose.foundation.text.selection.SelectionContainer")

target = """                LazyColumn {
                    item {
                        Text(
                            text = logText, 
                            style = MaterialTheme.typography.bodySmall,
                            modifier = Modifier.pointerInput(Unit) {
                                detectTapGestures(
                                    onLongPress = {
                                        clipboardManager.setText(AnnotatedString(logText))
                                        android.widget.Toast.makeText(context, "Log copied to clipboard", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                )
                            }
                        )
                    }
                }"""

replacement = """                SelectionContainer {
                    LazyColumn {
                        val lines = logText.split("\\n").filter { it.isNotBlank() }
                        if (lines.isEmpty()) {
                            item { Text("No errors recorded.") }
                        } else {
                            items(lines) { line ->
                                Text(
                                    text = line, 
                                    style = MaterialTheme.typography.bodySmall,
                                    modifier = Modifier.padding(bottom = 8.dp).fillMaxWidth().clickable {
                                        clipboardManager.setText(AnnotatedString(line))
                                        android.widget.Toast.makeText(context, "Copied error line", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                )
                            }
                        }
                    }
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
