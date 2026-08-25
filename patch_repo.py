with open("app/src/main/java/com/aistudio/ytdownloader/SettingsRepository.kt", "r") as f:
    content = f.read()

# Add maxConcurrentDownloads to PreferencesKeys
if "val MAX_CONCURRENT_DOWNLOADS" not in content:
    content = content.replace('val SAVE_DIRECTORY = stringPreferencesKey("save_directory")', 'val SAVE_DIRECTORY = stringPreferencesKey("save_directory")\n        val MAX_CONCURRENT_DOWNLOADS = intPreferencesKey("max_concurrent_downloads")')

# Update appConfigFlow map
target_map = """        .map { preferences ->
            val theme = preferences[PreferencesKeys.THEME] ?: "System"
            val saveDirectory = preferences[PreferencesKeys.SAVE_DIRECTORY] ?: "/storage/emulated/0/Download"
            AppConfig(theme = theme, saveDirectory = saveDirectory)
        }"""
replacement_map = """        .map { preferences ->
            val theme = preferences[PreferencesKeys.THEME] ?: "System"
            val saveDirectory = preferences[PreferencesKeys.SAVE_DIRECTORY] ?: "/storage/emulated/0/Movies/YT Downloader"
            val maxConcurrentDownloads = preferences[PreferencesKeys.MAX_CONCURRENT_DOWNLOADS] ?: 1
            AppConfig(theme = theme, saveDirectory = saveDirectory, maxConcurrentDownloads = maxConcurrentDownloads)
        }"""
content = content.replace(target_map, replacement_map)

# Update updateAppConfig
target_edit = """    suspend fun updateAppConfig(config: AppConfig) {
        context.dataStore.edit { preferences ->
            preferences[PreferencesKeys.THEME] = config.theme
            preferences[PreferencesKeys.SAVE_DIRECTORY] = config.saveDirectory
        }
    }"""
replacement_edit = """    suspend fun updateAppConfig(config: AppConfig) {
        context.dataStore.edit { preferences ->
            preferences[PreferencesKeys.THEME] = config.theme
            preferences[PreferencesKeys.SAVE_DIRECTORY] = config.saveDirectory
            preferences[PreferencesKeys.MAX_CONCURRENT_DOWNLOADS] = config.maxConcurrentDownloads
        }
    }"""
content = content.replace(target_edit, replacement_edit)

with open("app/src/main/java/com/aistudio/ytdownloader/SettingsRepository.kt", "w") as f:
    f.write(content)
