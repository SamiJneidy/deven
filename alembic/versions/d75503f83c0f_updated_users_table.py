"""Updated users table

Revision ID: d75503f83c0f
Revises: aa7e184eaecd
Create Date: 2025-04-13 23:07:16.522339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd75503f83c0f'
down_revision: Union[str, None] = 'aa7e184eaecd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('users', 'status_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'status_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
