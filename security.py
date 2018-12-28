from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    print("user object :{}".format(user))
    print("object_type:{}".format(type(user)))
    print("from db :{}:{}".format(user.username, user.password))
    print("from payload {}:{}".format(username, password))
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    print("payload :{}".format(payload))
    user_id = payload['identity']
    print("user id :{}".format(user_id))
    return UserModel.find_by_id(user_id)


