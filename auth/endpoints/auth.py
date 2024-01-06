from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.db.connection import get_session
from auth.exceptions import AuthException
from auth.schemas import (
    LoginRequest,
    LoginResponse,
    SignupRequest,
    SignupSuccess,
    TokenRequest,
    TokenResponse,
    PasswordResetRequest,
    PasswordResetResponse
)
from auth.services import (
    authenticate_user,
    create_user,
    validate_token,
    send_password_reset,
    confirm_password_reset
)

api_router = APIRouter(
    prefix="",
    tags=["Authentication/Registration"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
    response_model=LoginResponse,
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
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exception)
        )


@api_router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid token",
        },
    },
)
async def refresh(
        _: Request,
        data: TokenRequest,
):
    """
    Логика работы: прикладываешь рефреш, получаешь пару акцесс+рефреш. старый рефреш становится недействительным
    """
    try:
        return await validate_token(data.refresh_token)
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exception)
        )


@api_router.post(
    "/reset-password-request",
    status_code=status.HTTP_200_OK,
    response_model=PasswordResetResponse,
)
async def password_reset_request(
        _: Request,
        data: PasswordResetRequest,
        session: AsyncSession = Depends(get_session),
):
    await send_password_reset(session=session, email=data.email)
    return PasswordResetResponse(message='reset message send to user')


@api_router.post(
    "/confirm-password-reset",
    status_code=status.HTTP_200_OK,
    response_model=PasswordResetResponse,
)
async def password_reset_request(
        _: Request,
        token: str,
        session: AsyncSession = Depends(get_session),
):
    try:
        await confirm_password_reset(session=session, token=token, new_password='qwerty')
        return PasswordResetResponse(message='successful password reset')
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception)
        )
