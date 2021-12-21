from celery_tasks.celery import celery_app
from celery_tasks.algorithms import Classification
from celery_tasks.algorithms import _Reinforcementlearning
from celery_tasks.algorithms import learn_with_label
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

def run_algorithm_reinforcement_learning(learner_id,learner_parameters):
    current_app.logger.info("run_algorithm_reinforcement_learning begin")
    if learner_parameters['train_name'] == 'HML_RL':
        current_app.logger.info("run_algorithm_reinforcement_learning HML_RL")
        _Reinforcementlearning.algorithm_HML_RL_train(learner_id)

def run_algorithm_train_with_label(data, data_label, learner_id, learner_parameters): # if train_name is GNN, no need for data_label and data is datapath
    if learner_parameters['train_name'] == 'RFC':
        n_estimators = learner_parameters['n_estimators']
        model_enc, model_rfc, y_prediction, report = Classification.algorithm_RFC_train(data, data_label, n_estimators)
        save_learner_model(model_enc, 'Label.pkl', learner_id)
        save_learner_model(model_rfc, 'RFC.pkl', learner_id)
        save_learner_y_prediction(y_prediction, learner_id)
        save_learner_report(report, learner_id)
    if learner_parameters['train_name'] == 'GNN_in_learner':
        current_app.logger.info("GNN_in_learner data path")
        current_app.logger.info(data  )
        n_components = learner_parameters['n_components']
        epoch = learner_parameters['epoch']
        model_GNN = learn_with_label.algorithm_GNN_train(data, n_components, epoch)
        save_learner_model(model_GNN, 'GNN_in_learner.pkl', learner_id)


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


if __name__ == '__main__':
    _Reinforcementlearning.algorithm_HML_RL_train()