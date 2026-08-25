import re

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target1 = "var availableQualities by remember { mutableStateOf<List<VideoQuality>?>(null) }"
rep1 = "var availableQualities by remember { mutableStateOf<List<QualityOption>?>(null) }"
content = content.replace(target1, rep1)

target2 = "items(availableQualities ?: VideoQuality.values().toList()) { quality ->"
rep2 = "items(availableQualities ?: VideoQuality.values().map { QualityOption(it, \"\") }) { qualityOpt ->"
content = content.replace(target2, rep2)

target3 = "RadioButton(selected = selectedQuality == quality, onClick = { selectedQuality = quality })"
rep3 = "RadioButton(selected = selectedQuality == qualityOpt.quality, onClick = { selectedQuality = qualityOpt.quality })"
content = content.replace(target3, rep3)

target4 = "Text(quality.label)"
rep4 = "Text(if (qualityOpt.sizeStr.isNotEmpty()) \"${qualityOpt.quality.label} (~${qualityOpt.sizeStr})\" else qualityOpt.quality.label)"
content = content.replace(target4, rep4)

target5 = "Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable { selectedQuality = quality }.fillMaxWidth()) {"
rep5 = "Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable { selectedQuality = qualityOpt.quality }.fillMaxWidth()) {"
content = content.replace(target5, rep5)

# Wait, `qualities.find { it == selectedQuality }` in the fetch side
# `val qualities = viewModel.fetchAvailableQualities(formatDialogUrl!!)`
# `qualities` is `List<QualityOption>`
# So in MainActivity.kt:
# `selectedQuality = qualities.find { it.quality == selectedQuality }?.quality ?: qualities.lastOrNull()?.quality ?: VideoQuality.High720`

target6 = "selectedQuality = qualities.find { it == selectedQuality } ?: qualities.lastOrNull() ?: VideoQuality.High720"
rep6 = "selectedQuality = qualities.find { it.quality == selectedQuality }?.quality ?: qualities.lastOrNull()?.quality ?: VideoQuality.High720"
content = content.replace(target6, rep6)


with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
print("done main")
