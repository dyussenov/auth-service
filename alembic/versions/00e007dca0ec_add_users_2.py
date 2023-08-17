"""add users 2

Revision ID: 00e007dca0ec
Revises: 0d2e42eb0cd6
Create Date: 2023-08-16 15:29:22.291989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00e007dca0ec'
down_revision: Union[str, None] = '0d2e42eb0cd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.String(length=36), primary_key=True),
        sa.Column('email', sa.String(length=25), nullable=False, unique=True),
        sa.Column('phone', sa.String(length=12), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=60), nullable=False),
        sa.Column('is_verified', sa.Boolean(), server_default=sa.false(), nullable=False),
    )

def downgrade():
    op.drop_table('users')