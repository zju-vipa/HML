from model import Model
from dao._BaseDao import BaseDao

"""
used for model related database operation
"""
class ModelDao(BaseDao):

    def __init__(self, db):
        super().__init__(db, Model)

    """
    provide functions of base class another name 
    """
    def addModel(self, model):
        self.add(model)

    def deleteModel(self, modelId):
        self.delete(modelId)

    def updateModel(self, model):
        self.update(model)

    def queryModelById(self, modelId):
        return self.queryById(modelId)


    """
    return the private model list of the user 
    """
    def getPrivateModelList(self, userid):
        models = Model.query.filter_by(created_by=userid).all()
        return models

    """
    return the private model list of the user 
    """
    def getPulicModelList(self):
        models = Model.query.filter_by(public=1).all()
        return models