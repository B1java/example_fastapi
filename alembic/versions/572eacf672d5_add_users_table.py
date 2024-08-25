"""add users table

Revision ID: 572eacf672d5
Revises: 1d8baaa3e023
Create Date: 2024-08-20 14:43:27.726711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '572eacf672d5'
down_revision: Union[str, None] = '1d8baaa3e023'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(),primary_key=True, nullable=False), 
                    sa.Column('password', sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()')),
                    sa.Column('email',sa.String,nullable=False, unique=True))


def downgrade() -> None:
    op.drop_table('users')
