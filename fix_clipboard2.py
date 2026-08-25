with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """                                                    val clipboardManager = androidx.compose.ui.platform.ClipboardManager { } // wait, I already have clipboardManager defined at the top of the function
                                                    // let me just assume clipboardManager is available in MainScreen scope"""
rep = ""

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
