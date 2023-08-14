"""add true users

Revision ID: b02849ea451d
Revises: 78894385c1bd
Create Date: 2023-08-14 15:39:57.630105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b02849ea451d'
down_revision = '78894385c1bd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.String(length=36), primary_key=True),
        sa.Column('email', sa.String(length=25), unique=True, nullable=False),
        sa.Column('phone', sa.String(length=12), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(length=50), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='0')
    )

def downgrade():
    op.drop_table('users')