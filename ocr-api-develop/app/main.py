from contextlib import asynccontextmanager

import uvicorn
import asyncio
from app.messaging import kafka_consumer
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api.api_router import router
from app.common.config import settings
from app.db.base import init_db
from app.helpers.exception_handler import (
    BaseHTTPException,
    CustomException,
    base_exception_handler,
    custom_404_handler,
    custom_validation_error,
    http_exception_handler,
)

origins = [
    "*",
    "http://localhost:8080"
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)

    app.state.db = app.database

    # Start Kafka consumer
    consumer_task = asyncio.create_task(kafka_consumer.consume_messages(app.state.db))
    consumer_task = asyncio.create_task(kafka_consumer.consume_messages_recog(app.state.db))

    yield

    # Close Kafka consumer when app shuts down
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        print(f"Cancel consumer")
        pass

    app.client.close()


def get_application(app_config: dict) -> FastAPI:
    application = FastAPI(**app_config)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(router, prefix=settings.API_PREFIX)
    application.add_exception_handler(BaseHTTPException, base_exception_handler)
    application.add_exception_handler(CustomException, http_exception_handler)
    application.add_exception_handler(RequestValidationError, custom_validation_error)
    application.add_exception_handler(404, custom_404_handler)
    return application


app_config = {
    "title": f"{settings.PROJECT_NAME}",
    "docs_url": "/docs",
    "redoc_url": "/re-docs",
    "openapi_url": f"{settings.API_PREFIX}/openapi.json",
    "description": "OCR Management System",
    "lifespan": lifespan,
}
app = get_application(app_config)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
