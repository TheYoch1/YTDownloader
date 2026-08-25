import re
with open("app/build.gradle.kts", "r") as f:
    content = f.read()

target = '''    packaging {
        resources {'''

rep = '''    packaging {
        jniLibs.useLegacyPackaging = true
        resources {'''

content = content.replace(target, rep)
with open("app/build.gradle.kts", "w") as f:
    f.write(content)
