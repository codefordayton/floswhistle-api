import uuid
import random

from extensions import db
from controllers.database.whistle import Whistle, FacilityType

def get_state():
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
              'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
              'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
              'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
              'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    return states[random.randint(0, len(states) - 1)]

def get_district():
    districts = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
    return districts[random.randint(0, len(districts) - 1)]

def get_shift():
    shifts = ['day', 'night', 'mid']
    return shifts[random.randint(0, len(shifts) - 1)]

def get_facility_type():
    types = [FacilityType.hospital, FacilityType.extended_care, FacilityType.long_term_care]
    return types[random.randint(0, len(types) - 1)]

def get_type():
    types = ['lpn', 'rn', 'cna', 'other']
    return types[random.randint(0, len(types) - 1)]

def get_hash():
    return str(uuid.uuid4())[:32]

def load():

    for x in range(500):
        whistle = Whistle(hash=get_hash(), report_date=None,
                          shift=get_shift(), facility_type=get_facility_type(),
                          district_state=get_state(), district=get_district(),
                          reporter_type=get_type())
        db.session.add(whistle)
        db.session.commit()
