from pymongo import MongoClient
from datetime import datetime
from hashlib import md5


class HyperQRUsers(MongoClient):
    dbclient = None
    game_database = 'hyperqr'
    users_collection = 'users'
    adventures_collection = 'adventures'
    pages_collection = 'pages'
    page_entities_collection = 'entities'
    _database = None
    _adventures = None
    _users = None
    _pages = None
    _entities = None
