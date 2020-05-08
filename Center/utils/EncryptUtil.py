import hashlib
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask import current_app

# used for password encrypt, just the same as dataturks
def sha256(text):
    encrypt_tool = hashlib.sha256()
    encrypt_tool.update(text.encode())
    res = encrypt_tool.hexdigest()
    return res

def encryptPassword(password):
    return sha256(password)

def create_machine_token(machine_id):
    """
    生成token
    :param machine_id: machine id
    :return: token
    """
    s = Serializer(current_app.config["SECRET_KEY"])
    token = s.dumps({'id': machine_id}).decode("ascii")
    print(token)
    return token