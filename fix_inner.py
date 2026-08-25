with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    lines = f.readlines()

new_lines = []
bracket_stack = []
for i, line in enumerate(lines):
    if "fun " in line and "{" in line:
        pass
    new_lines.append(line)
        
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.writelines(lines)
