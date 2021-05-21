from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI =  ''

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME'))
    SQLALCHEMY_ECHO = False
    SECRET_KEY= os.getenv('PASS_KEY')
    SECURITY_PASSWORD_SALT= os.getenv('SECURITY_PASSWORD_SALT')
    MAIL_DEFAULT_SENDER= os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_SERVER= os.getenv('MAIL_SERVER')
    MAIL_PORT= 2525
    MAIL_USERNAME= os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD= os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS= True
    MAIL_USE_SSL= False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_ECHO = False
    SECRET_KEY= os.getenv('PASS_KEY')
    SECURITY_PASSWORD_SALT= os.getenv('SECURITY_PASSWORD_SALT')
    MAIL_DEFAULT_SENDER= os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_SERVER= os.getenv('MAIL_SERVER')
    MAIL_PORT= 2525
    MAIL_USERNAME= os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD= os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True