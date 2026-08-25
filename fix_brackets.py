with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = "        }\n    }\n}\n        }\n    }\n}\n\n@Composable\nfun DownloadItemCard("
replacement = "        }\n    }\n}\n\n@Composable\nfun DownloadItemCard("

if target in content:
    content = content.replace(target, replacement)
else:
    # Just replace all `} } } } } }` with the right amount
    import re
    content = re.sub(r"\}\s*\}\s*\}\s*\}\s*\}\s*\}\s*@Composable\nfun DownloadItemCard", "}\n}\n}\n}\n@Composable\nfun DownloadItemCard", content)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
