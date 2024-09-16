"""Initial migration

Revision ID: 7cbecb6602e4
Revises: 
Create Date: 2024-09-14 13:31:59.370333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '7cbecb6602e4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tests', 'id',
               existing_type=mysql.VARCHAR(length=32),
               type_=sa.CHAR(length=36),
               existing_nullable=False)
    op.alter_column('tests', 'username',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('tests', 'email',
               existing_type=mysql.VARCHAR(length=120),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('tests', 'password',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=255),
               nullable=True)
    op.create_index(op.f('ix_tests_id'), 'tests', ['id'], unique=False)
    op.create_unique_constraint(None, 'tests', ['username'])
    op.create_unique_constraint(None, 'tests', ['email'])
    op.add_column('users', sa.Column('username', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('email', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('password', sa.String(length=255), nullable=False))
    op.drop_index('id_UNIQUE', table_name='users')
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_unique_constraint(None, 'users', ['username'])
    op.create_unique_constraint(None, 'users', ['email'])
    op.drop_column('users', 'userscol')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('userscol', mysql.VARCHAR(length=45), nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.create_index('id_UNIQUE', 'users', ['id'], unique=True)
    op.drop_column('users', 'password')
    op.drop_column('users', 'email')
    op.drop_column('users', 'username')
    op.drop_constraint(None, 'tests', type_='unique')
    op.drop_constraint(None, 'tests', type_='unique')
    op.drop_index(op.f('ix_tests_id'), table_name='tests')
    op.alter_column('tests', 'password',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('tests', 'email',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=120),
               existing_nullable=False)
    op.alter_column('tests', 'username',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)
    op.alter_column('tests', 'id',
               existing_type=sa.CHAR(length=36),
               type_=mysql.VARCHAR(length=32),
               existing_nullable=False)
    # ### end Alembic commands ###