API_KEY=$(grep GEMINI_API_KEY applet/.env | cut -d '=' -f 2)

curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key=${API_KEY}" \
-H 'Content-Type: application/json' \
-d '{
    "contents": [
        {
            "parts": [
                {
                    "text": "Search YouTube for \"lofi girl\" and return a list of the top 5 relevant video titles and their YouTube URLs."
                }
            ]
        }
    ],
    "tools": [
        {
            "googleSearch": {}
        }
    ],
    "generationConfig": {
        "temperature": 0.2,
        "responseMimeType": "application/json",
        "responseSchema": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "title": {
                        "type": "STRING"
                    },
                    "url": {
                        "type": "STRING"
                    }
                },
                "required": [
                    "title",
                    "url"
                ]
            }
        }
    }
}'
