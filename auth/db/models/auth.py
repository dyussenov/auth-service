from uuid import uuid4

from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from auth.db import DeclarativeBase

def _generate_uuid():
    return str(uuid.uuid4())

class User(DeclarativeBase):
    user_id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True, default=_generate_uuid)
    email: Mapped[str] = mapped_column(VARCHAR(25), unique=True)
    phone: Mapped[str] = mapped_column(VARCHAR(12), unique=True)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(50))
    is_verified: Mappded[bool] = mapped_column(default=False)
