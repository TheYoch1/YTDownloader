# Look at these errors. It's not just the bottom of the file now. The whole viewmodel broke because processDownload brackets are totally busted!
# Let's count brackets properly from top to bottom, finding where we go negative OR where the class closes.
import urllib.request

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Easiest way: The file is small. Let me fetch the unpatched original from git... wait there is no git.
# I will download a fresh working version if I can't fix it. But I CAN fix it.

balance = 0
class_end_line = -1

lines = text.split('\n')
for i, line in enumerate(lines):
    balance += line.count('{') - line.count('}')
    if balance == 0 and "class DownloaderViewModel" in text[:sum(len(l)+1 for l in lines[:i+1])]:
        class_end_line = i
        break

print(f"Class ends at line: {class_end_line+1}")
