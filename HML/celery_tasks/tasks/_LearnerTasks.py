from celery_tasks.celery import celery_app
from celery_tasks.algorithms import Classification
from celery_tasks.algorithms import _Reinforcementlearning
import pandas as pd
import os
import joblib
from dao import LearnerDao
from model import db, Learner
from flask import current_app
learnerDao = LearnerDao(db)


def learner_to_bean(learner_json):
    learner_bean = Learner()
    # not task_id
    learner_bean.learner_id = learner_json['learner_id']
    learner_bean.learner_name = learner_json['learner_name']
    learner_bean.learner_type = learner_json['learner_type']
    learner_bean.learner_parameters = learner_json['learner_parameters']
    learner_bean.train_state = learner_json['train_state']
    learner_bean.dataset_id = learner_json['dataset_id']
    learner_bean.user_id = learner_json['user_id']
    learner_bean.username = learner_json['username']
    learner_bean.action = learner_json['action']
    # not action
    learner_bean.test_state = learner_json['test_state']

    return learner_bean


@celery_app.task(bind=True, name='learner.train')
def train(self, learner_json, learner_parameters, dataset_file_path):

    self.update_state(state='PROCESS', meta={'progress': 0.01, 'message': 'start'})
    learner_bean = learner_to_bean(learner_json)
    learner_id = learner_bean.learner_id

    # try:
    self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read csv'})
    data = pd.read_csv(dataset_file_path, delimiter=',', header=0, encoding='utf-8')

    self.update_state(state='PROCESS', meta={'progress': 0.10, 'message': 'training'})

    label = learner_parameters["label"]
    if label:
        data_label = data[label]
        data.drop(columns=label, inplace=True)
        run_algorithm_train_with_label(data, data_label, learner_id, learner_parameters)
    else:
        current_app.logger.info("learnerTask train no label")
        run_algorithm_reinforcement_learning(learner_id, learner_parameters)
        # todo  later maybe other algorithm need to add

    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': 'update train_state'})
    learner_bean.train_state = '2'
    learnerDao.updateLearner(learner_bean)

    # except Exception:
    #     self.update_state(state='FAILURE', meta={'progress': 1.0, 'message': 'failure'})
    #     learner_bean.train_state = '3'
    #     learnerDao.updateLearner(learner_bean)
    #     return 'FAILURE'

    return 'SUCCESS'


@celery_app.task(bind=True, name='learner.test')
def test(self, learner_json, learner_parameters, dataset_file_path):
    # print("test 0")
    self.update_state(state='PROCESS', meta={'progress': 0.01, 'message': 'start'})
    learner_bean = learner_to_bean(learner_json)
    learner_id = learner_bean.learner_id
    # print("test 1")
    # try:
    self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read csv'})
    data = pd.read_csv(dataset_file_path, delimiter=',', header=0, encoding='utf-8')

    self.update_state(state='PROCESS', meta={'progress': 0.10, 'message': 'testing'})
    # print("test 2")

    label = learner_parameters["label"]
    if label:
        data_label = data[label]
        data.drop(columns=label, inplace=True)
        run_algorithm_train_with_label(data, data_label, learner_id, learner_parameters)
    else:
        current_app.logger.info("learnerTask train no label")
        run_algorithm_reinforcement_learning_test(learner_id, learner_parameters)
        # todo  later maybe other algorithm need to add

    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': 'update test_state'})
    # print("test 3")
    learner_bean.test_state = '2'
    learnerDao.updateLearner(learner_bean)
    self.update_state(state='SUCCESS', meta={'progress': 1, 'message': 'update test_state'})
    # print("test 4")

    return 'SUCCESS'


def run_algorithm_reinforcement_learning_test(learner_id,learner_parameters):
    current_app.logger.info("run_algorithm_reinforcement_learning_test begin")
    if learner_parameters['train_name'] == 'HML_RL':
        current_app.logger.info("run_algorithm_reinforcement_learning_test HML_RL")
        _Reinforcementlearning.algorithm_HML_RL_test(learner_id)
    if learner_parameters['train_name'] == 'HML_ML':
        current_app.logger.info("run_algorithm_reinforcement_learning_test HML_ML")
        _Reinforcementlearning.algorithm_HML_RL_test_ML(learner_id)

def run_algorithm_reinforcement_learning(learner_id,learner_parameters):
    current_app.logger.info("run_algorithm_reinforcement_learning begin")
    if learner_parameters['train_name'] == 'HML_RL':
        current_app.logger.info("run_algorithm_reinforcement_learning HML_RL")
        _Reinforcementlearning.algorithm_HML_RL_train(learner_id)
    elif learner_parameters['train_name'] == 'HML_ML':
        current_app.logger.info("run_algorithm_reinforcement_learning HML_ML")
        _Reinforcementlearning.algorithm_HML_RL_train_ML(learner_id)
        
def run_algorithm_train_with_label(data, data_label, learner_id, learner_parameters):
    if learner_parameters['train_name'] == 'RFC':
        n_estimators = learner_parameters['n_estimators']
        model_enc, model_rfc, y_prediction, report = Classification.algorithm_RFC_train(data, data_label, n_estimators)
        save_learner_model(model_enc, 'Label.pkl', learner_id)
        save_learner_model(model_rfc, 'RFC.pkl', learner_id)
        save_learner_y_prediction(y_prediction, learner_id)
        save_learner_report(report, learner_id)
    # 自填加
    elif learner_parameters['train_name'] == 'SVM':
        n_estimators = learner_parameters['n_estimators']
        model_enc, model_svm, y_prediction, report = Classification.algorithm_SVM_train(data, data_label, n_estimators)
        save_learner_model(model_enc, 'Label.pkl', learner_id)
        save_learner_model(model_svm, 'RFC.pkl', learner_id)
        save_learner_y_prediction(y_prediction, learner_id)
        save_learner_report(report, learner_id)
    elif learner_parameters['train_name'] == 'LR':
        n_estimators = learner_parameters['n_estimators']
        model_enc, model_lr, y_prediction, report = Classification.algorithm_LR_train(data, data_label, n_estimators)
        save_learner_model(model_enc, 'Label.pkl', learner_id)
        save_learner_model(model_lr, 'RFC.pkl', learner_id)
        save_learner_y_prediction(y_prediction, learner_id)
        save_learner_report(report, learner_id)


def save_learner_model(model_object, model_file_name, learner_id):
    model_directory = os.path.join(celery_app.conf["SAVE_L_MODEL_PATH"], learner_id)
    if not os.path.exists(model_directory):
        os.mkdir(model_directory)
    model_path = os.path.join(model_directory, model_file_name)
    joblib.dump(model_object, model_path)
    return model_path


def save_learner_y_prediction(y_prediction, learner_id):
    file_directory = os.path.join(celery_app.conf["SAVE_L_MODEL_PATH"], learner_id)
    file_path = os.path.join(file_directory, 'y_prediction.csv')
    y_prediction.to_csv(file_path, header=True, index=False)
    return file_path


def save_learner_report(report, learner_id):
    file_directory = os.path.join(celery_app.conf["SAVE_L_MODEL_PATH"], learner_id)
    file_path = os.path.join(file_directory, 'report.txt')
    with open(file_path, 'w') as f:
        f.write(report)
    return file_path


# if __name__ == '__main__':
#     _Reinforcementlearning.algorithm_HML_RL_train()