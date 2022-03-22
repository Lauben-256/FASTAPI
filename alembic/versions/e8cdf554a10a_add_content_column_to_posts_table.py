"""add content column to posts table

Revision ID: e8cdf554a10a
Revises: 68e8d9a319a0
Create Date: 2022-03-22 22:15:55.146228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8cdf554a10a'
down_revision = '68e8d9a319a0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
