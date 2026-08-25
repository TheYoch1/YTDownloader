import re

# Models.kt
with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "r") as f:
    content = f.read()

content = content.replace(
    'var quality: VideoQuality = VideoQuality.High1080', 
    'var quality: VideoQuality = VideoQuality.High720'
)

with open("app/src/main/java/com/aistudio/ytdownloader/Models.kt", "w") as f:
    f.write(content)

# SettingsRepository.kt
with open("app/src/main/java/com/aistudio/ytdownloader/SettingsRepository.kt", "r") as f:
    content = f.read()

content = content.replace(
    'val qualityString = preferences[PreferencesKeys.QUALITY] ?: VideoQuality.High1080.name',
    'val qualityString = preferences[PreferencesKeys.QUALITY] ?: VideoQuality.High720.name'
)
content = content.replace(
    'val quality = try { VideoQuality.valueOf(qualityString) } catch (e: Exception) { VideoQuality.High1080 }',
    'val quality = try { VideoQuality.valueOf(qualityString) } catch (e: Exception) { VideoQuality.High720 }'
)

with open("app/src/main/java/com/aistudio/ytdownloader/SettingsRepository.kt", "w") as f:
    f.write(content)

# MainActivity.kt
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
    'selectedQuality = qualities.lastOrNull() ?: VideoQuality.High1080',
    'selectedQuality = qualities.lastOrNull() ?: VideoQuality.High720'
)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
