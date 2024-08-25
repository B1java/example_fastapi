"""add content column to posts table

Revision ID: 1d8baaa3e023
Revises: 36d1bfa0fa5f
Create Date: 2024-08-19 15:11:28.147637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d8baaa3e023'
down_revision: Union[str, None] = '36d1bfa0fa5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
