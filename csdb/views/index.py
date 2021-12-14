
from flask import render_template, request, make_response, flash
from csdb.forms import SettingForm, ShardForm, SearchForm
from csdb.modle.dbm import EtcdData, SettingInfo
from csdb.views import index_bp


@index_bp.route('/index', methods=['GET', 'POST'])
def index():
    args = request.args
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if form.shard_id.data:
        # print(EtcdData.__table__.columns.keys())
        pagination = EtcdData.query.filter_by(gid=form.gid.data, shard_id=form.shard_id.data).paginate(1, per_page=10)
    elif form.gid.data:
        pagination = EtcdData.query.filter_by(gid=form.gid.data).paginate(page, per_page=10)
    else:
        pagination = EtcdData.query.paginate(page, per_page=10)
    messages = pagination.items
    if not messages:
        flash('查询参数有误!', 'warning')
    return render_template('index.html',pagination=pagination, messages=messages, form=form)


