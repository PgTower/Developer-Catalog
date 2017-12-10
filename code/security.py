from werkzeug.security import safe_str_cmp
from user import User

def authenicate(username, password):
    # Makes a JWT token used for identity
    # --> Doc--security.py--1
    user =User.find_by_username(username)
    # safe_str_cmp used to allow older python2 compatibility
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    # Uses the token from authenicate
    # --> Doc--security.py--2
    user_id = payload['identity']
    return User.find_by_id(user_id)