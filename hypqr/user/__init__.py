from datetime import datetime
from hashlib import md5


class HyperQRUsers:
    dbclient = None
    game_database = 'hyperqr'
    users_collection = 'users'
    _database = None
    _users = None
    _sensitive_user_keys = ['password', ]

    def __init__(self, dbclient, game_database=None):
        """
        Expects a MongoDB Client to be established
        :param dbclient: mongodb object
        """
        self.dbclient = dbclient
        if game_database:
            self.game_database = game_database
        self._database = self.dbclient[self.game_database]
        self._users = self._database[self.users_collection]

    def find_user(self, username):
        _data = self._users.find_one({'username': username})
        if _data:
            return True
        return False

    def get_user_info(self, username, key_type='username'):
        if key_type == "id":
            _data = self._users.find_one({'_id': username})
        else:
            _data = self._users.find_one({'username': username})
        if '_id' in _data:
            return self._del_sensitive_keys(_data)
        return False

    def add_user(self, userdata):
        _data_needs = ['username', 'password', 'email', 'birthday']
        for _data in _data_needs:
            if _data not in userdata:
                return False, "_USER_INFO_INCOMPLETE"
        if not self.find_user(userdata['username']):
            userdata['password'] = md5(bytes(userdata['password'], encoding='utf-8')).hexdigest()
            userdata['verified'] = False,
            userdata['birthday'] = datetime.strptime(userdata['birthday'], "%Y-%M-%d")
            _status = self._users.insert_one(userdata)
            return True, _status
        return False, "_USER_ALREADY_EXISTS"

    def is_verified(self, user_id):
        _data = self.get_user_info(user_id, key_type='id')
        if _data:
            if 'verified' in _data:
                if _data['verified'] == 1:
                    return True
        return False

    def set_verified(self, user_id, status=0):
        _data = self.get_user_info(user_id, key_type='id')
        if _data:
            self._users.update(user_id, {'$set': {'verified': status}})
            return self.is_verified(user_id)
        return False

    def delete_user(self, username):
        _delete_info = self.find_user(username)
        if '_id' in _delete_info:
            self._users.deleteOne(_delete_info)

    def list_users(self):
        data = []
        _temp = self._users.find()
        for _temp_data in _temp:
            data.append(self._del_sensitive_keys(_temp_data))
        return data

    def count_users(self):
        return self._users.count()

    def _del_sensitive_keys(self, userdata):
        for sensitive_key in self._sensitive_user_keys:
            if sensitive_key in userdata:
                del userdata[sensitive_key]
        return userdata
