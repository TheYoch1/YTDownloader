import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    lines = f.readlines()

def check_balance(lines):
    balance = 0
    for i, line in enumerate(lines):
        balance += line.count('{') - line.count('}')
        if balance == 0 and i > 100:
            print(f"Balance reached zero at line {i+1}: {line.strip()}")
            return i

check_balance(lines)
