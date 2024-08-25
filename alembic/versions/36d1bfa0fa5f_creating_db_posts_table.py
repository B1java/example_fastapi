"""Creating DB posts table

Revision ID: 36d1bfa0fa5f
Revises: 
Create Date: 2024-08-19 14:52:04.825225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36d1bfa0fa5f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(),nullable=False, primary_key=True),
                    sa.Column('title', sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
    