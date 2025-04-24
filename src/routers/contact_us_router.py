# emails.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to: str, subject: str, content: str):
    msg = MIMEMultipart()
    msg["From"] = f"{settings.MAIL_DEFAULT_SENDER_NAME} <{settings.MAIL_USERNAME}>"
    msg["To"] = to
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


# contact_us_router.py


from typing import Annotated, Union

from fastapi import APIRouter, BackgroundTasks, Form, HTTPException, status
from fastapi import Request
from fastapi.templating import Jinja2Templates
from loguru import logger

from dependencies import GetDBDep, GetCurrentUserDep
from config import settings

templates = Jinja2Templates(directory="src/templates")

contact_us_router = APIRouter(prefix="/contact_us", tags=["Contact Us"])


@contact_us_router.post("/")
async def submit_contact_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    request: Request = Request,
):
    logger.debug(f"{name = } {email = } {message = }")
    content = templates.TemplateResponse(
        "emails/contact_us.html",
        {"name": name, "email": email, "message": message, "request": request},
    ).body.decode("utf-8")
    logger.debug(f"{content = }")
    background_tasks.add_task(
        send_email,
        to=settings.MAIL_USERNAME,
        subject="New Contact Us Notification",
        content=content,
    )
    return {"message": "Contact us notification sent in the background"}
