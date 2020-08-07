
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_login.login_manager import LoginManager
from csdb.modle.ldap_user import LdapUser

bootstrap = Bootstrap()
db = SQLAlchemy()
csrf = CSRFProtect()

#login
login_manager = LoginManager()
login_manager.login_view = 'login.login'
login_manager.login_message = '你必须登陆后才能访问该页面'
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(userid):
    return LdapUser.get_user(userid)