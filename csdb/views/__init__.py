# -*- coding: utf-8 -*-
from flask import Blueprint
from csdb.modle.permission import need_login

index_bp = Blueprint('index', __name__, url_prefix='/v1')
login_bp = Blueprint('login', __name__, url_prefix='/v1')
setting_bp = Blueprint('setting', __name__, url_prefix='/v1')

setting_bp.before_request(need_login)

from . import index
from . import login
from . import setting