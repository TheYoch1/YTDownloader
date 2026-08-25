import re

with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "r") as f:
    text = f.read()

# Make sure processDownload has a closing bracket
split_point = text.find("    fun cancelDownload(id: String) {")
if split_point != -1:
    top_half = text[:split_point]
    
    # Check if processDownload ends cleanly before cancelDownload
    pd_end = top_half.rfind("finally {")
    if pd_end != -1:
        # Just ensure there are the right number of closing brackets after finally
        pd_segment = top_half[pd_end:]
        expected_close = "}        }    }"
        if expected_close not in pd_segment.replace('\n', '').replace(' ', ''):
            # We are missing brackets for the catch/finally block of processDownload
            print("Missing brackets detected before cancelDownload")
            top_half = top_half.rsplit("finally {", 1)[0] + "        } finally {\n            stopForegroundServiceIfDone()\n        }\n    }\n"
            
            with open("app/src/main/java/com/aistudio/ytdownloader/DownloaderViewModel.kt", "w") as f:
                f.write(top_half + text[split_point:])
