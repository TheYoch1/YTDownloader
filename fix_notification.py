import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    content = f.read()

target = '''                pendingIntent = android.app.PendingIntent.getActivity(application, id.hashCode(), intent, flags)
            }
            
            showNotification("$typeStr Download Complete", "$titleStr has finished downloading.", id.hashCode(), pendingIntent)
        } catch (e: Exception) {'''

rep = '''                pendingIntent = android.app.PendingIntent.getActivity(application, id.hashCode(), intent, flags)
            }
            
            if (_appConfig.value.notifyOnComplete) {
                showNotification("$typeStr Download Complete", "$titleStr has finished downloading.", id.hashCode(), pendingIntent)
            }
        } catch (e: Exception) {'''

content = content.replace(target, rep)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
    f.write(content)
