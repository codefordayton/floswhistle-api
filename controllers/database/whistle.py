from extensions import db
from sqlalchemy.sql import func

import uuid
from dateutil import parser
from datetime import datetime, timedelta
import enum

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
    facility_type = db.Column(db.Enum(FacilityType), nullable=False)
    district_state = db.Column(db.String, nullable=False)
    district = db.Column(db.Integer, nullable=False)
    reporter_type = db.Column(db.Enum(ReporterType), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, hash=None, report_date=None,
                 facility_type=FacilityType.hospital,
                 district_state=None, district=None,
                 start_date=None, end_date=None,
                 reporter_type=ReporterType.lpn, **kwargs):
        self.id = str(uuid.uuid4())
        if start_date is None:
            self.start_date = datetime.now()
        else:
            # self.start_date = parser.parse(start_date)
            self.start_date = datetime.fromtimestamp(start_date)
        if end_date is None:
            self.end_date = datetime.now()
        else:
            # self.end_date = parser.parse(end_date)
            self.end_date = datetime.fromtimestamp(end_date)
        self.hash = hash
        self.facility_type = facility_type
        self.district_state = district_state
        self.district = district
        self.reporter_type = reporter_type
        self.created_date = datetime.utcnow()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_simple_dict(self):
        data = self.as_dict();
        data.pop('id', None)
        data.pop('hash', None)
        data.pop('created_date', None)
        return data
