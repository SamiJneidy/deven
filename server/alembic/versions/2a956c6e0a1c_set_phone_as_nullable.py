"""set phone as nullable

Revision ID: 2a956c6e0a1c
Revises: d75503f83c0f
Create Date: 2025-04-15 00:51:32.496514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a956c6e0a1c'
down_revision: Union[str, None] = 'd75503f83c0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
