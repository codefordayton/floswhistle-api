"""empty message

Revision ID: ecacbc24e19a
Revises: bde2607caa38
Create Date: 2020-04-23 20:57:02.655429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecacbc24e19a'
down_revision = 'bde2607caa38'
branch_labels = None
depends_on = None

old_facility = ('hospital', 'extended_care', 'long_term_care')
new_facility = ('hospital', 'extended_care', 'long_term_care', 'pre_hospital', 'nursing_home', 'er', 'urgent_care')
old_facility_type = sa.Enum(*old_facility, name='facilitytype')
new_facility_type = sa.Enum(*new_facility, name='facilitytype')
tmp_facility_type = sa.Enum(*new_facility, name='_facilitytype')

old_reporter = ('lpn', 'rn', 'cna', 'other')
new_reporter = ('lpn', 'rn', 'cna', 'other', 'emt', 'paramedic', 'apn', 'rt', 'physician', 'pa')
old_reporter_type = sa.Enum(*old_reporter, name='reportertype')
new_reporter_type = sa.Enum(*new_reporter, name='reportertype')
tmp_reporter_type = sa.Enum(*new_reporter, name='_reportertype')

def upgrade():
    tmp_facility_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE pandemic_whistles ALTER COLUMN facility_type TYPE _facilitytype'
               ' USING facility_type::text::_facilitytype')
    op.execute('ALTER TABLE whistles ALTER COLUMN facility_type TYPE _facilitytype'
               ' USING facility_type::text::_facilitytype')
    old_facility_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" type type
    new_facility_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE pandemic_whistles ALTER COLUMN facility_type TYPE facilitytype'
               ' USING facility_type::text::facilitytype')
    op.execute('ALTER TABLE whistles ALTER COLUMN facility_type TYPE facilitytype'
               ' USING facility_type::text::facilitytype')
    tmp_facility_type.drop(op.get_bind(), checkfirst=False)

    tmp_reporter_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE pandemic_whistles ALTER COLUMN reporter_type TYPE _reportertype'
               ' USING reporter_type::text::_reportertype')
    op.execute('ALTER TABLE whistles ALTER COLUMN reporter_type TYPE _reportertype'
               ' USING reporter_type::text::_reportertype')
    old_reporter_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" type type
    new_reporter_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE pandemic_whistles ALTER COLUMN reporter_type TYPE reportertype'
               ' USING reporter_type::text::reportertype')
    op.execute('ALTER TABLE whistles ALTER COLUMN reporter_type TYPE reportertype'
               ' USING reporter_type::text::reportertype')
    tmp_reporter_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    tmp_facility_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE pandemic_whistles ALTER COLUMN facility_type TYPE _facilitytype'
               ' USING facility_type::text::_facilitytype')
    op.execute('ALTER TABLE whistles ALTER COLUMN facility_type TYPE _facilitytype'
               ' USING facility_type::text::_facilitytype')
    new_facility_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "old" type type
    old_facility_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE pandemic_whistles ALTER COLUMN facility_type TYPE facilitytype'
               ' USING facility_type::text::facilitytype')
    op.execute('ALTER TABLE whistles ALTER COLUMN facility_type TYPE facilitytype'
               ' USING facility_type::text::facilitytype')
    tmp_facility_type.drop(op.get_bind(), checkfirst=False)

    tmp_reporter_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE pandemic_whistles ALTER COLUMN reporter_type TYPE _reportertype'
               ' USING reporter_type::text::_reportertype')
    op.execute('ALTER TABLE whistles ALTER COLUMN reporter_type TYPE _reportertype'
               ' USING reporter_type::text::_reportertype')
    new_reporter_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "old" type type
    old_reporter_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE pandemic_whistles ALTER COLUMN reporter_type TYPE reportertype'
               ' USING reporter_type::text::reportertype')
    op.execute('ALTER TABLE whistles ALTER COLUMN reporter_type TYPE reportertype'
               ' USING reporter_type::text::reportertype')
    tmp_reporter_type.drop(op.get_bind(), checkfirst=False)
