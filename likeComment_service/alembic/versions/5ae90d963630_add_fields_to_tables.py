"""add fields to tables

Revision ID: 5ae90d963630
Revises: 65f2be32e66f
Create Date: 2024-10-04 07:58:05.582497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ae90d963630'
down_revision: Union[str, None] = '65f2be32e66f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
