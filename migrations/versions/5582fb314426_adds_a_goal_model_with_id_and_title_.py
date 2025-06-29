"""Adds a Goal model with id and title attributes


Revision ID: 5582fb314426
Revises: 715a63be17d0
Create Date: 2025-05-16 11:58:12.943036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5582fb314426'
down_revision = '715a63be17d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
