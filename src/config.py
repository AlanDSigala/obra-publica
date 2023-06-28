import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

DB_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="AlanDanielSigala",
    password="Yoloswag2020630668$",
    hostname="AlanDanielSigala.mysql.pythonanywhere-services.com",
    databasename="AlanDanielSigala$forapp"
)


class Config(object):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
class ProductionConfig(Config):
    SECRET_KEY = 'TBD'
    DATABASE_URI = DB_URI

class DevelopmentConfig(Config):
    DATABASE_URI = 'sqlite:///obra.db'
    SQLALCHEMY_DATABASE_URI= "sqlite:///obra.db"

