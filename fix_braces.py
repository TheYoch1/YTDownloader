import re
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """    if (isStorageFull && !dismissedStorageDialog) {"""
rep = """        }
    }
    
    if (isStorageFull && !dismissedStorageDialog) {"""
content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
