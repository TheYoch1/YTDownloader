with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    main_text = f.read()

# Fix the specific lines 619 and 622
main_text = main_text.replace("viewModel.addDownload(u, null, customSettings)", "viewModel.addDownload(u, \"Unknown Title\", false, customSettings)")
main_text = main_text.replace("viewModel.addDownload(formatDialogUrl!!.trim(), formatDialogTitle, customSettings)", "viewModel.addDownload(formatDialogUrl!!.trim(), formatDialogTitle ?: \"Unknown Title\", false, customSettings)")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(main_text)
