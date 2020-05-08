from model import Dataset
from dao._BaseDao import BaseDao

"""
used for dataset related database operation
"""
class DatasetDao(BaseDao):

    def __init__(self, db):
        super().__init__(db, Dataset)

    """
    provide functions of base class another name 
    """
    def addDataset(self, dataset):
        self.add(dataset)

    def deleteDataset(self, datasetId):
        self.delete(datasetId)

    def updateDataset(self, dataset):
        self.update(dataset)

    def queryDatasetById(self, datasetId):
        return self.queryById(datasetId)


    """
    use the userid to get his dataset list
    """
    def getDatasetListByUserid(self, userid):
        datasets = Dataset.query.filter_by(created_by=userid).all()
        return datasets