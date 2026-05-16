from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/")
def home():
    return {"message": "Alexa backend running"}

@app.post("/")
async def alexa_webhook(request: Request):
    body = await request.json()

    try:
        user_text = body["request"]["intent"]["slots"]["query"]["value"]
    except:
        user_text = "Hello"

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
                        "Reply briefly in the same language as the user."
                    )
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        }
    )

    answer = response.json()["choices"][0]["message"]["content"]

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