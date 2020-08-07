from csdb.extensions import db
import json


class EtcdData(db.Model):
    '''
    Adjacency List Relationships
    '''
    __tablename__ = 'etcd_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shard_id = db.Column(db.Integer, unique=True)
    gid = db.Column(db.Integer)
    redis = db.Column(db.String(64))
    redis_db = db.Column(db.String(64))
    rank_redis = db.Column(db.String(64))
    rank_redis_db = db.Column(db.String(64))
    dn = db.Column(db.String(64))
    private_ip = db.Column(db.String(64))
    merge_id = db.Column(db.Integer, db.ForeignKey('etcd_data.id'))
    merge_rel = db.relationship("EtcdData", back_populates='merge_main', cascade='all, delete-orphan')
    merge_main = db.relationship("EtcdData", back_populates='merge_rel', remote_side=[id])

    @staticmethod
    def merge_update(shard_ids: list):
        rst = []
        for i in shard_ids:
            shard = EtcdData.query.filter_by(shard_id=i).first()
            # if not shard:
            #     shard = EtcdData.create_shard(shard_data={'shard_id': i})
            rst.append(shard)
        return rst

    @staticmethod
    def create_shard(shard_data):
        shard = EtcdData(
            gid=shard_data.get('gid'),
            shard_id=shard_data.get('shard_id'),
            redis=shard_data.get('redis'),
            redis_db=shard_data.get('redis_db'),
            rank_redis=shard_data.get('rank_redis'),
            rank_redis_db=shard_data.get('rank_redis_db'),
            dn=shard_data.get('dn'),
            private_ip=shard_data.get('private_ip'),
        )
        if shard_data.get('merge_rel'):
            form_merge_rel = json.loads(shard_data.get('merge_rel'))
            shard.merge_rel = shard.merge_update(form_merge_rel)
        db.session.add(shard)
        db.session.commit()
        return shard

    @staticmethod
    def sync_shard_data(shard_data_list):
        for shard_data in shard_data_list:
            if shard_data.get('merge_rel'):
                form_merge_rel = [int(x) for x in shard_data.get('merge_rel').split(',')]
                for each_shard in form_merge_rel:
                    m_shard = EtcdData.query.filter_by(shard_id=each_shard).first()
                    if not m_shard:
                        m_shard = EtcdData(shard_id=each_shard)
                        db.session.add(m_shard)
                        db.session.commit()
                shard = EtcdData.query.filter_by(shard_id=int(shard_data.get('shard_id'))).first()
                shard.gid=int(shard_data.get('gid'))
                shard.shard_id=int(shard_data.get('shard_id'))
                shard.redis=shard_data.get('gm/redis')
                shard.redis_db=int(shard_data.get('gm/redis_db'))
                shard.rank_redis=shard_data.get('gm/redis_rank')
                shard.rank_redis_db=int(shard_data.get('gm/redis_rank_db'))
                shard.dn=shard_data.get('dn')
                shard.private_ip=shard_data.get('gm/private_ip')
                mer_other = [int(i) for i in shard_data.get('merge_rel').split(',')]
                mer_other.remove(int(shard_data.get('shard_id')))
                shard.merge_rel = [EtcdData.query.filter_by(shard_id=x).first() for x in mer_other]
                db.session.commit()


    def update_shard(self, shard_data):
        self.redis = shard_data.get('redis')
        self.redis_db = shard_data.get('redis_db')
        self.rank_redis = shard_data.get('rank_redis')
        self.rank_redis_db = shard_data.get('rank_redis_db')
        self.dn = shard_data.get('dn')
        if shard_data.get('merge_rel'):
            form_merge_rel = json.loads(shard_data.get('merge_rel'))
            self.merge_rel = EtcdData.merge_update(form_merge_rel)
        db.session.commit()

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

class SettingInfo(db.Model):
    __tablename__ = 'setting_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(64))
    url = db.Column(db.String(64))
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    # plus_id = db.Column(db.Integer, db.ForeignKey('setting_info.id'))
    gid = db.Column(db.Integer)
    etcd_root = db.Column(db.String(64))

    # etcd_root = db.Column()

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict


# print(EtcdData.query.all())
# db.metadata.clear()
# db.create_all()

