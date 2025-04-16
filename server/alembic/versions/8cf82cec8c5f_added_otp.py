"""added otp

Revision ID: 8cf82cec8c5f
Revises: 2a956c6e0a1c
Create Date: 2025-04-16 03:44:59.848019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cf82cec8c5f'
down_revision: Union[str, None] = '2a956c6e0a1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('otps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('usage', sa.Enum('LOGIN', 'PASSWORD_RESET', 'EMAIL_VERIFICATION', name='otpusage'), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'VERIFIED', 'EXPIRED', name='otpstatus'), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_otps_code'), 'otps', ['code'], unique=True)
    op.create_index(op.f('ix_otps_email'), 'otps', ['email'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_otps_email'), table_name='otps')
    op.drop_index(op.f('ix_otps_code'), table_name='otps')
    op.drop_table('otps')
    # ### end Alembic commands ###
