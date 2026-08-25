with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    lines = f.readlines()

balance = 0
for i, line in enumerate(lines):
    balance += line.count('{') - line.count('}')
    print(f"{i+1:03d} | {balance:02d} | {line.strip()}")
