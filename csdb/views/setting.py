
from csdb.views import setting_bp
from csdb.forms import SettingForm
from csdb.modle.dbm import EtcdData, SettingInfo
from flask import render_template, request, flash, redirect, url_for
from csdb.extensions import db
from csdb.modle.etcd import EtcdBase


@setting_bp.route('/setting', methods=['GET', 'POST'])
def setting():
    form = SettingForm()
    if form.validate_on_submit():
        add_setting = SettingInfo(
            description = form.description.data,
            url = form.url.data,
            username = form.username.data,
            password = form.password.data,
            etcd_root = form.etcd_root.data,
            gid = form.gid.data,
        )
        db.session.add(add_setting)
        db.session.commit()
        return redirect(url_for('setting.setting'))
    messages = SettingInfo.query.all()
    return render_template('setting.html', form=form, messages=messages)

@setting_bp.route('/get_etcd_info', methods=['GET'])
def get_etcd_info():
    args = request.args
    config_list = []
    if args.get('all_sync'):
        config_list = SettingInfo.query.all()
    elif args.get('id'):
        config_list = SettingInfo.query.filter_by(id=args.get('id', 211)).all()
    for i in config_list:
        config = i.to_dict()
        shard_info_list = EtcdBase(config=config).get_data()
        EtcdData.sync_shard_data(shard_info_list)
    flash('Etcd数据同步成功', 'success')
    return 'ok'