from dotenv import load_dotenv
from fastapi import FastAPI, Request
import os, requests

load_dotenv()

app = FastAPI()

@app.post("/notify")
async def notify(req: Request):
    body = await req.json()
    to = body.get("to")
    subject = body.get("subject")
    message = body.get("message")
    response = requests.post(
        "https://api.mailgun.net/v3/sandbox1c8fc794354f4626a8ced3957cdcf223.mailgun.org/messages",
        auth=("api", os.getenv('API_KEY')),
        data={"from": "Mailgun Sandbox <postmaster@sandbox1c8fc794354f4626a8ced3957cdcf223.mailgun.org>",
              "to": to,
              "subject": subject,
              "html": message})
    print(response)
    return {"status": response.status_code, "detail": response.text}
