import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.api import ws
from app.api.dependencies import emulator_service
from app.api.routes import commands, parameters, status
from app.core.config import settings
from app.core.logging import setup_logging


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()

    logger.info("application starting")

    task = asyncio.create_task(emulator_service.start_loop())

    yield

    task.cancel()

    logger.info("application stopped")


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ValueError)
async def value_error_handler(
    request: Request,
    exc: ValueError,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": str(exc),
        },
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(
    request: Request,
    exc: ValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "validation failed",
            "details": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception("unhandled exception")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "internal server error",
        },
    )

app.include_router(ws.router)

app.include_router(
    status.router,
    prefix=settings.api_prefix,
)

app.include_router(
    parameters.router,
    prefix=settings.api_prefix,
)

app.include_router(
    commands.router,
    prefix=settings.api_prefix,
)