import urllib.request
import os
import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# So at line 695 it says: }         } finally {
# We need it to just be: } finally {
# WAIT, the previous fix missed the double close. Let's fix that.
text = text.replace("}         } finally {", "} finally {")
# and at 698 there is a missing closing bracket for the processDownload block itself? Let's check balance inside the catch block...

# I will just write a script that formats the file and explicitly counts where the extra '{' is coming from.
lines = text.split('\n')
for i, line in enumerate(lines):
    if "}         } finally {" in line:
        print(f"Found double bracket at {i+1}")

