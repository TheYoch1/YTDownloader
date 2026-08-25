with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    lines = f.readlines()

new_lines = lines[:293] + lines[349:]

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.writelines(new_lines)
