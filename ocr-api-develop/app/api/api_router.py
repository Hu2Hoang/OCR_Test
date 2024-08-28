from fastapi import APIRouter

from app.api.routes import test, api_healthcheck

router = APIRouter()

router.include_router(test.router, tags=["test"])
router.include_router(api_healthcheck.router, tags=["health-check"], prefix="/healthcheck")
