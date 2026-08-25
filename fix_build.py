import re
with open("app/build.gradle.kts", "r") as f:
    content = f.read()

if "packaging" not in content:
    content = content.replace("android {", "android {\n    packaging {\n        jniLibs.useLegacyPackaging = true\n    }")

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
