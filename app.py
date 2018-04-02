import hashlib
from datetime import datetime, timedelta
from dateutil import parser
import random
import requests
from enum import Enum
from flask import Flask, Blueprint, request, Response, json
from extensions import cors, db, migrate
from controllers.database.whistle import Whistle, Shift
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
    report_date = data.get('report_date')
    if report_date:
        time_window = datetime.utcnow() - timedelta(days=2)
        reported_date = parser.parse(report_date)
        if reported_date < time_window:
            valid = False

    return valid

def generate_hash(request):
    user_string = request.headers.get('User-Agent', 'unknown')
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    input = ip + ' ' + user_string
    return hashlib.md5(input.encode()).hexdigest()

def is_unique(hash, report_date, shift):
    time_window = datetime.utcnow() - timedelta(hours=12)
    if report_date:
        reported_date = parser.parse(report_date).date()
    else:
        reported_date = datetime.utcnow().date()  

    if not shift:
        shift = Shift.day

    print("HERE", report_date, reported_date, shift)
    existing = Whistle.query.filter(
        Whistle.hash == hash,
        Whistle.created_date > time_window,
        # Whistle.report_date == reported_date,
        Whistle.shift == shift).all() #.limit(1).one_or_none()
    for rec in existing:
        print('REC', reported_date == rec.report_date, reported_date, rec.report_date, rec.shift)
    print('REC', existing)
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
    if not is_unique(user_hash, request.json.get('report_date'), request.json.get('shift')):
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
    time_window = datetime.utcnow() - timedelta(days=7)
    whistles = Whistle.query.filter(
        Whistle.report_date > time_window).all()
    whistle_objs = []
    for item in whistles:
        whistle_objs.append(item.as_simple_dict())

    return Response(json.dumps(whistle_objs, cls=EnumEncoder),
                    mimetype='application/json')
