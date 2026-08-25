with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "r") as f:
    text = f.read()

replacement = """    var currentItemIndex: Int = 0,
    var totalItems: Int = 0,
    var currentItemTitle: String = "",
    var currentItemProgress: Float = 0f
)"""
text = text.replace("""    var currentItemIndex: Int = 0,
    var totalItems: Int = 0,
    var currentItemTitle: String = ""
)""", replacement)

with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "w") as f:
    f.write(text)
