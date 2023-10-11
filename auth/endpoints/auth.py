from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.db.connection import get_session
from auth.schemas import SignupRequest, SignupSuccess, LoginRequest, LoginResponse
from auth.services import create_user, authenticate_user
from auth.config import get_settings

api_router = APIRouter(
    prefix="",
    tags=["Authentication/Registration"],
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


@api_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    # response_model=LoginResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters for login",
        },
    },
)
async def login(
        _: Request,
        login_form: LoginRequest = Body(...),
        session: AsyncSession = Depends(get_session),
):
    try:
        return await authenticate_user(session, login_form.phone, login_form.password)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='wrong credentials')


async def refresh(
        _: Request,
        session: AsyncSession = Depends(get_session),
):
    pass
