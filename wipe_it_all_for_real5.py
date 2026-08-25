import urllib.request
import os
import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# I see it now. Local function means it's STILL inside processDownload!
# We just need to add one more bracket right before cancelDownload to close the outer class properly? No, to close processDownload.

lines = text.split('\n')
for i, line in enumerate(lines):
    if "fun cancelDownload(id: String) {" in line:
        lines.insert(i, "    }")
        break

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write('\n'.join(lines))
