from fastapi import FastAPI, Request
import boto3
import json

app = FastAPI()

sns_client = boto3.client("sns", region_name="us-east-1")

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:762233762592:clinic-system-topic"

@app.post("/notify")
async def notify(req: Request):
    body = await req.json()

    message_content = body.get("message", "")

    plain_text_message = f"""
    Notification from Clinic:

    {message_content}

    — The Clinic Team
    """

    response = sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=plain_text_message,  
        Subject=body.get("subject", "Clinic Appointment Booked")
    )

    print("SNS response:", response)

