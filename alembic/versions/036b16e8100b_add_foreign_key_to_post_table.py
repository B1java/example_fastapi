"""add foreign key to post table

Revision ID: 036b16e8100b
Revises: 572eacf672d5
Create Date: 2024-08-20 18:27:29.926805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '036b16e8100b'
down_revision: Union[str, None] = '572eacf672d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fk", source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')



def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
