"""empty message

Revision ID: 818b53b95cbd
Revises: 9b43a553ea1f
Create Date: 2018-04-08 19:34:51.681861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '818b53b95cbd'
down_revision = '9b43a553ea1f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('whistles')
    op.execute("DROP TYPE shift;")
    op.execute("DROP TYPE facilitytype;")
    op.execute("DROP TYPE reporter_type;")
    op.create_table('whistles',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('hash', sa.String(length=33), nullable=False),
    sa.Column('report_date', sa.DateTime(), nullable=False),
    sa.Column('shift', sa.Enum('day', 'night', 'mid', name='shift_type'), nullable=False),
    sa.Column('facility_type', sa.Enum('hospital', 'extended_care', 'long_term_care', name='facilitytype2'), nullable=False),
    sa.Column('district_state', sa.String(), nullable=False),
    sa.Column('district', sa.Integer(), nullable=False),
    sa.Column('reporter_type', sa.String(), nullable=True),
    sa.Column('reporter_type', sa.Enum('lpn', 'rn', 'cna', 'other', name='reportertype'), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
    pass


def downgrade():
    pass
