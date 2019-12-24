"""empty message

Revision ID: d861b05458c5
Revises: 7207845adf6c
Create Date: 2019-12-22 23:50:45.029850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd861b05458c5'
down_revision = '7207845adf6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('done_status', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'done_status')
    # ### end Alembic commands ###