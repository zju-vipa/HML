from model import Dataset
from dao._BaseDao import BaseDao
from sqlalchemy import or_

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

    def deleteDataset(self, dataset_id):
        dataset = Dataset.query.filter_by(dataset_id=dataset_id).first()
        self.delete(dataset)

    def queryDatasetById(self, dataset_id):
        dataset = Dataset.query.filter_by(dataset_id=dataset_id).first()
        return dataset

    def queryDatasetListByUserId(self, user_id, if_featureEng=None):
        # Dataset.query.filter(or_(Dataset.user_id == user_id, Dataset.if_public == 1))
        if if_featureEng is None:
            datasets = Dataset.query.filter_by(user_id=user_id).all()
        else:
            datasets = Dataset.query.filter_by(user_id=user_id) \
                .filter_by(if_featureEng=if_featureEng).all()

        return datasets

    def updateDataset(self, dataset_bean):
        dataset = Dataset.query.filter_by(dataset_id=dataset_bean.dataset_id).first()
        # not update task_id
        dataset.dataset_name = dataset_bean.dataset_name
        dataset.file_type = dataset_bean.file_type
        dataset.if_profile = dataset_bean.if_profile
        dataset.profile_state = dataset_bean.profile_state
        dataset.if_public = dataset_bean.if_public
        dataset.introduction = dataset_bean.introduction
        dataset.if_featureEng = dataset_bean.if_featureEng
        dataset.featureEng_id = dataset_bean.featureEng_id
        dataset.original_dataset_id = dataset_bean.original_dataset_id
        dataset.user_id = dataset_bean.user_id
        dataset.username = dataset_bean.username
        self.db.session.commit()
