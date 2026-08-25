with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

if "isUrl" in content:
    print("Has isUrl")
