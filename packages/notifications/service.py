import smtplib
from email.message import EmailMessage
from typing import Any

from sqlalchemy.orm import Session

from apps.api.app.config import get_settings
from packages.core.constants import TARGET_EMAIL
from packages.db.models.notification import Notification
from packages.notifications.yahoo_mailer import build_message


class NotificationService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def enqueue(self, session: Session, notification_type: str, subject: str, payload_json: dict[str, Any]) -> Notification:
        notification = Notification(
            notification_type=notification_type,
            target_email=TARGET_EMAIL,
            subject=subject,
            payload_json=payload_json,
            status="pending",
        )
        session.add(notification)
        session.commit()
        session.refresh(notification)
        return notification

    def send_pending(self, session: Session, limit: int = 20) -> int:
        pending = (
            session.query(Notification)
            .filter(Notification.status == "pending")
            .order_by(Notification.created_at.asc())
            .limit(limit)
            .all()
        )
        sent_count = 0
        for item in pending:
            text_body = item.payload_json.get("text_body", item.subject)
            html_body = item.payload_json.get("html_body")
            message = build_message(item.subject, item.target_email, text_body, html_body)
            self._deliver(message)
            item.status = "sent"
            item.sent_at = item.created_at
            session.add(item)
            sent_count += 1
        session.commit()
        return sent_count

    def _deliver(self, message: EmailMessage) -> None:
        username = self.settings.yahoo_smtp_username
        password = self.settings.yahoo_smtp_app_password
        message["From"] = username
        if not password or password == "change-me":
            return
        with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465, timeout=30) as smtp:
            smtp.login(username, password)
            smtp.send_message(message)

