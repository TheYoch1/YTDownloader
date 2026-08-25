import re

path_data = "M 32,32 C 25.4,32 20,37.4 20,44 L 20,64 C 20,70.6 25.4,76 32,76 L 46,76 L 46,80 L 40,80 L 54,94 L 68,80 L 62,80 L 62,76 L 76,76 C 82.6,76 88,70.6 88,64 L 88,44 C 88,37.4 82.6,32 76,32 Z M 32,40 L 76,40 C 78.2,40 80,41.8 80,44 L 80,64 C 80,66.2 78.2,68 76,68 L 62,68 L 54,68 L 46,68 L 32,68 C 29.8,68 28,66.2 28,64 L 28,44 C 28,41.8 29.8,40 32,40 Z M 48,46 L 48,62 L 64,54 Z"

def replace_coord(match):
    x = float(match.group(1))
    y = float(match.group(2))
    
    # Scale by 0.65 and center on 54, 54
    # original center: cx=54, cy=63
    new_x = (x - 54) * 0.65 + 54
    new_y = (y - 63) * 0.65 + 54
    
    return f"{new_x:g},{new_y:g}"

# The regex looks for a space/letter, then number, comma, number.
# Wait, let's tokenize
tokens = path_data.split(' ')
new_tokens = []
for t in tokens:
    if ',' in t:
        x, y = map(float, t.split(','))
        new_x = (x - 54) * 0.65 + 54
        new_y = (y - 63) * 0.65 + 54
        new_tokens.append(f"{new_x:g},{new_y:g}")
    else:
        new_tokens.append(t)

new_path = ' '.join(new_tokens)
print(new_path)

with open("app/src/main/res/drawable/ic_launcher_foreground.xml", "w") as f:
    f.write(f'''<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">

    <path
        android:fillColor="#FFFFFF"
        android:pathData="{new_path}"
        android:fillType="evenOdd" />
</vector>
''')

with open("app/src/main/res/drawable/ic_launcher_monochrome.xml", "w") as f:
    f.write(f'''<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">

    <path
        android:fillColor="#000000"
        android:pathData="{new_path}"
        android:fillType="evenOdd" />
</vector>
''')

