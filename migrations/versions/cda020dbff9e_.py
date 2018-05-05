"""empty message

Revision ID: cda020dbff9e
Revises: 313316215b1a
Create Date: 2018-05-05 13:37:58.119017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cda020dbff9e'
down_revision = '313316215b1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('request_photo_key', 'request', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('request_photo_key', 'request', ['photo'])
    # ### end Alembic commands ###