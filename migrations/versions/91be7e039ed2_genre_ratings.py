"""genre ratings

Revision ID: 91be7e039ed2
Revises: 53d0a3a0e86e
Create Date: 2021-03-30 13:19:56.130318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91be7e039ed2'
down_revision = '53d0a3a0e86e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genre_ratings',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('action', sa.Integer(), nullable=True),
    sa.Column('adventure', sa.Integer(), nullable=True),
    sa.Column('animation', sa.Integer(), nullable=True),
    sa.Column('comedy', sa.Integer(), nullable=True),
    sa.Column('crime', sa.Integer(), nullable=True),
    sa.Column('documentary', sa.Integer(), nullable=True),
    sa.Column('drama', sa.Integer(), nullable=True),
    sa.Column('family', sa.Integer(), nullable=True),
    sa.Column('fantasy', sa.Integer(), nullable=True),
    sa.Column('history', sa.Integer(), nullable=True),
    sa.Column('horror', sa.Integer(), nullable=True),
    sa.Column('music', sa.Integer(), nullable=True),
    sa.Column('mystery', sa.Integer(), nullable=True),
    sa.Column('romance', sa.Integer(), nullable=True),
    sa.Column('sci-fi', sa.Integer(), nullable=True),
    sa.Column('thriller', sa.Integer(), nullable=True),
    sa.Column('war', sa.Integer(), nullable=True),
    sa.Column('western', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genre_ratings')
    # ### end Alembic commands ###
