import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

text = re.sub(
    r'// Name format\n\s*val cleanTitle = item\.title\.replace\(Regex\("\[\^a-zA-Z0-9\.\\\\- \]"([^)]*)\n\s*request\.addOption\("-o", item\.settings\.filenamePattern\.replace\("\\$title", cleanTitle\) \+ "\.%\(ext\)s"\)',
    '// Name format\n            request.addOption("-o", "%(title)s.%(ext)s")',
    text,
    flags=re.MULTILINE
)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
