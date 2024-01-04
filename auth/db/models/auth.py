from enum import Enum
from uuid import uuid4

from sqlalchemy.dialects.postgresql import ENUM, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from auth.db import DeclarativeBase


def _generate_uuid():
    return str(uuid4())


class UserType(Enum):
    individual = "Физическое лицо"
    legal = "Юридическое лицо"
    individual_entrepreneur = "Индивидуальный предприниматель"


class User(DeclarativeBase):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(
        VARCHAR(36), primary_key=True, default=_generate_uuid
    )
    email: Mapped[str] = mapped_column(VARCHAR(25), unique=True)
    phone: Mapped[str] = mapped_column(VARCHAR(12), unique=True)
    name: Mapped[str] = mapped_column(VARCHAR(24))
    surname: Mapped[str] = mapped_column(VARCHAR(24))
    hashed_password: Mapped[str] = mapped_column(VARCHAR(60))
    user_type: Mapped[Enum] = mapped_column(ENUM(UserType))
    is_verified: Mapped[bool] = mapped_column(default=False)

    def __str__(self):
        return f"user: {self.user_id}, phone: {self.phone}"
