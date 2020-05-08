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

    def delete(self, id):
        bean = self.domain.query.filter_by(id=id).first()
        self.db.session.delete(bean)
        self.db.session.commit()

    def update(self, bean):
        self.db.session.add(bean)
        self.db.session.commit()

    def queryById(self, id):
        bean = self.domain.query.filter_by(id=id).first()
        return bean