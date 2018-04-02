from extensions import db

import uuid
import datetime
from dateutil import parser
import enum

class Shift(enum.Enum):
    day = 'day'
    night = 'night'
    mid = 'mid'

class FacilityType(enum.Enum):
    hospital = 'hospital'
    extended_care = 'extended_care'
    long_term_care = 'long_term_care'

class ReporterType(enum.Enum):
    lpn = 'lpn'
    rn = 'rn'
    cna = 'cna'
    other = 'other'

class Whistle(db.Model):
    __tablename__ = 'whistles'

    id = db.Column(db.String(64), primary_key=True)
    hash = db.Column(db.String(33), nullable=False)
    report_date = db.Column(db.DateTime, nullable=False)
    shift = db.Column(db.Enum(Shift), nullable=False)
    facility_type = db.Column(db.Enum(FacilityType), nullable=False)
    district_state = db.Column(db.String, nullable=False)
    district = db.Column(db.Integer, nullable=False)
    reporter_type = db.Column(db.Enum(ReporterType), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, hash=None, report_date=None, shift=Shift.day,
                 facility_type=FacilityType.hospital,
                 district_state=None, district=None,
                 reporter_type=ReporterType.lpn, **kwargs):
        self.id = str(uuid.uuid4())
        if report_date is None:
            self.report_date = datetime.datetime.now().date()
        else:
            self.report_date = parser.parse(report_date).date()
        self.hash = hash
        self.shift = shift
        self.facility_type = facility_type
        self.district_state = district_state
        self.district = district
        self.reporter_type = reporter_type
        self.created_date = datetime.datetime.utcnow()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_simple_dict(self):
        data = self.as_dict();
        data.pop('id', None)
        data.pop('hash', None)
        data.pop('created_date', None)
        return data

