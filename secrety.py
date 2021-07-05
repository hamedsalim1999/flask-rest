from users import User


user = [
    User(1,'bob','rust')
]
username_mapping={u.username: u for u in user}
userid_mapping = {u.id: u for u in user}


def authenticate(username , password):
    user = username_mapping.get(username,None)
    if user and user.password == password:
        return user
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id)
