with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()
content = content.replace('"Dashboard & History",', '"App Settings",')
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
