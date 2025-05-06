import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from loguru import logger

from config import settings


def send_email(to: list[str], subject: str, content: str, bcc: list[str] = []):
    msg = MIMEMultipart()
    msg["From"] = f"{settings.MAIL_DEFAULT_SENDER_NAME} <{settings.MAIL_USERNAME}>"
    msg["To"] = ", ".join(to)
    if bcc:
        msg["Bcc"] = ", ".join(bcc)
    msg["Subject"] = subject
    msg.attach(MIMEText(content, "html"))
    try:
        server = smtplib.SMTP(settings.MAIL_SERVER, 587)
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
        logger.debug("Email sent successfully")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
