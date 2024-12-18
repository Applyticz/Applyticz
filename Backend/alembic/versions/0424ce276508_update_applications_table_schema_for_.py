"""Update applications table schema for applied dates

Revision ID: 0424ce276508
Revises: 7611e616ed87
Create Date: 2024-11-19 23:14:04.863370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '0424ce276508'
down_revision: Union[str, None] = '7611e616ed87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('applications', 'interview_dates',
               existing_type=mysql.JSON(),
               type_=sa.Date(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('applications', 'interview_dates',
               existing_type=sa.Date(),
               type_=mysql.JSON(),
               existing_nullable=True)
    # ### end Alembic commands ###
