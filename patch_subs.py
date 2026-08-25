import sys

with open('app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt', 'r') as f:
    content = f.read()

old_subs = '''                    request.addOption("-f", formatStr)
                }
                
                if (settings.downloadSubtitles) {
                    request.addOption("--write-auto-subs")
                    request.addOption("--write-subs")
                    request.addOption("--sub-langs", "en.*")
                    
                    if (!settings.audioOnly) {
                        request.addOption("--embed-subs")
                        request.addOption("--merge-output-format", "mkv")
                    }
                }'''

new_subs = '''                    request.addOption("-f", formatStr)
                    request.addOption("--merge-output-format", "mp4")
                }
                
                if (settings.downloadSubtitles) {
                    request.addOption("--write-auto-subs")
                    request.addOption("--write-subs")
                    request.addOption("--sub-langs", "en.*")
                    request.addOption("--convert-subs", "srt")
                }'''

content = content.replace(old_subs, new_subs)

with open('app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt', 'w') as f:
    f.write(content)
