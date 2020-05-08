"""
BaseDao is the base class of all dao class
it provides base crud operation
"""


class BaseDao:
    def __init__(self, db, domain):
        self.db = db
        self.domain = domain

    def add(self, bean):
        self.db.session.add(bean)
        self.db.session.commit()

    def delete(self, bean):
        self.db.session.delete(bean)
        self.db.session.commit()

