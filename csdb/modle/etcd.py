import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin
from os import path
import json
import re

class EtcdBase():
    def __init__(self, config):
        self.config = config
    def get_data(self):
        username = self.config.get('username')
        password = self.config.get('password')
        gid = str(self.config['gid'])
        url = self.config['url']
        etcd_root = self.config['etcd_root']
        base_url = urljoin(url, path.join('v2/keys',etcd_root.strip('/')))
        rst = json.loads(requests.get(path.join(base_url, gid), auth=HTTPBasicAuth(username, password)).content)
        all_shard = []
        for each_node in rst['node']['nodes']:
            if str(each_node['key']).startswith(path.join(etcd_root,gid)):
                shard_url = path.join(url,'v2/keys',str(each_node['key']).strip('/'))
                info_get = [
                    'dn',
                    'shard_id',
                    'merge_rel',
                    'gm/private_ip',
                    'gm/redis',
                    'gm/redis_db',
                    'gm/redis_rank',
                    'gm/redis_rank_db'
                ]
                shard_info = dict()
                for s_key in info_get:
                    if re.search('[0-9]{4}$', shard_url):
                        s_value = requests.get(path.join(shard_url,s_key), auth=HTTPBasicAuth(username, password))
                        y = json.loads(s_value.content)
                        if y.get('action') and y.get('node'):
                            shard_info[s_key] = json.loads(s_value.content).get('node').get('value')
                if shard_info:
                    shard_info['gid'] = gid
                    all_shard.append(shard_info)
        return all_shard







