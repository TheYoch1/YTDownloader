with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """    if (showSettings) {
            SettingsBottomSheet(
                settings = settings,
                config = config,
                onDismiss = { showSettings = false },
                onSettingsChanged = { viewModel.updateCurrentSettings(it) },
                onConfigChanged = { viewModel.updateConfig(it) }
            )
        }"""

replacement = """    if (showSettings) {
            SettingsBottomSheet(
                settings = settings,
                config = config,
                onDismiss = { showSettings = false },
                onSettingsChanged = { viewModel.updateCurrentSettings(it) },
                onConfigChanged = { viewModel.updateConfig(it) },
                onViewErrorLog = { showErrorLog = true }
            )
        }"""

if target in content:
    content = content.replace(target, replacement)
    print("Fixed SettingsBottomSheet call")
else:
    print("Could not find target!")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
