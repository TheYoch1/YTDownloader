import sys

with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

deps = '''    implementation("androidx.datastore:datastore-preferences:1.1.1")
    implementation("com.github.yausername.youtubedl-android:library:0.16.3")
    implementation("com.github.yausername.youtubedl-android:ffmpeg:0.16.3")'''

content = content.replace('    implementation("androidx.datastore:datastore-preferences:1.1.1")', deps)

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
