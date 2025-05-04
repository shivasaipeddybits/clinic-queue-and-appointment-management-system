from pydantic import BaseModel, EmailStr

class NotificationRequest(BaseModel):
    to: EmailStr
    subject: str
    message: str
