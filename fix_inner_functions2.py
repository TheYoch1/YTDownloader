import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# DownloaderViewModel compiles fine now!
# But wait, NO. "Unresolved reference clearFinishedDownloads" in MainActivity means clearFinishedDownloads is NOT accessible.
# It is still outside the class!
# Let's count brackets properly from top to bottom, finding where we go negative OR where the class closes.

balance = 0
lines = text.split('\n')
for i, line in enumerate(lines):
    balance += line.count('{') - line.count('}')
    print(f"{i+1:03d} | {balance:02d} | {line.strip()}")
    if balance == 0:
        print("CLASS CLOSED AT", i+1)
