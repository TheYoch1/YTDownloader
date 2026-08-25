import urllib.request
import os
import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

lines = text.split('\n')
new_lines = []

balance = 0
for i, line in enumerate(lines):
    if "fun cancelDownload(id: String) {" in line:
        if balance <= 0:
            # We are outside the class. We need to inject an opening bracket to pull these methods back into the class!
            # Or better yet, we just delete the extra closing brackets before this line
            print("Found it outside class. Removing prior closing brackets to pull it back in.")
            
            # Walk backwards and delete closing brackets until balance is 1
            for j in range(len(new_lines) - 1, -1, -1):
                if balance == 1:
                    break
                if "}" in new_lines[j]:
                    new_lines[j] = new_lines[j].replace("}", "", 1)
                    balance += 1
                    
    balance += line.count('{') - line.count('}')
    new_lines.append(line)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write('\n'.join(new_lines))
