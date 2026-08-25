import re
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

content = re.sub(r"\}\n\}\n\}\n@Composable\nfun DownloadItemCard", "}\n}\n@Composable\nfun DownloadItemCard", content)

opened = content.count('{')
closed = content.count('}')
print(f"Total opened: {opened}, closed: {closed}")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
