from flask import render_template, request, make_response, flash
from csdb.forms import SettingForm, ShardForm, SearchForm
from csdb.modle.dbm import EtcdData, SettingInfo
from csdb.views import client_bp


@client_bp.route('/ip', methods=['GET', 'POST'])
def client_info():
    return render_template('client_info.html')