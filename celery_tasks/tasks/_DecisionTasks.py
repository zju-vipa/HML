from celery_tasks.celery import celery_app
from celery_tasks.algorithms import DimReduction, Classification
import pandas as pd
import os
import joblib
from dao import DecisionDao
from model import db, Decision
decisionDao = DecisionDao(db)


def decision_to_bean(decision_json):
    decision_bean = Decision()
    # not task_id
    decision_bean.decision_id = decision_json['decision_id']
    decision_bean.decision_name = decision_json['decision_name']
    decision_bean.decision_type = decision_json['decision_type']
    decision_bean.decision_parameters = decision_json['decision_parameters']
    decision_bean.featureEng_id = decision_json['featureEng_id']
    decision_bean.learner_id = decision_json['learner_id']
    decision_bean.apply_state = decision_json['apply_state']
    decision_bean.dataset_id = decision_json['dataset_id']
    decision_bean.user_id = decision_json['user_id']
    decision_bean.username = decision_json['username']

    return decision_bean


@celery_app.task(bind=True, name='decision.applyFeatureEng')
def apply_featureEng(self, decision_json, decision_parameters, featureEng_id, featureEng_processes, dataset_file_path):

    self.update_state(state='PROCESS', meta={'progress': 0.01, 'message': 'start'})
    decision_bean = decision_to_bean(decision_json)
    decision_id = decision_bean.decision_id

    self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read csv'})
    data = pd.read_csv(dataset_file_path, delimiter=',', header=0, encoding='utf-8')

    self.update_state(state='PROCESS', meta={'progress': 0.10, 'message': 'feature engineering'})
    use_featureEng(data, decision_id, decision_parameters, featureEng_id, featureEng_processes)

    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': 'update train_state'})
    decision_bean.apply_state = '2'
    decisionDao.updateDecision(decision_bean)

    return 'SUCCESS'


def use_featureEng(data, decision_id, decision_parameters, featureEng_id, featureEng_processes):
    processes_num = len(featureEng_processes)
    for process_idx in range(processes_num):

        col_retain = featureEng_processes[int(str(process_idx))]["col_retain"]

        data_retain = pd.DataFrame()
        if col_retain:
            data_retain = data[col_retain]
            data.drop(columns=col_retain, inplace=True)

        data = run_algorithm_featureEng(data, decision_parameters, featureEng_id,
                                        featureEng_processes[int(str(process_idx))])

        data = pd.concat([data, data_retain], axis=1)

    new_dataset_file_path = save_decision_x_transform(data, decision_id)

    return new_dataset_file_path


@celery_app.task(bind=True, name='decision.applyLearner')
def apply_learner(self, decision_json, decision_parameters, learner_id, learner_parameters, dataset_file_path):

    self.update_state(state='PROCESS', meta={'progress': 0.01, 'message': 'start'})
    decision_bean = decision_to_bean(decision_json)
    decision_id = decision_bean.decision_id

    self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read csv'})
    data = pd.read_csv(dataset_file_path, delimiter=',', header=0, encoding='utf-8')

    self.update_state(state='PROCESS', meta={'progress': 0.10, 'message': 'learn'})
    use_learner(data, decision_id, decision_parameters, learner_id, learner_parameters)

    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': 'update train_state'})
    decision_bean.apply_state = '2'
    decisionDao.updateDecision(decision_bean)

    return 'SUCCESS'


def use_learner(data, decision_id, decision_parameters, learner_id, learner_parameters):
    label = learner_parameters["label"]
    if label:
        data_label = data[label]
        data.drop(columns=label, inplace=True)
        y_prediction, report = run_algorithm_learner_with_label(data, data_label, decision_parameters, learner_id, learner_parameters)
        save_decision_y_prediction(y_prediction, decision_id)
        save_decision_report(report, decision_id)
    else:
        y_prediction = run_algorithm_learner_without_label(data, decision_parameters, learner_id, learner_parameters)
        save_decision_y_prediction(y_prediction, decision_id)


@celery_app.task(bind=True, name='decision.applyDecision')
def apply_decision(self, decision_json, decision_parameters, featureEng_id, featureEng_processes,
                   learner_id, learner_parameters, dataset_file_path):

    self.update_state(state='PROCESS', meta={'progress': 0.01, 'message': 'start'})
    decision_bean = decision_to_bean(decision_json)
    decision_id = decision_bean.decision_id

    self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read csv'})
    data = pd.read_csv(dataset_file_path, delimiter=',', header=0, encoding='utf-8')

    self.update_state(state='PROCESS', meta={'progress': 0.10, 'message': 'feature engineering'})
    new_dataset_file_path = use_featureEng(data, decision_id, decision_parameters, featureEng_id, featureEng_processes)

    self.update_state(state='PROCESS', meta={'progress': 0.55, 'message': 'read csv'})
    data = pd.read_csv(new_dataset_file_path, delimiter=',', header=0, encoding='utf-8')

    self.update_state(state='PROCESS', meta={'progress': 0.60, 'message': 'learn'})
    use_learner(data, decision_id, decision_parameters, learner_id, learner_parameters)

    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': 'update train_state'})
    decision_bean.apply_state = '2'
    decisionDao.updateDecision(decision_bean)

    return 'SUCCESS'


def run_algorithm_featureEng(data, decision_parameters, featureEng_id, featureEng_process):
    if featureEng_process['operate_name'] == 'OneHot':
        model_enc = load_featureEng_model('OneHot.pkl', featureEng_id)
        data_onehot = DimReduction.algorithm_OneHot_apply(data, model_enc)
        return data_onehot
    if featureEng_process['operate_name'] == 'PCA':
        model_pca = load_featureEng_model('PCA.pkl', featureEng_id)
        data_pca = DimReduction.algorithm_PCA_apply(data, model_pca)
        return data_pca


def run_algorithm_learner_with_label(data, data_label, decision_parameters, learner_id, learner_parameters):
    if learner_parameters['train_name'] == 'RFC':
        model_enc = load_learner_model('Label.pkl', learner_id)
        model_rfc = load_learner_model('RFC.pkl', learner_id)
        y_prediction, report = Classification.algorithm_RFC_validation(data, data_label, model_enc, model_rfc)
        return y_prediction, report


def run_algorithm_learner_without_label(data, decision_parameters, learner_id, learner_parameters):
    if learner_parameters['train_name'] == 'RFC':
        model_enc = load_learner_model('Label.pkl', learner_id)
        model_rfc = load_learner_model('RFC.pkl', learner_id)
        y_prediction = Classification.algorithm_RFC_test(data, model_enc, model_rfc)
        return y_prediction


def load_featureEng_model(model_file_name, featureEng_id):
    model_directory = os.path.join(celery_app.conf["SAVE_FE_MODEL_PATH"], featureEng_id)
    model_path = os.path.join(model_directory, model_file_name)
    model_object = joblib.load(model_path)
    return model_object


def load_learner_model(model_file_name, learner_id):
    model_directory = os.path.join(celery_app.conf["SAVE_L_MODEL_PATH"], learner_id)
    model_path = os.path.join(model_directory, model_file_name)
    model_object = joblib.load(model_path)
    return model_object


def save_decision_x_transform(x_transform, decision_id):
    file_directory = os.path.join(celery_app.conf["SAVE_D_RESULT_PATH"], decision_id)
    if not os.path.exists(file_directory):
        os.mkdir(file_directory)
    file_path = os.path.join(file_directory, 'x_transform.csv')
    x_transform.to_csv(file_path, header=True, index=False)
    return file_path


def save_decision_y_prediction(y_prediction, decision_id):
    file_directory = os.path.join(celery_app.conf["SAVE_D_RESULT_PATH"], decision_id)
    if not os.path.exists(file_directory):
        os.mkdir(file_directory)
    file_path = os.path.join(file_directory, 'y_prediction.csv')
    y_prediction.to_csv(file_path, header=True, index=False)
    return file_path


def save_decision_report(report, decision_id):
    file_directory = os.path.join(celery_app.conf["SAVE_D_RESULT_PATH"], decision_id)
    if not os.path.exists(file_directory):
        os.mkdir(file_directory)
    file_path = os.path.join(file_directory, 'report.txt')
    with open(file_path, 'w') as f:
        f.write(report)
    return file_path
