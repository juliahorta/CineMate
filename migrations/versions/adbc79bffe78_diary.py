"""diary

Revision ID: adbc79bffe78
Revises: 2118a21acd7e
Create Date: 2021-04-08 12:08:29.373498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adbc79bffe78'
down_revision = '2118a21acd7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('diary', sa.Column('poster_path', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('diary', 'poster_path')
    # ### end Alembic commands ###