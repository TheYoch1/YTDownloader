# The viewmodel is hopelessly broken due to dangling brackets inside functions we didn't touch
# I will download a fresh version, or rewrite the end cleanly by ignoring the unclosed bracket
import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Let's count where the bracket imbalance started
lines = text.split('\n')
balance = 0
for i, line in enumerate(lines):
    balance += line.count('{') - line.count('}')
    if balance < 0:
        print(f"Negative balance at line {i+1}: {line}")
        
