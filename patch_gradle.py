with open("app/build.gradle.kts", "r") as f:
    text = f.read()
text = text.replace('implementation("io.github.junkfood02.youtubedl-android:ffmpeg:0.18.1")', 'implementation("io.github.junkfood02.youtubedl-android:ffmpeg:0.18.1")\n    implementation("com.google.code.gson:gson:2.11.0")')
with open("app/build.gradle.kts", "w") as f:
    f.write(text)
