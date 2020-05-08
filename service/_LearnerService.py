from dao import LearnerDao
from model import db
from utils.EncryptUtil import get_uid
from celery_tasks.tasks import LearnerTasks
from flask import current_app
import os
import shutil
import pandas as pd


class LearnerService:

    def __init__(self):
        self.learnerDao = LearnerDao(db)

    def addLearner(self, learner, learner_parameters, dataset_file_path):
        learner.learner_id = get_uid()
        learner.train_state = '1'

        task = LearnerTasks.train.apply_async((learner.serialize,
                                               learner_parameters,
                                               dataset_file_path), countdown=1)

        learner.task_id = task.id
        self.learnerDao.addLearner(learner)

        return learner

    def deleteLearner(self, learner_id, file_directory):
        shutil.rmtree(file_directory)
        return self.learnerDao.deleteLearner(learner_id)

    def updateLearner(self, learner):
        return self.learnerDao.updateLearner(learner)

    def queryLearnerById(self, learner_id):
        learner = self.learnerDao.queryLearnerById(learner_id)
        if learner:
            return learner
        else:
            return None

    def queryLearnerListByUserId(self, user_id):
        learners = self.learnerDao.queryLearnerListByUserId(user_id)
        if learners:
            return learners
        else:
            return None

    def getLearnerFileDirectory(self, learner):
        file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner.learner_id)

        if not os.path.exists(file_directory):
            return None

        return file_directory

    def getPredictionFilePath(self, learner):
        file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner.learner_id)
        file_name = 'y_prediction.csv'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            return None

        return file_path

    def getReportFilePath(self, learner):
        file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner.learner_id)
        file_name = 'report.txt'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            return None

        return file_path

    def getPredictionData(self, file_path):
        try:
            data = pd.read_csv(file_path, delimiter=',', header=0, nrows=16, encoding='utf-8')
        except Exception:
            return None

        data = data.to_dict(orient='index')

        data_list = [data[i] for i in range(len(data))]

        return data_list

    def getReportData(self, file_path):
        try:
            with open(file_path, "r") as f:
                data = f.read()
        except Exception:
            return None

        return data

    def getTaskTrainState(self, task_id):
        task = LearnerTasks.train.AsyncResult(task_id)

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