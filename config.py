from distutils.debug import DEBUG
import os
import urllib.parse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import psycopg2

class Config(object):
    SECRET_KEY='123447a47f563e90fe2db0f56b1b17be62378e31b7cfd3adc776c59ca4c75e2fc512c15f69bb38307d11d5d17a41a7936789'

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='postgresql://isnjonskuprehk:07d8bb3abcb665f2611cbf435a79c4dfeeac18604299189722d794802c1971fa@ec2-23-23-182-238.compute-1.amazonaws.com:5432/dbgnihpfcroaus'
    #SQLALCHEMY_DATABASE_URI='postgresql://elvis@finanzasdb@finanzasdb.postgres.database.azure.com:5432/finanzasdb'
#    dbname='{your_database}' user='elvis@finanzasdb' host='finanzasdb.postgres.database.azure.com' password='{your_password}' port='5432' sslmode='true'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    

#"postgresql://isnjonskuprehk:07d8bb3abcb665f2611cbf435a79c4dfeeac18604299189722d794802c1971fa@ec2-23-23-182-238.compute-1.amazonaws.com:5432/finanzasflask"