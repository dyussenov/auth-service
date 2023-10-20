from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '9fa0e4c22ade'
down_revision: Union[str, None] = 'd5b79879712f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        CREATE TYPE usertype AS ENUM ('individual', 'individual_entrepreneur', 'legal');
        CREATE TABLE users(
            user_id VARCHAR(36) PRIMARY KEY,
            email VARCHAR(25) NOT NULL UNIQUE,
            phone VARCHAR(12) NOT NULL UNIQUE,
            name VARCHAR(12) NOT NULL ,
            surname VARCHAR(12) NOT NULL,
            hashed_password VARCHAR(60) NOT NULL,
            is_verified BOOLEAN NOT NULL DEFAULT FALSE,
            user_type usertype
        );
        """
    )


def downgrade():
    op.drop_table("users")
