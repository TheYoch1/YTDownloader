with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()
    
# Check for 'selectedQuality' which might still be referenced
if "selectedQuality" in text:
    print("Found selectedQuality in MainActivity!")
    text = text.replace("selectedQuality =", "selectedFormatId =")
    
    with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
        f.write(text)
