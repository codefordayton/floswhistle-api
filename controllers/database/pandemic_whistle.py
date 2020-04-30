from extensions import db
from sqlalchemy.sql import func
from .whistle import ReporterType, FacilityType

import uuid
from dateutil import parser
from datetime import datetime, timedelta
import enum

class PandemicWhistle(db.Model):
    __tablename__ = 'pandemic_whistles'

    id = db.Column(db.String(64), primary_key=True)
    hash = db.Column(db.String(33), nullable=False)
    facility_type = db.Column(db.Enum(FacilityType), nullable=False)
    district_state = db.Column(db.String, nullable=False)
    district = db.Column(db.Integer, nullable=False)
    reporter_type = db.Column(db.Enum(ReporterType), nullable=False)
    reported_date = db.Column(db.DateTime, nullable=False)
    surgical_masks = db.Column(db.Boolean, default=False, nullable=False)
    n95_masks = db.Column(db.Boolean, default=False, nullable=False)
    papr_hoods = db.Column(db.Boolean, default=False, nullable=False)
    non_sterile_gloves = db.Column(db.Boolean, default=False, nullable=False)
    isolation_gowns = db.Column(db.Boolean, default=False, nullable=False)
    face_shields = db.Column(db.Boolean, default=False, nullable=False)
    oxygen = db.Column(db.Boolean, default=False, nullable=False)
    sedatives = db.Column(db.Boolean, default=False, nullable=False)
    narcotic_analgesics = db.Column(db.Boolean, default=False, nullable=False)
    paralytics = db.Column(db.Boolean, default=False, nullable=False)
    icu_beds = db.Column(db.Boolean, default=False, nullable=False)
    icu_trained_nurses = db.Column(db.Boolean, default=False, nullable=False)
    ventilators = db.Column(db.Boolean, default=False, nullable=False)
    test_none = db.Column(db.Boolean, nullable=True)
    test_tried = db.Column(db.Boolean, nullable=True)
    test_no_result = db.Column(db.Boolean, nullable=True)
    test_swab_neg = db.Column(db.Boolean, nullable=True)
    test_swab_pos = db.Column(db.Boolean, nullable=True)
    test_anti_neg = db.Column(db.Boolean, nullable=True)
    test_anti_pos = db.Column(db.Boolean, nullable=True)
    willing_to_report = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String(1024), nullable=True)

    created_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, hash=None, report_date=None,
                 facility_type=FacilityType.hospital,
                 district_state=None, district=None,
                 reported_date=None, reporter_type=ReporterType.lpn,
                 surgical_masks=False, n95_masks=False,
                 papr_hoods=False, non_sterile_gloves=False,
                 isolation_gowns=False, face_shields=False,
                 oxygen=False, sedatives=False,
                 narcotic_analgesics=False, paralytics=False,
                 icu_beds=False, icu_trained_nurses=False,
                 ventilators=False, test_none=None, test_tried=None,
                 test_no_result=None, test_swab_neg=None,
                 test_swab_pos=None, test_anti_neg=None,
                 test_anti_pos=None, willing_to_report=None,
                 comment=None, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_date = datetime.utcnow()

        if reported_date is None:
            self.reported_date = datetime.now()
        else:
            self.reported_date = datetime.fromtimestamp(int(float(reported_date)))
        self.hash = hash
        self.facility_type = facility_type
        self.district_state = district_state
        self.district = district
        self.reporter_type = reporter_type

        self.surgical_masks = surgical_masks
        self.n95_masks = n95_masks
        self.papr_hoods = papr_hoods
        self.non_sterile_gloves = non_sterile_gloves
        self.isolation_gowns = isolation_gowns
        self.face_shields = face_shields
        self.oxygen = oxygen
        self.sedatives = sedatives
        self.narcotic_analgesics = narcotic_analgesics
        self.paralytics = paralytics
        self.icu_beds = icu_beds
        self.icu_trained_nurses = icu_trained_nurses
        self.ventilators = ventilators
        self.test_none= test_none
        self.test_tried = test_tried
        self.test_no_result = test_no_result
        self.test_swab_neg = test_swab_neg
        self.test_swab_pos = test_swab_pos
        self.test_anti_neg = test_anti_neg
        self.test_anti_pos = test_anti_pos
        self.willing_to_report = willing_to_report
        self.comment = comment

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_simple_dict(self):
        return {
            'reported_date': self.reported_date,
            'allIds': ['facility', 'reporter', 'shortages', 'test_data'],
            'facility': {
                'district': self.district,
                'district_state': self.district_state,
                'facility_type': self.facility_type
            },
            'reporter': {
                'reporter_type': self.reporter_type,
                'willing_to_report': self.willing_to_report
            },
            'shortages': {
                'icu_beds': self.icu_beds,
                'face_shields': self.face_shields,
                'icu_trained_nurses': self.icu_trained_nurses,
                'isolation_gowns': self.isolation_gowns,
                'n95_masks': self.n95_masks,
                'narcotic_analgesics': self.narcotic_analgesics,
                'non_sterile_gloves': self.non_sterile_gloves,
                'oxygen': self.oxygen,
                'papr_hoods': self.papr_hoods,
                'paralytics': self.paralytics,
                'sedatives': self.sedatives,
                'surgical_masks': self.surgical_masks,
                'ventilators': self.ventilators
            },
            'test_data': {
                'test_none': self.test_none,
                'test_tried': self.test_tried,
                'test_no_result': self.test_no_result,
                'test_results': {
                    'test_anti_neg': self.test_anti_neg,
                    'test_anti_pos': self.test_anti_pos,
                    'test_swab_neg': self.test_swab_neg,
                    'test_swab_pos': self.test_swab_pos
                }
            }
        }
        # data = self.as_dict();
        # data.pop('id', None)
        # data.pop('hash', None)
        # data.pop('created_date', None)
        # return data
