import re

with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "r") as f:
    content = f.read()

content = content.replace(
    'var maxConcurrentDownloads: Int = 1,',
    'var maxConcurrentDownloads: Int = 1,\n    var colorOffset: Float = -1f,'
)

with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/aistudio/ytdownloader/SettingsRepository.kt", "r") as f:
    content = f.read()

content = content.replace(
    'val ACCENT = stringPreferencesKey("accent")',
    'val ACCENT = stringPreferencesKey("accent")\n        val COLOR_OFFSET = floatPreferencesKey("color_offset")'
)

content = content.replace(
    'val maxConcurrentDownloads = preferences[PreferencesKeys.MAX_CONCURRENT_DOWNLOADS] ?: 1',
    'val maxConcurrentDownloads = preferences[PreferencesKeys.MAX_CONCURRENT_DOWNLOADS] ?: 1\n            val colorOffset = preferences[PreferencesKeys.COLOR_OFFSET] ?: -1f'
)

content = content.replace(
    'AppConfig(theme = theme, accent = accent, saveDirectory = saveDirectory, maxConcurrentDownloads = maxConcurrentDownloads)',
    'AppConfig(theme = theme, accent = accent, saveDirectory = saveDirectory, maxConcurrentDownloads = maxConcurrentDownloads, colorOffset = colorOffset)'
)

content = content.replace(
    'preferences[PreferencesKeys.MAX_CONCURRENT_DOWNLOADS] = config.maxConcurrentDownloads',
    'preferences[PreferencesKeys.MAX_CONCURRENT_DOWNLOADS] = config.maxConcurrentDownloads\n            preferences[PreferencesKeys.COLOR_OFFSET] = config.colorOffset'
)

with open("app/src/main/java/com/aistudio/ytdownloader/SettingsRepository.kt", "w") as f:
    f.write(content)
