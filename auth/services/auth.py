from datetime import datetime, timedelta

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt
from jose.jwt import JWTError

from auth.db.models import User
from auth.schemas import SignupRequest, LoginResponse
from auth.config import get_settings


async def validate_token(refresh_token: str, session: AsyncSession):
    settings = get_settings()

    try:
        e = jwt.decode(refresh_token, settings.SECRET_KEY)
        print(e)
    except JWTError:
        raise Exception
    return {
        'access_token': 'qwerty',
        'refresh_token': 'aasdfg'
    }


async def create_user(
        session: AsyncSession, potential_user: SignupRequest
) -> User | None:
    user = User(
        email=potential_user.email,
        phone=potential_user.phone,
        hashed_password=potential_user.password,
    )
    session.add(user)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False, "User already exists."
    return True, "Successful registration!"


def create_token(sub, exp, jwt_secret):
    now = datetime.utcnow()
    payload = {
        'iat': now,
        'nbf': now,
        'exp': now + timedelta(seconds=exp),
        'sub': sub,
    }
    token = jwt.encode(
        payload,
        jwt_secret,
        algorithm='HS256'
    )
    return token


def verify_password(
        plain_password: str,
        hashed_password: str,
):
    pwd_context = get_settings().PWD_CONTEXT
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(
        session: AsyncSession,
        phone: str,
        plain_password: str
) -> LoginResponse:
    stmt = select(User).where(User.phone == phone)
    result = await session.execute(stmt)
    user = result.scalar()
    settings = get_settings()
    if not user:
        raise Exception  # todo exeption

    if verify_password(plain_password, user.hashed_password):
        return LoginResponse(
            access_token=create_token(user.user_id, settings.ACCESS_TOKEN_EXPIRE_SECONDS, settings.SECRET_KEY),
            refresh_token=create_token(user.user_id, settings.REFRESH_TOKEN_EXPIRE_SECONDS, settings.SECRET_KEY)
        )
    else:
        raise Exception  # todo exeption
