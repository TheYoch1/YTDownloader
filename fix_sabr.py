import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

# Replace height with res
content = content.replace("[height<=", "[res<=")
content = content.replace("[height>=", "[res>=")

# Remove extractor-args lines
content = re.sub(r'\s*req(?:uest)?\.addOption\("--extractor-args", "youtube:player_client=android,web"\)', '', content)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)

print("Fixed")
