"""empty message

Revision ID: df1b7dba0b01
Revises: 52b9eb053a78
Create Date: 2020-04-30 18:32:25.084149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df1b7dba0b01'
down_revision = '52b9eb053a78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pandemic_whistles', 'test_no_result',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('pandemic_whistles', 'test_none',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('pandemic_whistles', 'test_tried',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pandemic_whistles', 'test_tried',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('pandemic_whistles', 'test_none',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('pandemic_whistles', 'test_no_result',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###