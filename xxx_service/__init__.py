"""Central web xxx_service config"""
import json
import logging.config
import os
from typing import Dict

from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from xxx_service.xxx import xxx_service_router
from xxx_service.info import info_router

xxx_service_app: FastAPI = FastAPI()


@xxx_service_app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Log cause of invalid requests"""
    logging.error(f"Invalid Request: {json.dumps(exc.errors(), indent=4)}")
    return await request_validation_exception_handler(request, exc)


@xxx_service_app.on_event("startup")
def startup_event() -> None:
    """Fastapi startup event hook"""
    init(xxx_service_app)


@xxx_service_app.get("/health")
async def health() -> Dict[str, str]:
    """Basic health endpoint"""
    return {"status": "UP"}


def init(xxx_service_app_instance: FastAPI) -> None:
    """Web App general config and boostrapping"""
    # https://medium.com/@PhilippeGirard5/fastapi-logging-f6237b84ea64
    logging_conf = os.path.dirname(__file__) + os.sep + "logging.conf"
    logging.config.fileConfig(logging_conf, disable_existing_loggers=False)

    # load routes
    xxx_service_app_instance.include_router(info_router, prefix="/info")
    xxx_service_app_instance.include_router(
        xxx_service_router, prefix="/xxx"
    )
