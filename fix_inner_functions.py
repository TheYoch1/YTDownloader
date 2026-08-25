import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# I see it now... e: file:///app/applet/app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt:762:5 Modifier 'private' is not applicable to 'local function'.
# The brackets are mismatched EARLIER in the file! Likely inside `processDownload`.
# I will find where processDownload ends by counting brackets inside of it.

lines = text.split('\n')
for i, line in enumerate(lines):
    if "private suspend fun processDownload(" in line:
        start_idx = i
        break

balance = 0
for i in range(start_idx, len(lines)):
    balance += lines[i].count('{') - lines[i].count('}')
    if balance == 0:
        end_idx = i
        break

print(f"processDownload spans {start_idx} to {end_idx}")
