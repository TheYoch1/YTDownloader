with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    main_text = f.read()

# Fix MainActivity.kt downloadSubtitles missing in MainActivity (it's in Models.kt but maybe the state variable was removed?)
main_text = main_text.replace("downloadSubtitles = settings.downloadSubtitles", "")

# Fix addDownload calls. The signature is: 
# fun addDownload(url: String, title: String, isPlaylist: Boolean, settings: DownloadSettings)
# Line 619: viewModel.addDownload(url, title, settings) -> It's missing isPlaylist=true/false
main_text = main_text.replace("viewModel.addDownload(url, title, settings)", "viewModel.addDownload(url, title ?: \"Unknown Title\", false, settings)")
main_text = main_text.replace("viewModel.addDownload(url, result.title, settings)", "viewModel.addDownload(url, result.title ?: \"Unknown Title\", true, settings)")
main_text = main_text.replace("viewModel.addDownload(result.webpageUrl, result.title, settings)", "viewModel.addDownload(result.webpageUrl ?: url, result.title ?: \"Unknown Title\", false, settings)")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(main_text)
