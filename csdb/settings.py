# -*- coding:utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class base_config():
    SECRET_KEY = 'Gourds'
    DEBUG = False
    WTF_CSRF_ENABLED = False
    LOG_PATH = os.path.join(basedir, 'logs')
    LOG_PATH_INFO = os.path.join(LOG_PATH, 'info.log')
    LOG_PATH_ERROR = os.path.join(LOG_PATH, 'error.log')
    # flask-sqlalchemy
    DB_USER = os.getenv('DB_USER')
    DB_PWD = os.getenv('DB_PWD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    #LDAP
    LDAP_URL = os.getenv('LDAP_URL')
    LDAP_DN = os.getenv('LDAP_DN')
    LDAP_PASSWORD = os.getenv('LDAP_PASSWORD')
    LDAP_OU = os.getenv('LDAP_OU')
    LDAP_FILTER = os.getenv('LDAP_FILTER')
    LDAP_SCHEMA_MAP = os.getenv('LDAP_SCHEMA_MAP')
    LDAP_ENABLE = os.getenv('LDAP_ENABLE')
    LDAP_SSL = os.getenv('LDAP_SSL')

class development(base_config):
    DEBUG = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class production(base_config):
    DEBUG = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True



config = {
    'development': development,
    'production': production
}