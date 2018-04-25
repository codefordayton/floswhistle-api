import hashlib
from datetime import datetime, timedelta
from dateutil import parser
import random
import requests
from enum import Enum
from flask import Flask, Blueprint, request, Response, json
from extensions import cors, db, migrate
from controllers.database.whistle import Whistle
from controllers.database.zip import Zip

try:
    from config import ProdConfig
except ImportError:
    from testconfig import TestConfig as ProdConfig

api_blueprint = Blueprint('api', __name__, url_prefix='/v1')

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return str(obj.value)
        return json.JSONEncoder.default(self, obj)

def create_app(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    app.register_blueprint(api_blueprint)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return app

def is_valid(data):
    valid = True

    if data is None: # Bozo filter
        return False

    zip = data.get('zip')
    if not zip:
        valid = False
    
    # Is the date to be reported in the last two?
    start_date = data.get('start_date')
    if start_date:
        time_window = datetime.utcnow() - timedelta(days=2)
        started_date = parser.parse(start_date)
        if started_date < time_window:
            valid = False

    return valid

def generate_hash(request):
    user_string = request.headers.get('User-Agent', 'unknown')
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    input = ip + ' ' + user_string
    return hashlib.md5(input.encode()).hexdigest()

def is_unique(hash, start_date):
    time_window = datetime.utcnow() - timedelta(hours=12)
    if start_date:
        started_date = parser.parse(start_date).date()
    else:
        started_date = datetime.utcnow().date()  

    existing = Whistle.query.filter(
        Whistle.hash == hash,
        Whistle.created_date > time_window).all()

    # return existing is None
    return len(existing) == 0

def get_zip_district(zip):
    zips = Zip.query.filter(Zip.zip == zip).all()
    weights = [z.factor for z in zips]
    return random.choices(zips, weights=weights)

@api_blueprint.route('/whistle', methods=['POST'])
def create_whistle():
    resp = {}

    # check that the request is valid
    if not is_valid(request.json):
        return Response(json.dumps({'error': 'Invalid request'}),
                        mimetype='application/json', status=400)

    # check that we haven't seen this user in 12 hours
    user_hash = generate_hash(request)
    if not is_unique(user_hash, request.json.get('start_date')):
        return Response(json.dumps({'error': 'Too many requests'}),
                        mimetype='application/json', status=400)

    zip_district = get_zip_district(request.json['zip'])[0]
    # add whistle
    whistle = Whistle(hash=user_hash, district=zip_district.district,
                      district_state=zip_district.state, **request.json)
    db.session.add(whistle)
    db.session.commit()

    return Response(json.dumps(whistle.as_dict(), cls=EnumEncoder),
                    mimetype='application/json')

@api_blueprint.route('/data', methods=['GET'])
def get_data():
    resp = {}
    # TODO: This is gross.
    rows = db.engine.execute("""
        select
            district_state,
            district,
            (select count(*) from whistles where district_state = w.district_state and 
                                                 district = w.district) as total_count,
            (select count(*) from whistles where reporter_type='lpn' and 
                                                 district_state = w.district_state and 
                                                 district = w.district) as lpn_count,
            (select count(*) from whistles where reporter_type='rn' and 
                                                 district_state = w.district_state and 
                                                 district = w.district) as rn_count,
            (select count(*) from whistles where reporter_type='cna' and 
                                                 district_state = w.district_state and 
                                                 district = w.district) as cna_count,
            (select count(*) from whistles where reporter_type='other' and 
                                                 district_state = w.district_state and 
                                                 district = w.district) as other_count,
            (select count(*) from whistles where facility_type = 'hospital' and
                                                 district_state = w.district_state and 
                                                 district = w.district) as hospital_count,
            (select count(*) from whistles where facility_type = 'extended_care' and
                                                 district_state = w.district_state and 
                                                 district = w.district) as extended_count,
            (select count(*) from whistles where facility_type = 'long_term_care' and
                                                 district_state = w.district_state and 
                                                 district = w.district) as long_count
        from whistles w
        group by district_state, district;
    """)
    # whistle_objs = { 'start_date': '4/1/2018', 'end_date': '4/2/2018', 'states': {} }
    whistle_objs = { 'states': {} }
    for row in rows:
        if row['district_state'] not in whistle_objs['states']:
            whistle_objs['states'][row['district_state']] = {}
        whistle_objs['states'][row['district_state']]["%02d" % row['district']] = {
            'type': { 'total': row['total_count'],
                'lpn': row['lpn_count'],
                'rn': row['rn_count'],
                'cna': row['cna_count'],
                'other': row['other_count']
            }, 'facility_type': {
                'hospital': row['hospital_count'],
                'extended_care': row['extended_count'],
                'long_term_care': row['long_count']
            }
        }

    return Response(json.dumps(whistle_objs), mimetype='application/json')
