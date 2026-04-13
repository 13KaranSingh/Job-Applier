from email.message import EmailMessage


def build_message(subject: str, to_email: str, text_body: str, html_body: str | None = None) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = subject
    message["To"] = to_email
    message.set_content(text_body)
    if html_body:
        message.add_alternative(html_body, subtype="html")
    return message

