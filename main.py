from fastapi import FastAPI, Request
import requests
import os
import json

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/")
async def alexa_webhook(request: Request):

    body = await request.json()

    print(json.dumps(body, indent=2))

    request_type = body["request"]["type"]

    # Skill opened
    if request_type == "LaunchRequest":

        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Hello. Ask me anything."
                },
                "shouldEndSession": False
            }
        }

    # User asked something
    elif request_type == "IntentRequest":

        try:
            user_text = body["request"]["intent"]["slots"]["query"]["value"]
        except:
            user_text = "Hello"

        print("USER:", user_text)

        # TEMPORARY TEST
        answer = f"You said {user_text}"

        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": answer
                },
                "shouldEndSession": False
            }
        }