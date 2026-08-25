with open("app/src/main/java/com/aistudio/ytdownloader/SettingsRepository.kt", "r") as f:
    content = f.read()

content = content.replace('val THEME = stringPreferencesKey("theme")',
'''val THEME = stringPreferencesKey("theme")
        val ACCENT = stringPreferencesKey("accent")''')

content = content.replace('val theme = preferences[PreferencesKeys.THEME] ?: "System"',
'''val theme = preferences[PreferencesKeys.THEME] ?: "System"
            val accent = preferences[PreferencesKeys.ACCENT] ?: "Blue"''')

content = content.replace('AppConfig(theme = theme, saveDirectory = saveDirectory, maxConcurrentDownloads = maxConcurrentDownloads)',
'AppConfig(theme = theme, accent = accent, saveDirectory = saveDirectory, maxConcurrentDownloads = maxConcurrentDownloads)')

content = content.replace('preferences[PreferencesKeys.THEME] = config.theme',
'''preferences[PreferencesKeys.THEME] = config.theme
            preferences[PreferencesKeys.ACCENT] = config.accent''')

with open("app/src/main/java/com/aistudio/ytdownloader/SettingsRepository.kt", "w") as f:
    f.write(content)
