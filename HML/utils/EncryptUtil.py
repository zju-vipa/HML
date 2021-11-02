from itsdangerous import TimedJSONWebSignatureSerializer as TimeSerializer
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask import current_app
import hashlib
import uuid


def get_uid():
    return str(uuid.uuid4()).replace('-', '')


def sha256(text):
    """
    used for password encrypt
    :param text:
    :return: res
    """
    encrypt_tool = hashlib.sha256()
    encrypt_tool.update(text.encode())
    res = encrypt_tool.hexdigest()
    return res


def encrypt_password(password):
    return sha256(password)


def create_token(api_user):
    """
    JWT: JSON Web Token
    :param api_user: user_id
    :return: token
    """
    s = TimeSerializer(current_app.config["SECRET_KEY"], expires_in=604800)  # JSON Web Signature
    token = s.dumps({'id': api_user}).decode("ascii")
    return token


def verify_token(token):
    """
    校验token
    :param token:
    :return: 用户信息 or None
    """
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = TimeSerializer(current_app.config["SECRET_KEY"])
    try:
        # 转换为字典
        data = s.loads(token)
    except Exception:
        return None
    return data['id']


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


def verify_machine_token(token):
    """
    校验token
    :param token:
    :return: machine information or None
    """
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 转换为字典
        data = s.loads(token)
        print('data is:', data)
    except Exception:
        return None
    return data['id']