"""add phone number

Revision ID: f3c27031d746
Revises: 4f2c7dcb4ed7
Create Date: 2024-03-19 12:58:08.991225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3c27031d746'
down_revision: Union[str, None] = '4f2c7dcb4ed7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Users", sa.Column("phone_number", sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("Users", "phone_number")
    pass
