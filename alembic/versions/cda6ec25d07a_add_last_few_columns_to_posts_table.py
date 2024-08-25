"""add last few columns to posts table

Revision ID: cda6ec25d07a
Revises: 036b16e8100b
Create Date: 2024-08-20 19:31:20.590030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cda6ec25d07a'
down_revision: Union[str, None] = '036b16e8100b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('posts', sa.Column('published', sa.Boolean(),nullable=False, server_default='TRUE'))


def downgrade() -> None:
    op.drop_column('posts','created_at')
    op.drop_column('posts','published')
