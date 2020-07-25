"""empty message

Revision ID: 10d102686be3
Revises: 18f4e883f1d4
Create Date: 2020-07-24 19:19:24.824397

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '10d102686be3'
down_revision = '18f4e883f1d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('repos', 'webhook_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('repos', 'webhook_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
