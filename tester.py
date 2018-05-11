from hypqr.user import HyperQRUsers
from pymongo import MongoClient
from pprint import pprint


if __name__ == '__main__':
    dbclient = MongoClient()

    users = HyperQRUsers(dbclient)
    user = users.find_user('drober')
    if user:
        print("User 'drober' found.")

    if users.find_user('drober'):
        user_info = users.get_user_info('drober')
        if users.is_verified(user_info['_id']):
            print("drober is verified")
        else:
            print("drober is not verified... verifying")
            users.set_verified(user_info['_id'], "1")
    else:
        print("User drober not found")

    (created, message) = users.add_user(
        {
            'username': "droboto",
            'email': 'drober+cv@gmail.com',
            'password': 'hash',
            'birthday': '1982-06-08'
        }
    )
    if created:
        print("Added user: droboto ({})".format(message))
    else:
        print("Failed to add user: {}".format(message))
    pprint("Users count: {}".format(users.count_users()))
