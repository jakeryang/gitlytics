"""empty message

Revision ID: 353c8ed27896
Revises: 9a25f78d4c9c
Create Date: 2020-07-22 15:00:03.497328

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '353c8ed27896'
down_revision = '9a25f78d4c9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flask_dance_oauth')
    op.add_column('repos', sa.Column('name', sa.Text(), nullable=True))
    op.drop_constraint('repos_url_key', 'repos', type_='unique')
    op.create_unique_constraint(None, 'repos', ['name'])
    op.drop_column('repos', 'url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('repos', sa.Column('url', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'repos', type_='unique')
    op.create_unique_constraint('repos_url_key', 'repos', ['url'])
    op.drop_column('repos', 'name')
    op.create_table('flask_dance_oauth',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('provider', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('token', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='flask_dance_oauth_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='flask_dance_oauth_pkey')
    )
    # ### end Alembic commands ###
