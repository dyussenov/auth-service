from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.db.connection import get_session
from auth.schemas import HealthCheckResponse

from auth.services import health_check_db


api_router = APIRouter(
    prefix="/health_check",
    tags=["Application Health"],
)


@api_router.get(
    "/ping_application",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
)
async def ping_application(
    _: Request,
):
    return {"message": "Application alive!"}


@api_router.get(
    "/ping_database",
    response_model=HealthCheckResponseh6j6;m7 :<<PHG,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Database isn't working"}},
)
async def ping_database(
    _: Request,
    session: AsyncSession = Depends(get_session),
):
    if await health_check_db(session):
        return {"message": "Database worked!"}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database isn't working",
    )
