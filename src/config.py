import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
DB_URI = 'TBD'


class Config(object):
    DEBUG = False
    SECRET_KEY = 'secret key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
class ProductionConfig(Config):
    SECRET_KEY = 'TBD'
    DATABASE_URI = DB_URI

class DevelopmentConfig(Config):
    DATABASE_URI = 'sqlite:///obra.db'

