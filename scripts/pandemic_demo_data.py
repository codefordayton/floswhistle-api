import uuid
import random
from datetime import datetime, timedelta

from extensions import db
from controllers.database.whistle import FacilityType, ReporterType
from controllers.database.pandemic_whistle import PandemicWhistle

def get_state():
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
              'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
              'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
              'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
              'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    return states[random.randint(0, len(states) - 1)]

def get_district_by_state(state):
    districts_by_state = { 
        'AL': 7, 'AK': 1, 'AZ': 9, 'AR': 4, 'CA': 53,
        'CO': 7, 'CT': 5, 'DE': 1, 'FL': 27, 'GA': 14,
        'HI': 2, 'ID': 2, 'IL': 18, 'IN': 9, 'IA': 4,
        'KS': 4, 'KY': 6, 'LA': 6, 'ME': 2, 'MD': 8,
        'MA': 9, 'MI': 14, 'MN': 8, 'MS': 4, 'MO': 8,
        'MT': 1, 'NE': 3, 'NV': 4, 'NH': 2, 'NJ': 12,
        'NM': 3, 'NY': 27, 'NC': 13, 'ND': 1, 'OH': 16,
        'OK': 5, 'OR': 5, 'PA': 18, 'RI': 2, 'SC': 7,
        'SD': 1, 'TN': 9, 'TX': 36, 'UT': 4, 'VT': 1,
        'VA': 11, 'WA': 10, 'WV': 3, 'WI': 8, 'WY': 1
    }
    return random.randint(1, districts_by_state.get(state, 1))

def get_facility_type():
    types = [
        FacilityType.pre_hospital,
        FacilityType.hospital,
        FacilityType.nursing_home,
        FacilityType.er,
        FacilityType.urgent_care
    ]
    return types[random.randint(0, len(types) - 1)]

def get_reporter_type():
    types = [
        ReporterType.emt,
        ReporterType.paramedic,
        ReporterType.rn,
        ReporterType.apn,
        ReporterType.lpn,
        ReporterType.cna,
        ReporterType.rt,
        ReporterType.physician,
        ReporterType.pa]
    return types[random.randint(0, len(types) - 1)]

def get_hash():
    return 'demo' + str(uuid.uuid4())[:24]

def get_reported_date():
    days_removed = random.randint(0, 60)
    today = datetime.today()
    just_today = datetime(today.year, today.month, today.day)
    return int((just_today - timedelta(days=days_removed)).timestamp())

def get_willing():
    return random.randint(0, 2)

def get_shortages():
    shortages = {}

    # get number we should try to get
    shortage_count = random.randint(0,5)
    options = [
        'surgical_masks', 'n95_masks', 'papr_hoods',
        'non_sterile_gloves', 'isolation_gowns', 'face_shields',
        'oxygen', 'sedatives', 'narcotic_analgesics',
        'paralytics', 'icu_beds', 'icu_trained_nurses', 'ventilators'
    ]

    for x in range(shortage_count):
        shortages[options[random.randint(0, len(options) - 1)]] = True

    return shortages

def get_testing():
    testing = {}

    # has no result option
    if random.choice([True, False]):
        value = random.choice(['test_none', 'test_tried', 'test_no_result'])
        testing[value] = True
    else:
        # has swab test
        if random.choice([True, False]):
            value = random.choice(['test_swab_neg', 'test_swab_pos'])
            testing[value] = True

        # has antibody test
        if random.choice([True, False]):
            value = random.choice(['test_anti_neg', 'test_anti_pos'])
            testing[value] = True
    
    return testing

def load():
    db.session.query(PandemicWhistle).filter(
        PandemicWhistle.hash.like('demo%')
    ).delete(synchronize_session=False)
    db.session.commit()

    for x in range(500):
        state = get_state()
        data = {
            'hash': get_hash(),
            'facility_type': get_facility_type(),
            'reporter_type': get_reporter_type(),
            'district_state': state,
            'district': get_district_by_state(state),
            'reported_date': get_reported_date(),
            'willing_to_report': get_willing()
        }
        data.update(get_shortages())
        data.update(get_testing())
        report = PandemicWhistle(**data)
        db.session.add(report)
        db.session.commit()
