"""add created at

Revision ID: 8c1a853c2510
Revises: 9fa0e4c22ade
Create Date: 2024-01-05 11:19:17.100469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8c1a853c2510'
down_revision: Union[str, None] = '9fa0e4c22ade'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE users
        ADD COLUMN created_at TIMESTAMP;
        ALTER TABLE users
        ADD COLUMN updated_at TIMESTAMP;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE users
        DROP COLUMN created_at;
        ALTER TABLE users
        DROP COLUMN updated_at;
        """
    )
    # ### end Alembic commands ###
