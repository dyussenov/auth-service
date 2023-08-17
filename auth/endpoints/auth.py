from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.db.connection import get_session
from auth.schemas import SignupRequest, SignupSuccess
from auth.services import create_user

api_router = APIRouter(
    prefix="",
    tags=["Authentication+Registration"],
)


@api_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=SignupSuccess,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters for registration",
        },
    },
)
async def signup(
    _: Request,
    signup_form: SignupRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):
    is_success, message = await create_user(session, signup_form)
    if is_success:
        return {"message": message}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )
