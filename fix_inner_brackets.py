with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """                    }
            Spacer(modifier = Modifier.height(16.dp))
            
            val activeDownloads"""

replacement = """                    }
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            
            val activeDownloads"""

content = content.replace(target, replacement)

# Now check the total brackets again
opened = content.count('{')
closed = content.count('}')
print(f"Total opened: {opened}, closed: {closed}")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
