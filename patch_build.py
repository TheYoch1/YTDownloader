import sys

with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

content = content.replace('    id("com.google.android.libraries.mapsplatform.secrets-gradle-plugin")\n', '')

content = content.replace('        buildConfig = true\n', '')

secrets_block = '''    secrets {
        propertiesFileName = ".env"
        defaultPropertiesFileName = ".env.example"
    }'''
content = content.replace(secrets_block, '')

content = content.replace('    implementation("com.squareup.retrofit2:retrofit:2.11.0")\n', '')
content = content.replace('    implementation("com.squareup.retrofit2:converter-kotlinx-serialization:2.11.0")\n', '')
content = content.replace('    implementation("com.squareup.okhttp3:okhttp:4.12.0")\n', '')

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
