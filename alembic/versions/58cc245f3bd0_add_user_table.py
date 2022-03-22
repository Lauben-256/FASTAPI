"""Add user table

Revision ID: 58cc245f3bd0
Revises: e8cdf554a10a
Create Date: 2022-03-22 22:20:45.801902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58cc245f3bd0'
down_revision = 'e8cdf554a10a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
