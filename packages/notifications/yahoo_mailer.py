from email.message import EmailMessage


def build_message(subject: str, to_email: str, text_body: str, html_body: str | None = None) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = subject
    message["To"] = to_email
    message.set_content(text_body)
    if html_body:
        message.add_alternative(html_body, subtype="html")
    return message


def top_job_email(company: str, title: str, location: str, score: float, action_url: str) -> tuple[str, str, str]:
    subject = f"[Job Bot] New Top Match: {company} - {title}"
    text = (
        f"Company: {company}\n"
        f"Role: {title}\n"
        f"Location: {location}\n"
        f"Score: {score}\n"
        f"Link: {action_url}\n"
    )
    html = (
        f"<h2>{company} - {title}</h2>"
        f"<p><strong>Location:</strong> {location}</p>"
        f"<p><strong>Score:</strong> {score}</p>"
        f"<p><a href=\"{action_url}\">Open job</a></p>"
    )
    return subject, text, html
