"""empty message

Revision ID: d5b5a012ba7e
Revises: cda020dbff9e
Create Date: 2018-05-05 16:30:49.857354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5b5a012ba7e'
down_revision = 'cda020dbff9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('request', 'photo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('photo', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
