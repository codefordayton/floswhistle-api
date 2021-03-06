"""empty message

Revision ID: c929b4d8fe16
Revises: 
Create Date: 2018-03-27 20:02:55.736662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c929b4d8fe16'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('whistles',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('hash', sa.String(length=33), nullable=False),
    sa.Column('report_date', sa.DateTime(), nullable=False),
    sa.Column('shift', sa.Enum('day', 'night', 'mid', name='shift'), nullable=False),
    sa.Column('facility_type', sa.Enum('hospital', 'extended_care', name='facilitytype'), nullable=False),
    sa.Column('district_state', sa.String(), nullable=False),
    sa.Column('district', sa.Integer(), nullable=False),
    sa.Column('reporter_type', sa.String(), nullable=True),
    sa.Column('reporter_type', sa.Enum('lpn', 'rn', 'cna', 'other', name='reporter_type'), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('whistles')
    # ### end Alembic commands ###
