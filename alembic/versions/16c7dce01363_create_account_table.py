"""create account table

Revision ID: 16c7dce01363
Revises: 
Create Date: 2021-09-08 12:04:06.244908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16c7dce01363'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, unique=True),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('password', sa.String(50), nullable=False)
    )


def downgrade():
    op.drop_table('users')
