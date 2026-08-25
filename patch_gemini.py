import sys

with open('app/src/main/java/com/aistudio/ytdownloader/GeminiService.kt', 'r') as f:
    content = f.read()

# Replace GenerationConfig and remove ResponseFormat
old_classes = '''@Serializable
data class ResponseFormat(
    val text: ResponseFormatText? = null
)

@Serializable
data class ResponseFormatText(
    val mimeType: String,
    val schema: JsonObject? = null
)

@Serializable
data class GenerationConfig(
    val responseFormat: ResponseFormat? = null,
    val temperature: Float? = null
)'''

new_classes = '''@Serializable
data class GenerationConfig(
    val responseMimeType: String? = null,
    val responseSchema: JsonObject? = null,
    val temperature: Float? = null
)'''

content = content.replace(old_classes, new_classes)

old_config_usage = '''        generationConfig = GenerationConfig(
            temperature = 0.2f,
            responseFormat = ResponseFormat(
                text = ResponseFormatText(
                    mimeType = "application/json",
                    schema = schema
                )
            )
        )'''

new_config_usage = '''        generationConfig = GenerationConfig(
            temperature = 0.2f,
            responseMimeType = "application/json",
            responseSchema = schema
        )'''

content = content.replace(old_config_usage, new_config_usage)

with open('app/src/main/java/com/aistudio/ytdownloader/GeminiService.kt', 'w') as f:
    f.write(content)
