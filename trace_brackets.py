with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

stack = []
for i, char in enumerate(content):
    if char == '{': stack.append(i)
    elif char == '}': 
        if stack: stack.pop()
        else: print(f"Extra closing bracket at {i}")

print("Unclosed opening brackets at indices:")
for i in stack:
    line_no = content[:i].count('\\n') + 1
    print(f"Line {line_no}: {content[i-30:i+30]}")
