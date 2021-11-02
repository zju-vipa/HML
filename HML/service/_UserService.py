from dao import UserDao
from model import db
from utils.EncryptUtil import encrypt_password, get_uid


class UserService:

    def __init__(self):
        self.userDao = UserDao(db)

    """
    this function will replace the password with encrypted password
    then add the user to database
    the user bean used for register should contains: 
        username, 
        password, 
        email,
    """
    def addUser(self, user):
        user.user_id = get_uid()
        user.password = encrypt_password(user.password)
        self.userDao.add(user)
        return user

    def queryUserById(self, user_id):
        user = self.userDao.queryUserById(user_id)
        if user:
            return user
        else:
            return None

    """
    used to check whether this name is available
    the database can't tolerate duplicated username
    """
    def queryUserByName(self, username):
        user = self.userDao.queryUserByName(username)
        if user:
            return user
        else:
            return None

    """
    used to check whether this email is available
    the database can't tolerate duplicated email
    """
    def queryUserByEmail(self, email):
        user = self.userDao.queryUserByEmail(email)
        if user:
            return user
        else:
            return None

    def loginByPassword(self, user):
        database_user = self.userDao.queryUserByEmail(user.email)
        if database_user and database_user.password == encrypt_password(user.password):
            return database_user
        else:
            return None
