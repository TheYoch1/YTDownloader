package com.aistudio.ytdownloader

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import java.io.IOException

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")

class SettingsRepository(private val context: Context) {
    private object PreferencesKeys {
        val AUDIO_ONLY = booleanPreferencesKey("audio_only")
        val QUALITY = stringPreferencesKey("quality")
        val TAG_AUDIO_FILE = booleanPreferencesKey("tag_audio_file")
        val FILENAME_PATTERN = stringPreferencesKey("filename_pattern")
        val THEME = stringPreferencesKey("theme")
        val ACCENT = stringPreferencesKey("accent")
        val COLOR_OFFSET = floatPreferencesKey("color_offset")
        val SAVE_DIRECTORY = stringPreferencesKey("save_directory")
        val MAX_CONCURRENT_DOWNLOADS = intPreferencesKey("max_concurrent_downloads")
        val SUBTITLES = booleanPreferencesKey("subtitles")
    }

    val appConfigFlow: Flow<AppConfig> = context.dataStore.data
        .catch { exception ->
            if (exception is IOException) {
                emit(emptyPreferences())
            } else {
                throw exception
            }
        }
        .map { preferences ->
            val theme = preferences[PreferencesKeys.THEME] ?: "System"
            val accent = preferences[PreferencesKeys.ACCENT] ?: "Teal"
            val saveDirectory = preferences[PreferencesKeys.SAVE_DIRECTORY] ?: "Default"
            val maxConcurrentDownloads = preferences[PreferencesKeys.MAX_CONCURRENT_DOWNLOADS] ?: 1
            val colorOffset = preferences[PreferencesKeys.COLOR_OFFSET] ?: -1f
            AppConfig(theme = theme, accent = accent, saveDirectory = saveDirectory, maxConcurrentDownloads = maxConcurrentDownloads, colorOffset = colorOffset)
        }

    val downloadSettingsFlow: Flow<DownloadSettings> = context.dataStore.data
        .catch { exception ->
            if (exception is IOException) {
                emit(emptyPreferences())
            } else {
                throw exception
            }
        }
        .map { preferences ->
            val audioOnly = preferences[PreferencesKeys.AUDIO_ONLY] ?: true
            val qualityString = preferences[PreferencesKeys.QUALITY] ?: VideoQuality.High720.name
            val quality = try { VideoQuality.valueOf(qualityString) } catch (e: Exception) { VideoQuality.High720 }
            val tagAudioFile = preferences[PreferencesKeys.TAG_AUDIO_FILE] ?: true
            val filenamePattern = preferences[PreferencesKeys.FILENAME_PATTERN] ?: "\$title"
            val subtitles = preferences[PreferencesKeys.SUBTITLES] ?: false

            DownloadSettings(
                audioOnly = audioOnly,
                quality = quality,
                tagAudioFile = tagAudioFile,
                filenamePattern = filenamePattern,
                downloadSubtitles = subtitles
            )
        }

    suspend fun updateAppConfig(config: AppConfig) {
        context.dataStore.edit { preferences ->
            preferences[PreferencesKeys.THEME] = config.theme
            preferences[PreferencesKeys.ACCENT] = config.accent
            preferences[PreferencesKeys.SAVE_DIRECTORY] = config.saveDirectory
            preferences[PreferencesKeys.MAX_CONCURRENT_DOWNLOADS] = config.maxConcurrentDownloads
            preferences[PreferencesKeys.COLOR_OFFSET] = config.colorOffset
        }
    }

    suspend fun updateDownloadSettings(settings: DownloadSettings) {
        context.dataStore.edit { preferences ->
            preferences[PreferencesKeys.AUDIO_ONLY] = settings.audioOnly
            preferences[PreferencesKeys.QUALITY] = settings.quality.name
            preferences[PreferencesKeys.TAG_AUDIO_FILE] = settings.tagAudioFile
            preferences[PreferencesKeys.FILENAME_PATTERN] = settings.filenamePattern
            preferences[PreferencesKeys.SUBTITLES] = settings.downloadSubtitles
        }
    }
}
