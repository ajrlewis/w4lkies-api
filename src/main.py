from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from config import settings
from routers import (
    auth_router,
    user_router,
    customer_router,
    vet_router,
    dog_router,
    service_router,
    booking_router,
    invoice_router,
    expense_router,
)

logger.debug("Creating application ...")
app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    summary=settings.PROJECT_SUMMARY,
    version=settings.PROJECT_VERSION,
    # terms_of_service=settings.PROJECT_TERMS_OF_SERVICE,
    # contact={
    #     "name": settings.PROJECT_CONTACT_NAME
    #     "url": settings.PROJECT_CONTACT_URL,
    #     "email": settings.PROJECT_CONTACT_EMAIL,
    # },
    license_info={
        "name": settings.PROJECT_LICENSE,
        "url": settings.PROJECT_LICENSE_URL,
    },
)


logger.debug("Mounting static directory ...")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

logger.debug("Adding CORS middleware ...")
allow_origins = settings.ALLOW_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Pagination"],
    expose_headers=["X-Pagination"],
)


logger.debug("Including routes ...")
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(customer_router)
app.include_router(vet_router)
app.include_router(dog_router)
app.include_router(service_router)
app.include_router(booking_router)
app.include_router(invoice_router)
app.include_router(expense_router)


from routers import contact_us_router, customer_sign_up_router

app.include_router(contact_us_router)
app.include_router(customer_sign_up_router)


@app.get("/")
async def read_root():
    return {"message": "Hello World!"}
