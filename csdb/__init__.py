# -*- coding:utf-8 -*-

import os
from flask import Flask
from csdb.settings import config
from csdb.views import index
from csdb.extensions import db, bootstrap, csrf, login_manager
from csdb.views import index_bp, login_bp, setting_bp, client_bp
from csdb.commands.init_db import init_db

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('csdb')
    app.config.from_object(config[config_name])
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app



def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(setting_bp)
    app.register_blueprint(client_bp)

def register_commands(app):
    app.cli.add_command(init_db)

def register_errors(app):
    pass

def register_logging(app):
    import logging
    from logging.handlers import RotatingFileHandler
    class InfoFilter(logging.Filter):
        def filter(self, record):
            """only use INFO
            筛选, 只需要 INFO 级别的log
            :param record:
            :return:
            """
            if logging.INFO <= record.levelno < logging.ERROR:
                # 已经是INFO级别了
                # 然后利用父类, 返回 1
                return 1
            else:
                return 0
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(pathname)s %(lineno)s %(module)s.%(funcName)s %(message)s')

    # log dir
    if not os.path.exists(app.config['LOG_PATH']):
        os.makedirs(app.config['LOG_PATH'])

    # FileHandler Info
    file_handler_info = RotatingFileHandler(filename=app.config['LOG_PATH_INFO'])
    file_handler_info.setFormatter(formatter)
    file_handler_info.setLevel(logging.INFO)
    info_filter = InfoFilter()
    file_handler_info.addFilter(info_filter)
    app.logger.addHandler(file_handler_info)

    # FileHandler Error
    file_handler_error = RotatingFileHandler(filename=app.config['LOG_PATH_ERROR'])
    file_handler_error.setFormatter(formatter)
    file_handler_error.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler_error)