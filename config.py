import os

class Config(object):

    SERVER_HOST = 'localhost'
    SERVER_PORT = 6001
    SECRET_KEY = 'secret key'
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres@localhost/whistles'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = f"postgres://floswhistleuser:codefordayton@aa2txh2j15e4y7.cfjnvamuuqaj.us-west-2.rds.amazonaws.com/ebdb"



class ProdConfig(Config):

    ENV = 'prod'
    DEBUG = True

    # CORS_ORIGINS = [
    #     'https://floswhistle.com',
    #     'https://floswhistle.org',
    #     'https://www.floswhistle.com',
    #     'https://www.floswhistle.org',
    #     'https://beta.floswhistle.org'
    # ]

    if 'RDS_HOSTNAME' in os.environ:
        SQLALCHEMY_DATABASE_URI = f"postgres://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}/{os.environ['RDS_DB_NAME']}"


class TestConfig(Config):
    ENV = 'test'
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/test1.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    #         os.path.join(os.path.dirname(.app.instance_path), 'test.db' 
