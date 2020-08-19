from dao import FeatureEngDao
from model import db
from utils.EncryptUtil import get_uid
from celery_tasks.tasks import FeatureEngTasks
import os
import shutil
from flask import current_app


class FeatureEngService:

    def __init__(self):
        self.featureEngDao = FeatureEngDao(db)

    def addFeatureEng(self, featureEng, featureEng_processes, original_dataset,
                      original_dataset_file_path, new_dataset_name):
        featureEng.featureEng_id = get_uid()
        featureEng.operate_state = '1'

        task = FeatureEngTasks.operate.apply_async((featureEng.serialize,
                                                          featureEng_processes,
                                                          original_dataset.serialize,
                                                          original_dataset_file_path,
                                                          new_dataset_name), countdown=1)

        featureEng.task_id = task.id
        self.featureEngDao.addFeatureEng(featureEng)

        return featureEng

    def deleteFeatureEng(self, featureEng_id, file_directory):
        shutil.rmtree(file_directory)
        return self.featureEngDao.deleteFeatureEng(featureEng_id)

    def updateFeatureEng(self, featureEng):
        return self.featureEngDao.updateFeatureEng(featureEng)

    def queryFeatureEngById(self, featureEng_id):
        featureEng = self.featureEngDao.queryFeatureEngById(featureEng_id)
        if featureEng:
            return featureEng
        else:
            return None

    def queryFeatureEngListByUserId(self, user_id):
        featureEngs = self.featureEngDao.queryFeatureEngListByUserId(user_id)
        if featureEngs:
            return featureEngs
        else:
            return None

    def getFeatureEngFileDirectory(self, featureEng):
        file_directory = os.path.join(current_app.config["SAVE_FE_MODEL_PATH"], featureEng.featureEng_id)

        if not os.path.exists(file_directory):
            return None

        return file_directory

    def getTaskOperateState(self, task_id):
        task = FeatureEngTasks.operate.AsyncResult(task_id)

        if task.state == 'PENDING':
            data = {
                'state': task.state,
                'progress': 0.00,
                'message': 'task pending or not exist'
            }
        elif task.state == 'FAILURE':
            data = {
                'state': task.state,
                'progress': 1.00,
                'message': str(task.info)
            }
        elif task.state == 'SUCCESS':
            data = {
                'state': task.state,
                'progress': 1.00,
                'message': str(task.info)
            }
        else:
            data = {
                'state': task.state,
                # meta 中的数据，通过 task.info.get() 可以获得
                'progress': task.info.get('progress', 0.00),
                'message': task.info.get('message', '')
            }

        return data