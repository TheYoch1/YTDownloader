import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('applet/.env')
api_key = os.getenv('GEMINI_API_KEY')

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Search YouTube for 'lofi girl' and return a list of the top 5 relevant video titles and their YouTube URLs."
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
}

response = requests.post(url, json=payload)
print(response.status_code)
print(response.text)
