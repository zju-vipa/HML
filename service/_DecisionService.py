from dao import DecisionDao
from model import db
from utils.EncryptUtil import get_uid
from celery_tasks.tasks import DecisionTasks
from flask import current_app
import os
import pandas as pd
import shutil


class DecisionService:

    def __init__(self):
        self.decisionDao = DecisionDao(db)

    def applyFeatureEng(self, decision, decision_parameters, featureEng_id, featureEng_processes, dataset_file_path):
        decision.decision_id = get_uid()
        decision.apply_state = '1'

        task = DecisionTasks.apply_featureEng.apply_async((decision.serialize,
                                                           decision_parameters,
                                                           featureEng_id,
                                                           featureEng_processes,
                                                           dataset_file_path), countdown=1)

        decision.task_id = task.id
        self.decisionDao.addDecision(decision)

        return decision

    def applyLearner(self, decision, decision_parameters, learner_id, learner_parameters, dataset_file_path):
        decision.decision_id = get_uid()
        decision.apply_state = '1'

        task = DecisionTasks.apply_learner.apply_async((decision.serialize,
                                                        decision_parameters,
                                                        learner_id,
                                                        learner_parameters,
                                                        dataset_file_path), countdown=1)

        decision.task_id = task.id
        self.decisionDao.addDecision(decision)

        return decision

    def applyDecision(self, decision, decision_parameters, featureEng_id, featureEng_processes,
                      learner_id, learner_parameters, dataset_file_path):
        decision.decision_id = get_uid()
        decision.apply_state = '1'

        task = DecisionTasks.apply_decision.apply_async((decision.serialize,
                                                         decision_parameters,
                                                         featureEng_id,
                                                         featureEng_processes,
                                                         learner_id,
                                                         learner_parameters,
                                                         dataset_file_path), countdown=1)

        decision.task_id = task.id
        self.decisionDao.addDecision(decision)

        return decision

    def deleteDecision(self, decision_id, file_directory):
        shutil.rmtree(file_directory)
        return self.decisionDao.deleteDecision(decision_id)

    def updateDecision(self, decision):
        return self.decisionDao.updateDecision(decision)

    def queryDecisionById(self, decision_id):
        decision = self.decisionDao.queryDecisionById(decision_id)
        if decision:
            return decision
        else:
            return None

    def queryDecisionListByUserId(self, user_id):
        decisions = self.decisionDao.queryDecisionListByUserId(user_id)
        if decisions:
            return decisions
        else:
            return None

    def getDecisionFileDirectory(self, decision):
        file_directory = os.path.join(current_app.config["SAVE_D_RESULT_PATH"], decision.decision_id)

        if not os.path.exists(file_directory):
            return None

        return file_directory

    def getTransformFilePath(self, decision):
        file_directory = os.path.join(current_app.config["SAVE_D_RESULT_PATH"], decision.decision_id)
        file_name = 'x_transform.csv'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            return None

        return file_path

    def getPredictionFilePath(self, decision):
        file_directory = os.path.join(current_app.config["SAVE_D_RESULT_PATH"], decision.decision_id)
        file_name = 'y_prediction.csv'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            return None

        return file_path

    def getReportFilePath(self, decision):
        file_directory = os.path.join(current_app.config["SAVE_D_RESULT_PATH"], decision.decision_id)
        file_name = 'report.txt'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            return None

        return file_path

    def getTransformData(self, file_path):
        try:
            data = pd.read_csv(file_path, delimiter=',', header=0, nrows=16, encoding='utf-8')
        except Exception:
            return None

        data = data.to_dict(orient='index')

        data_list = [data[i] for i in range(len(data))]

        return data_list

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

    def getTaskApplyState(self, task_id, mode):
        if mode == 'featureEng':
            task = DecisionTasks.apply_featureEng.AsyncResult(task_id)
        elif mode == 'learner':
            task = DecisionTasks.apply_learner.AsyncResult(task_id)
        elif mode == 'decision':
            task = DecisionTasks.apply_decision.AsyncResult(task_id)
        else:
            return None

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