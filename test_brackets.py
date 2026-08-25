with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

stack = 0
for i, char in enumerate(content):
    if char == '{': stack += 1
    elif char == '}': stack -= 1
    
print(f"Stack end: {stack}")
