import hashlib
import requests
import json
from flask import Flask, Blueprint, request, Response
from extensions import cors, db, migrate
from controllers.database.whistle import Whistle

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
    # TODO: What does valid mean? Filled out?
    return True


def generate_hash(request):
    user_string = request.headers.get('User-Agent', 'unknown')
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    input = ip + ' ' + user_string
    return hashlib.md5(input.encode()).hexdigest()


def is_unique(hash):
    time_window = datetime.now() - datetime.timedelta(hours=12)
    return Whistle.query.filter(
        Whistle.hash == user_hash,
        Whistle.report_date > time_window).limit(1).one_or_none()


@api_blueprint.route('/whistle', methods=['POST'])
def create_whistle():
    resp = {}

    # check that the request is valid
    if not is_valid(request.json):
        return Response(json.dumps({'error': 'Invalid request'}),
                        mimetype='application/json',
                        status_code=400)

    # check that we haven't seen this user in 12 hours
    user_hash = generate_hash(request)
    if not is_unique(user_hash):
        return Response(json.dumps({'error': 'Too many requests'}),
                        mimetype='application/json',
                        status_code=400)

    # add whistle
    whistle = Whistle(hash=user_hash, **request.json)
    db.session.add(whistle)
    db.session.commit()

    return Response(json.dumps(whistle.as_dict(), cls=EnumEncoder),
                    mimetype='application/json')


@api_blueprint.route('/data', methods=['GET'])
def get_data():
    resp = {}
    return Response(json.dumps(resp), mimetype='application/json')

