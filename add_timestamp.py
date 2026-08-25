with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "r") as f:
    text = f.read()

text = text.replace("var currentItemProgress: Float = 0f", "var currentItemProgress: Float = 0f,\n    val timestamp: Long = System.currentTimeMillis()")

with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "w") as f:
    f.write(text)
