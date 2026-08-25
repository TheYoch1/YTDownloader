package com.aistudio.ytdownloader

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Warning
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.ffmpeg.FFmpeg
import kotlinx.coroutines.delay

sealed class SplashState {
    object Loading : SplashState()
    data class UpdateAvailable(val info: UpdateInfo) : SplashState()
    data class SafeMode(val message: String) : SplashState()
    data class InitError(val message: String) : SplashState()
}

class SplashActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        val prefs = getSharedPreferences("app_prefs", MODE_PRIVATE)
        val hasCrashedBefore = prefs.getBoolean("crashed_last_time", false)
        if (hasCrashedBefore) {
            prefs.edit().putBoolean("crashed_last_time", false).apply() // Reset flag
        }
            
        setContent {
            var uiState by remember { mutableStateOf<SplashState>(SplashState.Loading) }
            
            LaunchedEffect(Unit) {
                // 1. Check for updates first in strict isolation (No FFmpeg/Chaquopy loads)
                val updateInfo = AppUpdater.checkForUpdates(this@SplashActivity)
                
                // Replace with actual current version check (e.g. BuildConfig.VERSION_CODE)
                val currentVersion = 1 
                
                if (updateInfo != null && updateInfo.latest_version > currentVersion) {
                    uiState = SplashState.UpdateAvailable(updateInfo)
                    if (updateInfo.mandatory) {
                        return@LaunchedEffect // Block all further initialization!
                    }
                    // If not mandatory, wait a moment for the user to see, but we allow dismissal via dialog
                }
                
                if (hasCrashedBefore) {
                    uiState = SplashState.SafeMode("The app recovered from a fatal crash. Safe Mode Active.")
                    // If we want to strictly halt on a crash loop until update:
                    return@LaunchedEffect
                }
                
                // 2. Initialize heavy components safely inside extreme try-catch
                try {
                    YoutubeDL.getInstance().init(applicationContext)
                    FFmpeg.getInstance().init(applicationContext)
                    
                    // Proceed to MainActivity
                    startActivity(Intent(this@SplashActivity, MainActivity::class.java))
                    finish()
                } catch (e: Exception) {
                    uiState = SplashState.InitError(e.message ?: "Failed to initialize video engine")
                }
            }
            
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    Box(contentAlignment = Alignment.Center) {
                        when (val state = uiState) {
                            is SplashState.Loading -> CircularProgressIndicator()
                            is SplashState.UpdateAvailable -> {
                                UpdateDialog(
                                    updateInfo = state.info,
                                    onDismiss = {
                                        // If not mandatory, allow continuing
                                        try {
                                            YoutubeDL.getInstance().init(applicationContext)
                                            FFmpeg.getInstance().init(applicationContext)
                                            startActivity(Intent(this@SplashActivity, MainActivity::class.java))
                                            finish()
                                        } catch (e: Exception) {
                                            uiState = SplashState.InitError(e.message ?: "Init failed")
                                        }
                                    }
                                )
                            }
                            is SplashState.SafeMode -> ErrorScreen("Safe Mode: ${state.message}\nPlease update the app.")
                            is SplashState.InitError -> ErrorScreen("Initialization Error: ${state.message}\nNetwork or binary corrupted.")
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun UpdateDialog(updateInfo: UpdateInfo, onDismiss: () -> Unit) {
    val context = androidx.compose.ui.platform.LocalContext.current
    AlertDialog(
        onDismissRequest = { 
            if (!updateInfo.mandatory) onDismiss() 
        },
        title = { Text("Update Required") },
        text = { 
            val msg = if (updateInfo.mandatory) "A critical update is required to continue using the app." else "A new version of the app is available."
            Text(msg) 
        },
        confirmButton = {
            Button(onClick = { 
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(updateInfo.url))
                context.startActivity(intent)
            }) {
                Text("Update Now")
            }
        },
        dismissButton = if (!updateInfo.mandatory) {
            {
                TextButton(onClick = onDismiss) {
                    Text("Later")
                }
            }
        } else null,
        // CRITICAL: Make dialog un-cancelable if mandatory is true
        properties = androidx.compose.ui.window.DialogProperties(
            dismissOnBackPress = !updateInfo.mandatory,
            dismissOnClickOutside = !updateInfo.mandatory
        )
    )
}

@Composable
fun ErrorScreen(message: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(32.dp)) {
        Icon(
            imageVector = androidx.compose.material.icons.Icons.Default.Warning, 
            contentDescription = "Error", 
            tint = MaterialTheme.colorScheme.error,
            modifier = Modifier.size(64.dp)
        )
        Spacer(Modifier.height(16.dp))
        Text("Network Error / Crash Recovery", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.error)
        Spacer(Modifier.height(8.dp))
        Text(message, style = MaterialTheme.typography.bodyMedium)
    }
}
