from celery_tasks.celery import celery_app
from celery_tasks.algorithms import DimReduction
from utils.EncryptUtil import get_uid
from flask import current_app
import pandas as pd
import os
import copy
import joblib
from dao import FeatureEngDao, DatasetDao
from model import db, FeatureEng, Dataset
datasetDao = DatasetDao(db)
featureEngDao = FeatureEngDao(db)


def featureEng_to_bean(featureEng_json):
    featureEng_bean = FeatureEng()
    # not task_id
    featureEng_bean.featureEng_id = featureEng_json['featureEng_id']
    featureEng_bean.featureEng_name = featureEng_json['featureEng_name']
    featureEng_bean.featureEng_type = featureEng_json['featureEng_type']
    featureEng_bean.featureEng_processes = featureEng_json['featureEng_processes']
    featureEng_bean.operate_state = featureEng_json['operate_state']
    featureEng_bean.new_dataset_id = featureEng_json['new_dataset_id']
    featureEng_bean.original_dataset_id = featureEng_json['original_dataset_id']
    featureEng_bean.user_id = featureEng_json['user_id']
    featureEng_bean.username = featureEng_json['username']

    return featureEng_bean


def dataset_to_bean(dataset_json):
    dataset_bean = Dataset()
    # not task_id
    dataset_bean.dataset_id = dataset_json['dataset_id']
    dataset_bean.dataset_name = dataset_json['dataset_name']
    dataset_bean.file_type = dataset_json['file_type']
    dataset_bean.if_profile = dataset_json['if_profile']
    dataset_bean.profile_state = dataset_json['profile_state']
    dataset_bean.if_public = dataset_json['if_public']
    dataset_bean.introduction = dataset_json['introduction']
    dataset_bean.if_featureEng = dataset_json['if_featureEng']
    dataset_bean.featureEng_id = dataset_json['featureEng_id']
    dataset_bean.original_dataset_id = dataset_json['original_dataset_id']
    dataset_bean.user_id = dataset_json['user_id']
    dataset_bean.username = dataset_json['username']

    return dataset_bean


@celery_app.task(bind=True, name='featureEng.operate')
def operate(self, featureEng_json, featureEng_processes, original_dataset_json,
                  original_dataset_file_path, new_dataset_name):

    self.update_state(state='PROCESS', meta={'progress': 0.01, 'message': 'start'})
    featureEng_bean = featureEng_to_bean(featureEng_json)
    original_dataset_bean = dataset_to_bean(original_dataset_json)
    featureEng_id = featureEng_bean.featureEng_id

    # try:
    data = None
    self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read csv'})
    current_app.logger.info(original_dataset_file_path)
    if(original_dataset_file_path[-3:]=="csv"):
        data = pd.read_csv(original_dataset_file_path, delimiter=',', header=0, encoding='utf-8')
    elif(original_dataset_file_path[-3:]=="mat"):
        data = original_dataset_file_path
    processes_num = len(featureEng_processes)
    for process_idx in range(processes_num):
        progress = round(0.1 + process_idx / processes_num * 0.85, 2)
        message = featureEng_processes[int(str(process_idx))]['operate_name'] + 'operating'
        self.update_state(state='PROCESS', meta={'progress': progress, 'message': message})  # need update

        col_retain = featureEng_processes[int(str(process_idx))]["col_retain"]

        data_retain = pd.DataFrame()
        if col_retain:
            data_retain = data[col_retain]
            data.drop(columns=col_retain, inplace=True)

        data = run_algorithm_train(data, featureEng_id, featureEng_processes[int(str(process_idx))])

        data = pd.concat([data, data_retain], axis=1)

    new_dataset = add_dataset(data, featureEng_bean, original_dataset_bean, new_dataset_name)

    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': 'update operate_state'})
    featureEng_bean.operate_state = '2'
    featureEng_bean.new_dataset_id = new_dataset.dataset_id
    featureEngDao.updateFeatureEng(featureEng_bean)

    # except Exception:
    #     self.update_state(state='FAILURE', meta={'progress': 1.0, 'message': 'failure'})
    #     featureEng_bean.operate_state = '3'F
    #     featureEngDao.updateFeatureEng(featureEng_bean)
    #     return 'FAILURE'

    return 'SUCCESS'


def run_algorithm_train(data, featureEng_id, featureEng_process):
    if featureEng_process['operate_name'] == 'OneHot':
        data_onehot, model_enc = DimReduction.algorithm_OneHot_train(data)
        save_featureEng_model(model_enc, 'OneHot.pkl', featureEng_id)
        return data_onehot
    if featureEng_process['operate_name'] == 'PCA':
        n_components = featureEng_process['n_components']
        data_pca, model_pca = DimReduction.algorithm_PCA_train(data, n_components)
        save_featureEng_model(model_pca, 'PCA.pkl', featureEng_id)
        return data_pca
    if featureEng_process['operate_name'] == 'GNN':
        current_app.logger.info("GNN data path")
        current_app.logger.info(data  )
        n_components = featureEng_process['n_components']
        epoch = featureEng_process['epoch']
        data_GNN, model_GNN = DimReduction.algorithm_GNN_train(data, n_components, epoch) # may need some ohter parameter
        save_featureEng_model(model_GNN, 'GNN.pkl', featureEng_id)
        return data_GNN

    return data


def save_featureEng_model(model_object, model_file_name, featureEng_id):
    model_directory = os.path.join(celery_app.conf["SAVE_FE_MODEL_PATH"], featureEng_id)
    if not os.path.exists(model_directory):
        os.mkdir(model_directory)
    model_path = os.path.join(model_directory, model_file_name)
    joblib.dump(model_object, model_path)
    return model_path


def add_dataset(data, featureEng_bean, original_dataset_bean, new_dataset_name):
    dataset = copy.deepcopy(original_dataset_bean)
    dataset.dataset_id = get_uid()
    dataset.dataset_name = new_dataset_name
    dataset.if_featureEng = True
    dataset.featureEng_id = featureEng_bean.featureEng_id
    dataset.original_dataset_id = original_dataset_bean.dataset_id

    file_type = dataset.file_type
    file_name = dataset.dataset_id + '.' + file_type
    file_path = os.path.join(celery_app.conf["SAVE_DATASET_PATH"], file_name)
    data.to_csv(file_path, header=True, index=False)

    dataset.profile_state = '0'
    # lsy_warning: 不生成分析文件
    dataset.if_profile = False
    dataset.task_id = None
    datasetDao.addDataset(dataset)

    return dataset
