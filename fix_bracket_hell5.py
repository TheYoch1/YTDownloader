with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

balance = 0
started = False
lines = text.split('\n')

for i, line in enumerate(lines):
    if "class DownloaderViewModel" in line:
        started = True
    if started:
        balance += line.count('{') - line.count('}')
        if balance == 0:
            print(f"Class ended prematurely at line {i+1}: {line}")
            break
