from requests import HTTPError

from dao import DataturksUserDao, UserDao
from model import db
import config
import requests
import json


class DataturksUserService:

    def __init__(self):
        self.dataturksUserDao = DataturksUserDao(db)
        self.userDao = UserDao(db)

    # 调用dataturks API，进行用户注册
    def register(self, email, password, **kwargs):
        firstName = kwargs.get('firstName')
        secondName = kwargs.get('secondName')
        username = kwargs.get('username')
        if username:
            firstName = secondName = username
        if firstName is None:
            firstName = secondName = email;
        else:
            secondName = firstName

        data = {
            'firstName': firstName,
            'secondName': secondName,
            'authType': 'emailSignUp',  # use email to sign up
            "email": email
        }
        headers = {
            'Content-Type': 'application/json',
            'password': password
        }

        # dataturks base url
        url = config.DATATURKS_BASE + '/createUserWithPassword'  # can test wrong url
        # return <requests.Response>
        try:
            rep = requests.post(url=url, data=json.dumps(data), headers=headers)  # <Response [200]>, 400, ...
            rep.raise_for_status()  # will raise error if http error, can't process in this way
            result = json.loads(rep.text)
        except HTTPError:
            print('HTTP Error')
            result = None
        # result formatted as:
        # {"id":"wjMtguNHg4kZCZZy3V4ZbKakllxa","token":"7wYuUffQdOpWRCMrfrBsDrvmWdAV0PTg8GsLxAzsHhaMNsY0gZ5h3ybTnMeAOZ81"}
        return result

    # 最基本的登录dataturks的方法
    def login(self, email, password):
        headers = {
            'Content-Type': 'application/json', 'email': email,
            'encryptedPassword': password
        }

        url = config.DATATURKS_BASE + "/loginByEncrypted"
        print(url)
        try:
            rep = requests.post(url=url, data=None,
                                headers=headers)  # post the backend of dataturks to get the login auth
            rep.raise_for_status()  # will raise error if http error, can't process in this way
            result = json.loads(rep.text)
        except HTTPError:
            print('HTTP Error')
            result = None
        # result formatted as:
        # {"id":"wjMtguNHg4kZCZZy3V4ZbKakllxa","token":"7wYuUffQdOpWRCMrfrBsDrvmWdAV0PTg8GsLxAzsHhaMNsY0gZ5h3ybTnMeAOZ81"}
        return result

    # 通过center的用户id，登录dataturks，
    # 并返回使用dataturks所需的信息
    def loginByUserId(self, userid):
        user = self.userDao.queryUserById(userid)
        if user is None:
            return None
        return self.login(user.email, user.password)

    # 获取用户在dataturks的主页信息
    def getUserHome(self, uid, token):
        headers = {
            'Content-Type': 'application/json',
            'uid': uid,
            'token': token
        }

        url = config.DATATURKS_BASE + "/getUserHome"
        try:
            rep = requests.post(url=url, data=None,
                                headers=headers)  # post the backend of dataturks to get the login auth
            rep.raise_for_status()  # will raise error if http error, can't process in this way
            result = json.loads(rep.text)
        except:
            result = None

        return result
