with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    lines = f.readlines()

balance = 0
for i, line in enumerate(lines):
    balance += line.count('{') - line.count('}')
    print(f"{i+1:3d}: {balance:2d} | {line.strip()}")
    if balance < 0:
        print(f"ERROR: Balance went negative at line {i+1}")
        break
