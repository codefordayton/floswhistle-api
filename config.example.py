class Config(object):

    SERVER_HOST = 'localhost'
    SERVER_PORT = 6000
    SECRET_KEY = 'secret key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'


class ProdConfig(Config):

    ENV = 'prod'
    DEBUG = False

