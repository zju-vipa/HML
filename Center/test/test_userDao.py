from dao import UserDao
from model import User,db


def test_queryUser():
    user = userDao.queryUserById("123123")
    assert(user.password == "123")
    user = userDao.queryUserById("q123")
    assert(user is None)

def test_addUser():
    user = User()
    user.id = "123124"
    user.username = "sontal2"
    user.password = "1234"
    user.email = "111111@qq.com"
    userDao.addUser(user)

def test_updateUser():
    user = userDao.queryUserById("123124")
    user.password = "999"
    userDao.updateUser(user)
    new_user = userDao.queryUserById("123124")
    assert(new_user.password == "999")

def test_deleteUser():
    userDao.deleteUserById("123124")
    user = userDao.queryUserById("123124")
    assert user is None;
