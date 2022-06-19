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
    

#"postgresql://isnjonskuprehk:07d8bb3abcb665f2611cbf435a79c4dfeeac18604299189722d794802c1971fa@ec2-23-23-182-238.compute-1.amazonaws.com:5432/finanzasflask"