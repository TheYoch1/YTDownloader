import re

with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

target_perms = '<uses-permission android:name="android.permission.INTERNET" />'
rep_perms = '''<uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />'''

content = content.replace(target_perms, rep_perms)

target_service = '</application>'
rep_service = '''    <service android:name=".DownloadService" android:foregroundServiceType="dataSync" android:exported="false" />
    </application>'''

content = content.replace(target_service, rep_service)

with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write(content)
print("done")
