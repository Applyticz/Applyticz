"""Add email and application columns

Revision ID: ee825eb4543e
Revises: 9042be62a9f2
Create Date: 2024-11-12 17:22:03.762837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ee825eb4543e'
down_revision: Union[str, None] = '9042be62a9f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('applications', sa.Column('status_history', sa.JSON(), nullable=False))
    op.add_column('applications', sa.Column('interview_notes', sa.String(length=1000), nullable=True))
    op.add_column('applications', sa.Column('interview_dates', sa.String(length=255), nullable=True))
    op.add_column('applications', sa.Column('interview_round', sa.String(length=255), nullable=True))
    op.add_column('applications', sa.Column('is_active_interview', sa.Boolean(), nullable=False))
    op.add_column('applications', sa.Column('offer_notes', sa.String(length=1000), nullable=True))
    op.add_column('applications', sa.Column('offer_interest', sa.Integer(), nullable=True))
    op.add_column('applications', sa.Column('is_active_offer', sa.Boolean(), nullable=False))
    op.add_column('emails', sa.Column('app', sa.CHAR(length=36), nullable=False))
    op.add_column('emails', sa.Column('body_preview', sa.String(length=255), nullable=False))
    op.alter_column('emails', 'status',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.create_foreign_key(None, 'emails', 'applications', ['app'], ['id'])
    op.drop_column('emails', 'position')
    op.drop_column('emails', 'company')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('emails', sa.Column('company', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('emails', sa.Column('position', mysql.VARCHAR(length=255), nullable=True))
    op.drop_constraint(None, 'emails', type_='foreignkey')
    op.alter_column('emails', 'status',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.drop_column('emails', 'body_preview')
    op.drop_column('emails', 'app')
    op.drop_column('applications', 'is_active_offer')
    op.drop_column('applications', 'offer_interest')
    op.drop_column('applications', 'offer_notes')
    op.drop_column('applications', 'is_active_interview')
    op.drop_column('applications', 'interview_round')
    op.drop_column('applications', 'interview_dates')
    op.drop_column('applications', 'interview_notes')
    op.drop_column('applications', 'status_history')
    # ### end Alembic commands ###
