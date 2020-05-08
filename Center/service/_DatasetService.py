from dao import DatasetDao, transfer_list
from model import Dataset, db
import uuid


class DatasetService:

    def __init__(self):
        self.datasetDao = DatasetDao(db)

    def getDatasetById(self, dataset_id):
        dataset = self.datasetDao.queryDatasetById(dataset_id)
        if dataset is not None:
            dataset = dataset.serialize
        return dataset


    def getDatasetListByUserid(self, userid):
        template = ['id', 'name', 'public', 'created_time','config']
        datasets = self.datasetDao.getDatasetListByUserid(userid)

        return transfer_list(datasets, template)

    """
    the dataset tobe added must have these attributes:
        name,           # the name of the dataset
        created_by,     # the userid of this dataset
    """

    def addDataset(self, dataset):
        dataset.id = str(uuid.uuid4()).replace('-', '')
        self.datasetDao.addDataset(dataset)
        