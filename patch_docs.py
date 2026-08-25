import sys

with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

content = content.replace('com.github.yausername.youtubedl-android:library:0.17.1', 'io.github.junkfood02.youtubedl-android:library:0.18.1')
content = content.replace('com.github.yausername.youtubedl-android:ffmpeg:0.17.1', 'io.github.junkfood02.youtubedl-android:ffmpeg:0.18.1')

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
