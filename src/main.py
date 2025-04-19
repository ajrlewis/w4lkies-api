from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from config import settings
from routers import auth_router, user_router, customer_router

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


logger.debug("Adding CORS middleware ...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.debug("Including routes ...")
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(customer_router)

import time
from fastapi import Request


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
