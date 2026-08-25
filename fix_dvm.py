with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

text = text.replace(
    "    private val _appConfig = MutableStateFlow(AppConfig())",
    "    private val _currentSettings = MutableStateFlow(DownloadSettings())\n    val currentSettings: StateFlow<DownloadSettings> = _currentSettings.asStateFlow()\n\n    private val _appConfig = MutableStateFlow(AppConfig())"
)

text = text.replace(
    "    fun updateCurrentSettings(settings: DownloadSettings) {\n    }",
    "    fun updateCurrentSettings(settings: DownloadSettings) {\n        _currentSettings.value = settings\n    }"
)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(text)
