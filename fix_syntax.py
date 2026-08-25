with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

opened = content.count('{')
closed = content.count('}')

print(f"Total opened: {opened}, closed: {closed}")
