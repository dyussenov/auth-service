from datetime import datetime, timedelta

from jose import jwt
from jose.jwt import JWTError
from sqlalchemy import exc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth.config import get_settings
from auth.db.models import User
from auth.exceptions import AuthException
from auth.schemas import LoginResponse, SignupRequest, UserResponse


async def create_user(
        session: AsyncSession, potential_user: SignupRequest
) -> User | None:
    user = User(
        email=potential_user.email,
        phone=potential_user.phone,
        name=potential_user.name,
        surname=potential_user.surname,
        user_type=potential_user.user_type,
        hashed_password=potential_user.password,
    )
    session.add(user)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False, "User already exists."
    return True, "Successful registration!"


def create_token(sub, exp, jwt_secret, user):
    now = datetime.utcnow()
    payload = {
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(seconds=exp),
        "sub": sub,
        "user": user,
    }
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return token


def verify_password(
        plain_password: str,
        hashed_password: str,
):
    pwd_context = get_settings().PWD_CONTEXT
    return pwd_context.verify(plain_password, hashed_password)


def user_helper(user: User) -> dict:
    """serialize orm user object to python dict"""
    user_dict = UserResponse(
        email=user.email,
        phone=user.phone,
        name=user.name,
        surname=user.surname,
        user_type=user.user_type,
    )
    return user_dict.model_dump()


async def authenticate_user(
        session: AsyncSession, phone: str, plain_password: str
) -> LoginResponse:
    stmt = select(User).where(User.phone == phone)
    result = await session.execute(stmt)
    user = result.scalar()
    settings = get_settings()
    if not user:
        raise AuthException("wrong phone or paasword")

    if verify_password(plain_password, user.hashed_password):
        user_dict = user_helper(user)
        return LoginResponse(
            access_token=create_token(
                user.user_id,
                settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                settings.SECRET_KEY,
                user_dict,
            ),
            refresh_token=create_token(
                user.user_id,
                settings.REFRESH_TOKEN_EXPIRE_SECONDS,
                settings.SECRET_KEY,
                user_dict,
            ),
        )
    else:
        raise AuthException("wrong phone or paasword")


async def validate_token(refresh_token: str):
    settings = get_settings()

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY)
        return {
            "access_token": create_token(
                payload["sub"],
                settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                settings.SECRET_KEY,
                payload["user"],
            ),
            "refresh_token": create_token(
                payload["sub"],
                settings.REFRESH_TOKEN_EXPIRE_SECONDS,
                settings.SECRET_KEY,
                payload["user"],
            ),
        }
    except JWTError:
        raise AuthException("invalid JWT")


async def send_password_reset(
        session: AsyncSession,
        email: str
) -> bool:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar()
    settings = get_settings()
    if user:
        reset_password_token = create_token(
            user.user_id,
            settings.REFRESH_TOKEN_EXPIRE_SECONDS,
            settings.SECRET_KEY,
            user_helper(user),
        )
        # todo: send token
        print(reset_password_token)

    return True


async def confirm_password_reset(
        token: str,
        new_password: str,
        session: AsyncSession,
):
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
    except JWTError:
        raise AuthException("invalid JWT")

    stmt = select(User).where(User.email == payload["user"]["email"])
    result = await session.execute(stmt)
    user = result.scalar()

    new_hashed_password = settings.PWD_CONTEXT.hash(new_password)
    stmt = update(User).where(User.email == payload["user"]["email"]).values(name='zaloopa')
    print(stmt)
    res = await session.execute(stmt)
    print(res)