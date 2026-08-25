with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    lines = f.readlines()

balance = 0
in_main = False
for i, line in enumerate(lines):
    if "fun MainScreen" in line:
        in_main = True
    
    if in_main:
        balance += line.count('{') - line.count('}')
        if balance == 0:
            print(f"MainScreen closed at line {i+1}: {line.strip()}")
            break
