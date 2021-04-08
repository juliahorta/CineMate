"""diary

Revision ID: 689d61b3fb2a
Revises: 760f4c19e756
Create Date: 2021-04-08 11:35:28.176711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '689d61b3fb2a'
down_revision = '760f4c19e756'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('diary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_watched', sa.String(length=140), nullable=True),
    sa.Column('movie_name', sa.String(length=200), nullable=True),
    sa.Column('movie_id', sa.String(length=200), nullable=True),
    sa.Column('release_date', sa.String(length=140), nullable=True),
    sa.Column('user_rating', sa.String(length=140), nullable=True),
    sa.Column('rewatch', sa.Boolean(create_constraint=False), nullable=True),
    sa.Column('review', sa.String(length=140), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('diary')
    # ### end Alembic commands ###
