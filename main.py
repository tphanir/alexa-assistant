from fastapi import FastAPI, Request
import requests
import os
import json

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@app.get("/")
async def home():
    return {"message": "Alexa AI Buddy backend running"}


@app.post("/")
async def alexa_webhook(request: Request):

    # Receive Alexa request JSON
    body = await request.json()

    print("========== ALEXA REQUEST ==========")
    print(json.dumps(body, indent=2))

    request_type = body["request"]["type"]

    # ---------------------------------------------------
    # LaunchRequest
    # Triggered when user says:
    # "Alexa, open ai buddy"
    # ---------------------------------------------------
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

    # ---------------------------------------------------
    # IntentRequest
    # Triggered when user says:
    # "ask who is Einstein"
    # ---------------------------------------------------
    elif request_type == "IntentRequest":

        try:
            user_text = body["request"]["intent"]["slots"]["query"]["value"]
        except:
            user_text = "Hello"

        print("USER:", user_text)

        try:

            # Send query to Groq
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-70b-8192",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a multilingual AI voice assistant. "
                                "Reply naturally and conversationally. "
                                "Reply in the same language as the user. "
                                "Support English, Telugu, and Hindi. "
                                "Keep responses short, under 40 words."
                            )
                        },
                        {
                            "role": "user",
                            "content": user_text
                        }
                    ],
                    "temperature": 0.7
                }
            )

            groq_json = response.json()

            print("========== GROQ RESPONSE ==========")
            print(json.dumps(groq_json, indent=2))

            answer = groq_json["choices"][0]["message"]["content"]

        except Exception as e:

            print("ERROR:", str(e))

            answer = "Sorry, something went wrong."

        # Send response back to Alexa
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

    # ---------------------------------------------------
    # Unknown request fallback
    # ---------------------------------------------------
    else:

        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "I could not understand that request."
                },
                "shouldEndSession": False
            }
        }