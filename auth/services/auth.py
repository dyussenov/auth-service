from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from auth.db.models import User
from auth.schemas import SignupRequest
from auth.config import get_settings

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


def verify_password(
    plain_password: str,
    hashed_password: str,
):
    pwd_context = get_settings().PWD_CONTEXT
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(

):
    pass
