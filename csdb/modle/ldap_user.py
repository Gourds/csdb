

class LdapUser():
    def __init__(self, username):
        self.id = username
        self.username = username

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    @classmethod
    def get_user(cls, userid):
        if True:
            return cls(userid)
        else:
            return None


