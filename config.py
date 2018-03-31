import os

class Config(object):

    SERVER_HOST = 'localhost'
    SERVER_PORT = 6000
    SECRET_KEY = 'secret key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/test.db'


class ProdConfig(Config):

    ENV = 'prod'
    DEBUG = False

    if 'RDS_HOSTNAME' in os.environ:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}/{os.environ['RDS_DB_NAME']}"
