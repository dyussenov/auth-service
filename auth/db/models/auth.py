from uuid import uuid4

from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from auth.db import DeclarativeBase


def _generate_uuid():
    return str(uuid4())


class User(DeclarativeBase):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(VARCHAR(36),primary_key=True, default=_generate_uuid)
    email: Mapped[str] = mapped_column(VARCHAR(25), unique=True)
    phone: Mapped[str] = mapped_column(VARCHAR(12), unique=True)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(60))
    is_verified: Mapped[bool] = mapped_column(default=False)
