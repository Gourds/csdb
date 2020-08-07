from ldap3 import Server, Connection
from flask import current_app
from flask_login import current_user
import json


class LdapConfig():
    def __init__(self, config=None):
        self.server_uri = None
        self.bind_dn = None
        self.password = None
        self.use_ssl = None
        self.search_ou = None
        self.search_filter = None
        self.attr_map = None
        self.auth_ldap = None
        if isinstance(config, dict):
            self.load_from_config(config)
        else:
            self.load_from_settings(current_app)

    def load_from_config(self, config):
        self.server_uri = config.get('ldap_url')
        self.bind_dn = config.get('ldap_dn')
        self.password = config.get('ldap_password')
        self.use_ssl = config.get('ldap_ssl')
        self.search_ou = config.get('ldap_ou')
        self.search_filter = config.get('ldap_filter')
        self.attr_map = config.get('ldap_schema_map')
        self.auth_ldap = config.get('ldap_enable')

    def load_from_settings(self, app):
        config = app.config
        self.server_uri = config.get('LDAP_URL')
        self.bind_dn = config.get('LDAP_DN')
        self.password = config.get('LDAP_PASSWORD')
        self.use_ssl = config.get('LDAP_SSL')
        self.search_ou = config.get('LDAP_OU')
        self.search_filter = config.get('LDAP_FILTER')
        if isinstance(config.get('LDAP_SCHEMA_MAP'), dict):
            self.attr_map = config.get('LDAP_SCHEMA_MAP')
        else:
            self.attr_map = json.loads(config.get('LDAP_SCHEMA_MAP'))
        self.auth_ldap = config.get('LDAP_ENABLE')


class LdapBackend():
    def __init__(self, config=None):
        if isinstance(config, dict):
            self.config = LdapConfig(config=config)
        else:
            self.config = LdapConfig()
        self._conn = None
        self._paged_size = self.get_paged_size()
        self.search_users = None
        self.search_value = None

    @property
    def connection(self):
        if self._conn:
            return self._conn
        server = Server(self.config.server_uri, use_ssl=self.config.use_ssl)
        conn = Connection(server, self.config.bind_dn, self.config.password)
        conn.bind()
        self._conn = conn
        return self._conn

    @staticmethod
    def get_paged_size():
        paged_size = 1000
        if isinstance(paged_size, int):
            return paged_size
        return None

    def paged_cookie(self):
        if self._paged_size is None:
            return None
        try:
            cookie = self.connection.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
            return cookie
        except Exception as e:
            return None

    def get_search_filter_extra(self):
        extra = ''
        if self.search_users:
            mapping_username = self.config.attr_map.get('username')
            for user in self.search_users:
                extra += '({}={})'.format(mapping_username, user)
            return '(|{})'.format(extra)
        if self.search_value:
            for attr in self.config.attr_map.values():
                extra += '({}={})'.format(attr, self.search_value)
            return '(|{})'.format(extra)
        return extra

    def get_search_filter(self):
        search_filter = self.config.search_filter % {'user': '*'}
        search_filter_extra = self.get_search_filter_extra()
        if search_filter_extra:
            search_filter = '(&{}{})'.format(search_filter, search_filter_extra)
        return search_filter

    def search_user_entries_ou(self, search_ou, paged_cookie=None):
        search_filter = self.get_search_filter()
        attributes = list(self.config.attr_map.values())
        self.connection.search(
            search_base=search_ou, search_filter=search_filter,
            attributes=attributes, paged_size=self._paged_size,
            paged_cookie=paged_cookie
        )

    def search_user_entries(self):
        user_entries = list()
        search_ous = str(self.config.search_ou).split('|')
        for search_ou in search_ous:
            self.search_user_entries_ou(search_ou)
            user_entries.extend(self.connection.entries)
            while self.paged_cookie():
                self.search_user_entries_ou(search_ou, self.paged_cookie())
                user_entries.extend(self.connection.entries)
        return user_entries

    def user_entry_to_dict(self, entry):
        user = {}
        attr_map = self.config.attr_map.items()
        for attr, mapping in attr_map:
            if not hasattr(entry, mapping):
                continue
            value = getattr(entry, mapping).value or ''
            if attr == 'is_active' and mapping.lower() == 'useraccountcontrol' \
                    and value:
                value = int(value)
            user[attr] = value
        return user

    def user_entries_to_dict(self, user_entries):
        users = []
        for user_entry in user_entries:
            user = self.user_entry_to_dict(user_entry)
            users.append(user)
        return users


class LdapAuthorizationBackend(LdapBackend):
    @staticmethod
    def user_can_authenticate(user):
        is_valid = getattr(user, 'is_valid', None)
        return is_valid or is_valid is None

    def pre_check(self, username, password):
        if not self.config.auth_ldap:
            error = 'Not enabled ldap'
            return False, error
        if not username:
            error = 'No username'
            return False, error
        if not password:
            error = 'No password'
            return False, error
        return True, ''

    def authenticate(self, request=None, username=None, password=None, **kwargs):
        match, msg = self.pre_check(username, password)
        if not match:
            return None
        rst = Connection(
            Server(self.config.server_uri, use_ssl=self.config.use_ssl),
            user=self._get_user_dn(username),
            password=password,
        )
        try:
            return rst.bind()
        finally:
            rst.unbind()

    def _get_user_dn(self, username):
        user_dn = 'uid={},cn=users,dc=taiyouxi,dc=cn'.format(username)
        return user_dn


def LdapLogin(username, password):
    auth_rst = LdapAuthorizationBackend()
    if auth_rst.authenticate(username=username, password=password):
        rst = LdapBackend()
        user_data = rst.search_user_entries()
        for i in rst.user_entries_to_dict(user_data):
            if i.get('username') == username:
                return {
                    'login': 'ok',
                }

