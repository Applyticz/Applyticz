"""Added Outlook API model

Revision ID: 9042be62a9f2
Revises: 7db42c47b697
Create Date: 2024-11-05 21:41:17.223476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9042be62a9f2'
down_revision: Union[str, None] = '7db42c47b697'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'outlook_auth',
        sa.Column('id', sa.CHAR(36), primary_key=True, unique=True, nullable=False),
        sa.Column('user_id', sa.CHAR(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('access_token', sa.String(2048), nullable=False),
        sa.Column('refresh_token', sa.String(2048), nullable=False),
        sa.Column('token_expiry', sa.DateTime, nullable=False),
        sa.Column('scope', sa.String(512), nullable=True),
    )

def downgrade() -> None:
    op.drop_table('outlook_auth')

