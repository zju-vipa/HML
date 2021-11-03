import requests

"""
test
"""


def test_login():
    user_info = {'password': '2333133223', 'email': '1@qq.com'}
    result = requests.post("http://10.214.211.135:8021/api/private/v1/user/login", data=user_info)
    print("------start to print-------")
    print(result.text)
    print("------finish to print-------")


def test_register():
    user_info = {'username': '122223', 'password': '2333133223', 'email': '1@qq.com'}
    result = requests.post("http://10.214.211.135:8021/api/private/v1/user/register", data=user_info)
    print("------start to print-------")
    print(result.text)
    print("------finish to print-------")
