from model import FeatureEng
from dao._BaseDao import BaseDao

"""
used for Feature related database operation
"""


class FeatureEngDao(BaseDao):

    def __init__(self, db):
        super().__init__(db, FeatureEng)

    """
    provide functions of base class another name 
    """

    def addFeatureEng(self, featureEng):
        self.add(featureEng)

    def deleteFeatureEng(self, featureEng_id):
        featureEng = FeatureEng.query.filter_by(featureEng_id=featureEng_id).first()
        self.delete(featureEng)

    def queryFeatureEngById(self, featureEng_id):
        featureEng = FeatureEng.query.filter_by(featureEng_id=featureEng_id).first()
        return featureEng

    def queryFeatureEngListByUserId(self, user_id):
        featureEngs = FeatureEng.query.filter_by(user_id=user_id).all()
        return featureEngs

    def updateFeatureEng(self, featureEng_bean):
        featureEng = FeatureEng.query.filter_by(featureEng_id=featureEng_bean.featureEng_id).first()
        # not update task_id
        featureEng.featureEng_name = featureEng_bean.featureEng_name
        featureEng.featureEng_type = featureEng_bean.featureEng_type
        featureEng.featureEng_modules = featureEng_bean.featureEng_modules
        featureEng.featureEng_processes = featureEng_bean.featureEng_processes
        featureEng.operate_state = featureEng_bean.operate_state
        featureEng.new_dataset_id = featureEng_bean.new_dataset_id
        featureEng.original_dataset_id = featureEng_bean.original_dataset_id
        featureEng.user_id = featureEng_bean.user_id
        featureEng.username = featureEng_bean.username
        featureEng.FeatureEng_efficiency = featureEng_bean.FeatureEng_efficiency
        featureEng.FeatureEng_accuracy = featureEng_bean.FeatureEng_accuracy
        featureEng.featureEng_operationMode = featureEng_bean.featureEng_operationMode
        featureEng.start_time = featureEng_bean.start_time
        self.db.session.commit()

    def updateTaskStatus(self, featureEng_id):
        featureEng = FeatureEng.query.filter_by(featureEng_id=featureEng_id).first()
        featureEng.operate_state = '3'
        self.db.session.commit()

    def queryLatestFeatureEngByUserId(self, user_id):
        featureEng = FeatureEng.query.filter_by(user_id=user_id, operate_state='2').order_by('start_time')[-1]
        return featureEng

    def queryFinishedFeatureEngListByUserId(self, user_id):
        featureEngs = FeatureEng.query.filter_by(user_id=user_id, operate_state='2').all()
        return featureEngs