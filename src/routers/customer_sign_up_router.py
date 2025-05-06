from fastapi import APIRouter, BackgroundTasks, Form, HTTPException, Request, status
from loguru import logger

from config import settings
from dependencies import GetDBDep, GetCurrentUserDep
from emails import send_email
from schemas.customer_sign_up_schema import CustomerSignUpSchema
from templates import render_template


customer_sign_up_router = APIRouter(prefix="/sign_up", tags=["Customer Sign Up"])


@customer_sign_up_router.post("/")
async def submit_customer_sign_up(
    background_tasks: BackgroundTasks,
    request: Request,
    data: CustomerSignUpSchema,
):
    try:
        customer = data.customer
        dogs = data.dogs

        logger.debug(f"{customer = }")
        logger.debug(f"{dogs = }")

        content = render_template(
            "emails/customer_sign_up.html",
            {"customer": customer, "dogs": dogs, "request": request},
        )

        background_tasks.add_task(
            send_email,
            to=[customer.email],
            bcc=[settings.MAIL_USERNAME],
            subject="🎉🐾 W4lkies Customer Sign Up 🐾🎉",
            content=content,
        )

        return {"message": "Customer sign-up notification sent in the background"}

    except Exception as e:
        logger.error(f"Error processing customer signup form: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
