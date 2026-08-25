with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "r") as f:
    text = f.read()

text = text.replace(
    '''        }
        } else if (action == ACTION_CHECK_QUEUE) {
            checkQueue()
        }

        return START_NOT_STICKY
    }''',
    '''        } else if (action == ACTION_CHECK_QUEUE) {
            checkQueue()
        }

        return START_NOT_STICKY
    }'''
)

with open("app/src/main/java/com/aistudio/ytdownloader/DownloadService.kt", "w") as f:
    f.write(text)
