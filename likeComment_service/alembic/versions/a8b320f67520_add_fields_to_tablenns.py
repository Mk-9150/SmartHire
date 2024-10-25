"""add fields to tablenns

Revision ID: a8b320f67520
Revises: 5ae90d963630
Create Date: 2024-10-04 08:00:19.792594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8b320f67520'
down_revision: Union[str, None] = '5ae90d963630'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
