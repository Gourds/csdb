

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField,  \
    ValidationError, HiddenField,BooleanField,PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

class SettingForm(FlaskForm):
    description = StringField('description', validators=[DataRequired(), Length(1,20)])
    url = StringField('url', validators=[DataRequired(), URL(), Length(1,255)])
    username = StringField('username', validators=[DataRequired(), Length(1,30)])
    password = PasswordField('password', validators=[DataRequired(), Length(1,128)])
    etcd_root = StringField('etcd_root', validators=[DataRequired(), Length(1,64)])
    gid = IntegerField('gid', validators=[DataRequired()])
    submit = SubmitField('添加')

    def to_dict(self):
        return {
            'description': self.description.data,
            'url': self.url.data,
            'username': self.username.data,
            'password': self.password.data,
            'etcd_root': self.etcd_root.data,
            'gid': self.gid.data,
        }

class SettingUpdateForm(SettingForm):
    id = IntegerField('id', validators=[DataRequired()])


class ShardForm(FlaskForm):
    gid = IntegerField('gid', validators=[DataRequired(message='gid not be null')])
    shard_id = IntegerField('shard_id', validators=[DataRequired(message='shardid not be null')])
    merge_rel = StringField('merge_rel')
    redis = StringField('redis', validators=[Length(1,50, message='redis length error')])
    redis_db = IntegerField('redis_db', validators=[DataRequired(message='reids not null')])
    rank_redis = StringField('rank_redis', validators=[Length(1,50, message='rank error')])
    rank_redis_db = IntegerField('rank_redis_db', validators=[DataRequired(message='rank not null')])
    dn = StringField('dn', validators=[Length(1,100, message='dn error')])
    private_ip = StringField('private_ip', validators=[Length(0,100, message='ip error')])
    submit = SubmitField()

    def to_dict(self):
        return {
            'gid': self.gid.data,
            'shard_id': self.shard_id.data,
            'merge_rel': self.merge_rel.data,
            'redis': self.redis.data,
            'redis_db': self.redis_db.data,
            'rank_redis': self.rank_redis.data,
            'rank_redis_db': self.rank_redis_db.data,
            'db': self.dn.data,
            'private_ip': self.private_ip.data,
        }

class SearchForm(FlaskForm):
    gid = SelectField(choices=[211, 212])
    shard_id = IntegerField('shard_id')
    # summit = SubmitField()
    search = SubmitField('查询')
    def to_dict(self):
        return {
            'gid' : self.gid.data,
            'shard_id': self.shard_id.data,
        }

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('记住')
    submit = SubmitField('登录')
    def to_dict(self):
        return {
            'username': self.username.data,
            'password': self.password.data,
        }

class LogoutForm(LoginForm):
    username = HiddenField()
    password = HiddenField()
    remember_me = HiddenField()
    submit = SubmitField('登出')