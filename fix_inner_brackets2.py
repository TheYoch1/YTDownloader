with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target = """    if (showSettings) {
            SettingsBottomSheet(
                settings = settings,
                config = config,
                onDismiss = { showSettings = false },
                onSettingsChanged = { viewModel.updateCurrentSettings(it) },
                onConfigChanged = { viewModel.updateConfig(it) },
                onViewErrorLog = { showErrorLog = true }
            )
        }
    }
}
}
@Composable
fun DownloadItemCard("""

replacement = """    if (showSettings) {
            SettingsBottomSheet(
                settings = settings,
                config = config,
                onDismiss = { showSettings = false },
                onSettingsChanged = { viewModel.updateCurrentSettings(it) },
                onConfigChanged = { viewModel.updateConfig(it) },
                onViewErrorLog = { showErrorLog = true }
            )
        }
    }
}
@Composable
fun DownloadItemCard("""

content = content.replace(target, replacement)

# Now check the total brackets again
opened = content.count('{')
closed = content.count('}')
print(f"Total opened: {opened}, closed: {closed}")

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
