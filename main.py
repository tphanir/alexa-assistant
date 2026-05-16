from fastapi import FastAPI

app = FastAPI()

@app.post("/")
async def root():

    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Backend reached successfully"
            },
            "shouldEndSession": False
        }
    }