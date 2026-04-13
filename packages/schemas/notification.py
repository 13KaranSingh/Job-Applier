from pydantic import BaseModel


class NotificationSchema(BaseModel):
    notification_type: str
    target_email: str
    subject: str
    payload_json: dict
    status: str

