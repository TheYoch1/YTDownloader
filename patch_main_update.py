with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

# Append the API function at the very end
api_code = """
data class GithubRelease(val tag_name: String, val html_url: String)

suspend fun checkGithubUpdate(): GithubRelease? {
    return kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
        try {
            val client = okhttp3.OkHttpClient()
            val request = okhttp3.Request.Builder()
                .url("https://api.github.com/repos/yochmovies/YTDownloader/releases/latest")
                .header("User-Agent", "YTDownloader-Update-Checker")
                .build()
            val response = client.newCall(request).execute()
            if (response.isSuccessful) {
                response.body?.string()?.let {
                    com.google.gson.Gson().fromJson(it, GithubRelease::class.java)
                }
            } else null
        } catch (e: Exception) {
            null
        }
    }
}
"""
if "checkGithubUpdate" not in text:
    text += api_code

# Inject LaunchedEffect and AlertDialog into MainScreen
mainscreen_start = "    var showSettings by remember { mutableStateOf(false) }"
mainscreen_update_ui = """    var showSettings by remember { mutableStateOf(false) }
    
    var updateAvailable by remember { mutableStateOf<GithubRelease?>(null) }
    val context = LocalContext.current
    
    LaunchedEffect(Unit) {
        try {
            val release = checkGithubUpdate()
            if (release != null) {
                val currentVersion = BuildConfig.VERSION_NAME
                val remoteVersion = release.tag_name.removePrefix("v")
                if (remoteVersion != currentVersion && release.tag_name != currentVersion) {
                    updateAvailable = release
                }
            }
        } catch(e: Exception) {
            // Ignore failure
        }
    }
    
    if (updateAvailable != null) {
        val release = updateAvailable!!
        AlertDialog(
            onDismissRequest = { updateAvailable = null },
            title = { Text("Update Available") },
            text = { Text("A new version (${release.tag_name}) is available. Would you like to download it?") },
            confirmButton = {
                TextButton(onClick = {
                    try {
                        val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(release.html_url))
                        context.startActivity(intent)
                    } catch(e: Exception) {}
                    updateAvailable = null
                }) {
                    Text("Download")
                }
            },
            dismissButton = {
                TextButton(onClick = { updateAvailable = null }) {
                    Text("Later")
                }
            }
        )
    }
"""

if "updateAvailable" not in text:
    text = text.replace(mainscreen_start, mainscreen_update_ui)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)

