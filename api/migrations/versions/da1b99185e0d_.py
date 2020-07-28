"""empty message

Revision ID: da1b99185e0d
Revises: 87697b31ecb8
Create Date: 2020-07-28 14:50:45.586909

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'da1b99185e0d'
down_revision = '87697b31ecb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gitdata', sa.Column('ref', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('gitdata', 'ref')
    # ### end Alembic commands ###
