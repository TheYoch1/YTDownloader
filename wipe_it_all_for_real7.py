import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Remove the two brackets we just added
if text.endswith("\n    }\n}\n"):
    text = text[:-9]
    print("Removed trailing brackets")

lines = text.split('\n')
for i, line in enumerate(lines):
    if "fun cancelDownload(id: String) {" in line:
        top_half = '\n'.join(lines[:i])
        bottom_half = '\n'.join(lines[i:])
        break

# Looking closely at top_half, we need to find EXACTLY where processDownload ends.
# I will just regex replace the finally block in processDownload
# processDownload ends with:
#        } finally {
#            stopForegroundServiceIfDone()
#        }

# I will count opening and closing brackets in processDownload specifically.
pd_start = top_half.find("    private suspend fun processDownload(id: String) {")
pd_text = top_half[pd_start:]

balance = 0
pd_end_idx = -1
for i, char in enumerate(pd_text):
    if char == '{':
        balance += 1
    elif char == '}':
        balance -= 1
        if balance == 0:
            pd_end_idx = i
            break

print("processDownload ends at relative index:", pd_end_idx)

if pd_end_idx != -1:
    top_half = top_half[:pd_start + pd_end_idx + 1]
    
with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(top_half + "\n" + bottom_half + "\n}\n")
