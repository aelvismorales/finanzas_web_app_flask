from distutils.debug import DEBUG
import os
import urllib.parse
from flask_sqlalchemy import SQLAlchemy

class Config(object):
    SECRET_KEY='asd123'

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:admin@localhost:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    

