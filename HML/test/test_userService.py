from app._UserApp import userService
from model import User


def test_addUser():
    user_bean = User()
    user_bean.username = '123'
    user_bean.email = '1232244@qq.com'
    user_bean.password = 'qqqqq'
    user = userService.addUser(user_bean).serialize
    print("------start to print-------")
    print(user)
    print("------finish to print-------")


def test_queryUserById():
    user = userService.queryUserById('c64e58484d294e21b30fb382b60c9bf0')
    if user:
        user = user.serialize
    print("------start to print-------")
    print(user)
    print("------finish to print-------")


def test_queryUserByName():
    user = userService.queryUserByName('123')
    if user:
        user = user.serialize
    print("------start to print-------")
    print(user)
    print("------finish to print-------")


def test_queryUserByEmail():
    user = userService.queryUserByEmail('1232244@qq.com')
    if user:
        user = user.serialize
    print("------start to print-------")
    print(user)
    print("------finish to print-------")


def test_loginByPassword():
    user_bean = User()
    user_bean.email = '1232244@qq.com'
    user_bean.password = 'qqqqq'
    user = userService.loginByPassword(user_bean)
    if user:
        user = user.serialize
    print("------start to print-------")
    print(user)
    print("------finish to print-------")

