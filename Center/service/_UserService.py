from dao import UserDao
from model import User, db
from utils.EncryptUtil import encryptPassword
import uuid

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
        user.id = str(uuid.uuid4()).replace('-', '')
        user.password = encryptPassword(user.password)
        self.userDao.add(user)


    def queryUserById(self, id):
        return self.userDao.queryUserById(id)

    """
    used to check whether this name is available
    the database can't tolerate duplicated username
    """
    def queryUserByName(self, name):
        return self.userDao.queryUserByName(name)

    """
    used to check whether this email is available
    the database can't tolerate duplicated email
    """
    def queryUserByEmail(self, email):
        return self.userDao.queryUserByEmail(email)

    def loginByPassword(self, user):
        database_user = self.userDao.queryUserByEmail(user.email)
        if database_user.password == encryptPassword(user.password):
            return database_user.serialize
        else:
            return None