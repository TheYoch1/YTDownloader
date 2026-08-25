import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

# I will find the block starting at "// Quick Settings" up to "AnimatedVisibility(visible = searchResults.isNotEmpty() || searchError != null)"
# Wait, let's just find the exact block and replace it.

target_regex = r"// Quick Settings \(Format and Quality\).*?IconButton\(onClick = \{ showSettings = true \}\) \{.*?Icon\(Icons\.Default\.Settings, contentDescription = \"Settings\"\)[\s\}]+(?=AnimatedVisibility)"

match = re.search(target_regex, content, re.DOTALL)
if match:
    replacement = """                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                    horizontalArrangement = Arrangement.End
                ) {
                    IconButton(onClick = { showSettings = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                }
                
                """
    content = content.replace(match.group(0), replacement)
    print("Found and replaced A/V options!")
else:
    print("Not found A/V options block.")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
