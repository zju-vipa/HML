from model import User
from dao._BaseDao import BaseDao

"""
used for user related database operation
"""


class UserDao(BaseDao):
    def __init__(self, db):
        self.db = db
        super().__init__(db, User)

    """
    provide functions of base class another name 
    """
    # 增加一位用户
    def addUser(self, user):
        self.add(user)

    # 通过id删除一位用户
    def deleteUserById(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        self.delete(user)

    # 通过id查询用户
    def queryUserById(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        return user

    # 通过name查找用户
    def queryUserByName(self, username):
        user = User.query.filter_by(username=username).first()
        return user

    # 通过email查找用户
    def queryUserByEmail(self, email):
        user = User.query.filter_by(email=email).first()
        return user

    # 更新用户信息
    def updateUser(self, user_bean):
        user = User.query.filter_by(user_id=user_bean.user_id).first()
        user.email = user_bean.email
        user.username = user_bean.username
        user.password = user_bean.password
        self.db.session.commit()

