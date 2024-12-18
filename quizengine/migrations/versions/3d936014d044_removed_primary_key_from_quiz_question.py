"""Removed primary key from quiz question

Revision ID: 3d936014d044
Revises: 20fc254e190b
Create Date: 2024-06-03 18:47:06.685429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3d936014d044'
down_revision: Union[str, None] = '20fc254e190b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quizquestion', 'updated_at')
    op.drop_column('quizquestion', 'id')
    op.drop_column('quizquestion', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quizquestion', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('quizquestion', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('quizquestion', sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
