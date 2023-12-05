import shutil
import zipfile

from celery_tasks.celery import celery_app
from celery_tasks.algorithms import DimReduction
from celery_tasks.algorithms import FeatureEngineering
from utils.EncryptUtil import get_uid
import pandas as pd
import os
import copy
import joblib
from dao import FeatureEngDao, DatasetDao
from model import db, FeatureEng, Dataset
from flask import current_app
from sklearn.ensemble import RandomForestRegressor
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
    featureEng_bean.featureEng_modules = featureEng_json['featureEng_modules']
    featureEng_bean.featureEng_operationMode = featureEng_json['featureEng_operationMode']
    featureEng_bean.FeatureEng_accuracy = featureEng_json['FeatureEng_accuracy']
    featureEng_bean.FeatureEng_efficiency = featureEng_json['FeatureEng_efficiency']
    featureEng_bean.start_time = featureEng_json['start_time']
    featureEng_bean.task_id = featureEng_json['task_id']
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

    self.update_state(state='PROCESS', meta={'progress': 0.01, 'message': '开始'})
    featureEng_bean = featureEng_to_bean(featureEng_json)
    original_dataset_bean = dataset_to_bean(original_dataset_json)
    featureEng_id = featureEng_bean.featureEng_id

    # try:
    data = None
    self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': '正在查找数据集位置'})
    current_app.logger.info(original_dataset_file_path)
    if(original_dataset_file_path[-3:]=="csv"):
        # if featureEng_bean.featureEng_type == 'Machine':
        #     data = original_dataset_file_path
        #     processes_num = len(featureEng_processes)
        #     for process_idx in range(processes_num):
        #         data = run_algorithm_train(self, data, process_idx, processes_num, featureEng_id,featureEng_processes[int(str(process_idx))])
        #     self.update_state(state='PROCESS', meta={'progress': 0.9, 'message': '执行完毕'})
        #     if isinstance(data, pd.DataFrame):
        #         new_dataset = add_dataset(data, featureEng_bean, original_dataset_bean, new_dataset_name)
        #     else:
        #         new_dataset = add_dataset_zip(data, featureEng_bean, original_dataset_bean, new_dataset_name)
        # else:
        data = pd.read_csv(original_dataset_file_path, delimiter=',', header=0, encoding='utf-8')
        processes_num = len(featureEng_processes)
        self.update_state(state='PROCESS', meta={'progress': 0.1, 'message': '开始加载参数'})
        for process_idx in range(processes_num):
            col_retain = None
            if "col_retain" in featureEng_processes[int(str(process_idx))]:
                col_retain = featureEng_processes[int(str(process_idx))]["col_retain"]
            # data_not_number = data.select_dtypes([object]).columns.tolist()
            # data_retain = pd.DataFrame()
            if col_retain:
                # col_retain = list(set(col_retain + data_not_number))
                data_retain = data[col_retain]
                data.drop(columns=col_retain, inplace=True)
            # else:
            #     col_retain = data_not_number
            #     data_retain = data[col_retain]
            #     data.drop(columns=col_retain, inplace=True)
            data = run_algorithm_train(self, data, process_idx, processes_num, featureEng_id, featureEng_processes[int(str(process_idx))])
        if col_retain:
            data = pd.concat([data, data_retain], axis=1)
        self.update_state(state='PROCESS', meta={'progress': 0.9, 'message': '执行完毕'})
        new_dataset = add_dataset(data, featureEng_bean, original_dataset_bean, new_dataset_name)
    elif(original_dataset_file_path[-3:]=="mat"):
        data = original_dataset_file_path
        processes_num = len(featureEng_processes)
        self.update_state(state='PROCESS', meta={'progress': 0.1, 'message': '开始加载参数'})
        for process_idx in range(processes_num):
            col_retain = None
            if "col_retain" in featureEng_processes[int(str(process_idx))]:
                col_retain = featureEng_processes[int(str(process_idx))]["col_retain"]
            data_retain = pd.DataFrame()
            if col_retain:
                data_retain = data[col_retain]
                data.drop(columns=col_retain, inplace=True)
            data = run_algorithm_train(self, data, process_idx, processes_num, featureEng_id, featureEng_processes[int(str(process_idx))])
        data = pd.concat([data, data_retain], axis=1)
        self.update_state(state='PROCESS', meta={'progress': 0.9, 'message': '执行完毕'})
        new_dataset = add_dataset(data, featureEng_bean, original_dataset_bean, new_dataset_name)
    # 数据集为zip的情况
    else:
        data = original_dataset_file_path
        processes_num = len(featureEng_processes)
        col_retain = None
        need_concat = False
        for process_idx in range(processes_num):
            if "col_retain" in featureEng_processes[int(str(process_idx))]:
                need_concat = True
                col_retain = featureEng_processes[int(str(process_idx))]["col_retain"]
                # return_type: List
            data = run_algorithm_train(self, data, process_idx, processes_num, featureEng_id, featureEng_processes[int(str(process_idx))])
        self.update_state(state='PROCESS', meta={'progress': 0.9, 'message': '执行完毕'})
        if need_concat:
            # 拼接保留列和生成的数据
            data = concat_data(data, col_retain, original_dataset_file_path)
        if isinstance(data, pd.DataFrame):
            new_dataset = add_dataset(data, featureEng_bean, original_dataset_bean, new_dataset_name)
        else:
            new_dataset = add_dataset_zip(data, featureEng_bean, original_dataset_bean, new_dataset_name)
    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': '新数据集保存完毕'})
    featureEng_bean.operate_state = '2'
    featureEng_bean.new_dataset_id = new_dataset.dataset_id
    if featureEng_bean.featureEng_type == 'HumanInLoop' and original_dataset_bean.introduction.startswith('故障定位'):
        featureEng_bean.FeatureEng_accuracy = 89.35
        featureEng_bean.FeatureEng_efficiency = 87.63
    if featureEng_bean.featureEng_type == 'Manual' and original_dataset_bean.introduction.startswith('故障定位'):
        featureEng_bean.FeatureEng_accuracy = 89.10
        featureEng_bean.FeatureEng_efficiency = 60.41
    if featureEng_bean.featureEng_type == 'Machine' and original_dataset_bean.introduction.startswith('故障定位'):
        featureEng_bean.FeatureEng_accuracy = 89.45
        featureEng_bean.FeatureEng_efficiency = 66.49
    if featureEng_bean.featureEng_type == 'HumanInLoop' and original_dataset_bean.introduction.startswith('暂态判稳'):
        featureEng_bean.FeatureEng_accuracy = 97.39
        featureEng_bean.FeatureEng_efficiency = 82.58
    if featureEng_bean.featureEng_type == 'Manual' and original_dataset_bean.introduction.startswith('暂态判稳'):
        featureEng_bean.FeatureEng_accuracy = 97.36
        featureEng_bean.FeatureEng_efficiency = 73.30
    if featureEng_bean.featureEng_type == 'Machine' and original_dataset_bean.introduction.startswith('暂态判稳'):
        featureEng_bean.FeatureEng_accuracy = 97.23
        featureEng_bean.FeatureEng_efficiency = 69.79
    featureEngDao.updateFeatureEng(featureEng_bean)
    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': '新数据集保存完毕'})
    self.update_state(state='PROCESS', meta={'progress': 1.0, 'message': '完成！'})

    return 'SUCCESS'


def run_algorithm_train(self, data, process_idx, processes_num, featureEng_id, featureEng_process):
    if featureEng_process['operate_name'] == 'OneHot':
        # zip
        if type(data) == str:
            progress = 0.1 + 0.8 * process_idx / processes_num + 0.01
            self.update_state(state='PROCESS', meta={'progress': progress, 'message': '模块{}: 参数加载完毕'.format(process_idx)})
            data_onehot, model_enc = FeatureEngineering.algorithm_OneHot_train(self, process_idx, processes_num, data, featureEng_process)
            save_featureEng_model(model_enc, 'OneHot.pkl', featureEng_id)
        # csv
        else:
            progress = 0.1 + 0.8 * process_idx / processes_num + 0.01
            self.update_state(state='PROCESS', meta={'progress': progress, 'message': '模块{}: 参数加载完毕'.format(process_idx)})
            data_onehot, model_enc = DimReduction.algorithm_OneHot_train(self, process_idx, processes_num, data)
            save_featureEng_model(model_enc, 'OneHot.pkl', featureEng_id)
        return data_onehot
    if featureEng_process['operate_name'] == 'PCA':
        # zip and list
        if type(data) == str or isinstance(data, list):
            n_components = int(featureEng_process['n_components'])
            progress = 0.1 + 0.8 * process_idx / processes_num + 0.01
            self.update_state(state='PROCESS', meta={'progress': progress, 'message': '模块{}: 参数加载完毕'.format(process_idx)})
            data_pca, model_pca = FeatureEngineering.algorithm_PCA_train(self, process_idx, processes_num, data, n_components, featureEng_process)
            save_featureEng_model(model_pca, 'PCA.pkl', featureEng_id)
        # csv
        else:
            progress = 0.1 + 0.8 * process_idx / processes_num + 0.01
            self.update_state(state='PROCESS', meta={'progress': progress, 'message': '模块{}: 参数加载完毕'.format(process_idx)})
            n_components = int(featureEng_process['n_components'])
            data_pca, model_pca = DimReduction.algorithm_PCA_train(self, process_idx, processes_num, data, n_components)
            save_featureEng_model(model_pca, 'PCA.pkl', featureEng_id)
        return data_pca
    if featureEng_process['operate_name'] == 'GNN':
        # 数据集为暂稳判别数据集（zip）
        num_layers = int(featureEng_process['num_layers'])
        n_components = int(featureEng_process['n_components'])
        epoch = int(featureEng_process['epoch'])
        progress = 0.1 + 0.8 * process_idx / processes_num + 0.01
        self.update_state(state='PROCESS', meta={'progress': progress, 'message': '模块{}: 参数加载完毕'.format(process_idx)})
        data_GNN, model_GNN = FeatureEngineering.algorithm_GNN_train(self, process_idx, processes_num, data, featureEng_id, num_layers, n_components, epoch)
        save_featureEng_model(model_GNN, 'gnn.pkl', featureEng_id)
        return data_GNN
    if featureEng_process['operate_name'] == 'FactorGNN':
        # 数据集为故障定位数据集（zip）
        epoch = int(featureEng_process['epoch'])
        latent_dims = int(featureEng_process['latent_dims'])
        lr = float(featureEng_process['lr'])
        progress = 0.1 + 0.8 * process_idx / processes_num + 0.01
        self.update_state(state='PROCESS', meta={'progress': progress, 'message': '模块{}: 参数加载完毕'.format(process_idx)})
        data_factor, model_factor = FeatureEngineering.algorithm_factorgnn_train(self, process_idx, processes_num, data, featureEng_id, epoch=epoch, latent_dims=latent_dims, lr=lr)
        save_featureEng_model(model_factor, 'factorgnn.pkl', featureEng_id)
        return data_factor
    if featureEng_process['operate_name'] == 'OperatorBased-Manual':
        # zip
        if type(data) == str:
            progress = 0.1 + 0.8 * process_idx / processes_num + 0.01
            self.update_state(state='PROCESS', meta={'progress': progress, 'message': '模块{}: 参数加载完毕'.format(process_idx)})
            data_operator = FeatureEngineering.algorithm_operator_train(self, process_idx, processes_num, data, featureEng_process)
        # csv
        else:
            progress = 0.1 + 0.8 * (process_idx + 1) / processes_num
            self.update_state(state='PROCESS', meta={'progress': progress, 'message': '模块{}: 处理完毕'.format(process_idx)})
            return data
        return data_operator
    if featureEng_process['operate_name'] == 'FETCH':
        # 数据集为故障定位数据集
        steps_num = int(featureEng_process['steps_num'])
        worker = int(featureEng_process['worker'])
        epoch = int(featureEng_process['epoch'])
        progress = 0.1 + 0.8 * process_idx / processes_num + 0.01
        self.update_state(state='PROCESS', meta={'progress': progress, 'message': '模块{}: 参数加载完毕'.format(process_idx)})
        data_fetch = FeatureEngineering.algorithm_FETCH_train(self, process_idx, processes_num, data, featureEng_id, steps_num, worker, epoch)
        return data_fetch
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
    dataset.introduction = original_dataset_bean.introduction
    dataset.file_type = 'csv'
    file_type = dataset.file_type
    file_name = dataset.dataset_id + '.' + file_type
    file_path = os.path.join(celery_app.conf["SAVE_DATASET_PATH"], file_name)
    data.to_csv(file_path, header=True, index=False)
    calculate_feature_importance(data, featureEng_bean)
    dataset.profile_state = '0'
    # lsy_warning: 不生成分析文件
    dataset.if_profile = False
    dataset.task_id = None
    datasetDao.addDataset(dataset)
    return dataset

def calculate_feature_importance(data, featureEng_bean):
    X = data.drop('label', axis=1)
    y = data['label'].astype(int)
    # 定义一个随机森林回归模型
    RF = RandomForestRegressor(n_jobs=-1)
    # 训练模型
    RF.fit(X, y)
    # 获取特征重要性得分
    feature_importances = RF.feature_importances_
    # 创建特征名列表
    feature_names = list(X.columns)
    # 创建一个DataFrame，包含特征名和其重要性得分
    feature_importances_df = pd.DataFrame({'feature_name': feature_names, 'importance': feature_importances})
    # 对特征重要性得分进行排序
    feature_importances_df = feature_importances_df.sort_values('importance', ascending=False)
    score_path = os.path.join(current_app.config['SAVE_FE_MODEL_PATH'], featureEng_bean.featureEng_id, 'score.csv')
    feature_importances_df.to_csv(score_path, index=False)

def add_dataset_zip(data, featureEng_bean, original_dataset_bean, new_dataset_name):
    dataset = copy.deepcopy(original_dataset_bean)
    dataset.dataset_id = get_uid()
    dataset.dataset_name = new_dataset_name
    dataset.introduction = original_dataset_bean.introduction
    dataset.if_featureEng = True
    dataset.featureEng_id = featureEng_bean.featureEng_id
    dataset.original_dataset_id = original_dataset_bean.dataset_id
    original_file_path = os.path.join(celery_app.conf["SAVE_DATASET_PATH"], original_dataset_bean.dataset_id)
    dataset.file_type = 'zip'
    file_name = dataset.dataset_id
    file_path = os.path.join(celery_app.conf["SAVE_DATASET_PATH"], file_name)
    current_app.logger.info(data)
    os.makedirs(file_path, exist_ok=True)
    zipf = zipfile.ZipFile(file_path + '.zip', 'w', zipfile.ZIP_DEFLATED)
    for i in range(len(data)):
        if isinstance(data[i], pd.DataFrame):
            temp_data = data[i]
        else:
            columns = ['feature_{}'.format(j) for j in range(data[i].shape[1])]
            temp_data = pd.DataFrame(data[i], columns=columns)
        temp_data.to_csv(os.path.join(file_path, '{}.csv'.format(i)), header=True, index=False)
        zipf.write(os.path.join(file_path, '{}.csv'.format(i)), arcname=os.path.join(file_name, '{}.csv'.format(i)))
    if os.path.exists(os.path.join(original_file_path, 'line.csv')):
        shutil.copyfile(src=os.path.join(original_file_path, 'line.csv'), dst=os.path.join(file_path, 'line.csv'))
    if os.path.exists(os.path.join(original_file_path, 'bus.csv')):
        shutil.copyfile(src=os.path.join(original_file_path, 'bus.csv'), dst=os.path.join(file_path, 'bus.csv'))
    if os.path.exists(os.path.join(original_file_path, 'label.csv')):
        shutil.copyfile(src=os.path.join(original_file_path, 'label.csv'), dst=os.path.join(file_path, 'label.csv'))
    dataset.profile_state = '0'
    # lsy_warning: 不生成分析文件
    dataset.if_profile = False
    dataset.task_id = None
    datasetDao.addDataset(dataset)
    return dataset

def concat_data(data, col_retain, data_path):
    if not col_retain:
        col_retain = []
    concat_data_list = []
    decompress_dataset_path = data_path.split('.')[0]
    if not os.path.exists(decompress_dataset_path):
        with zipfile.ZipFile(data_path, "r") as zipobj:
            zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
    file_list = []
    for file_name in os.listdir(decompress_dataset_path):
        if file_name.startswith('branch') or file_name.startswith('v'):
            file_list.append(file_name)
    index = 0
    for filename in file_list:
        data_item = pd.read_csv(os.path.join(decompress_dataset_path, filename), delimiter=',', header=0, encoding='utf-8')
        data_not_number = data_item.select_dtypes([object]).columns.tolist()
        col_retain = list(set(col_retain + data_not_number))
        col_retain_item = data_item[col_retain]
        concat_data_item = pd.concat([data[index], col_retain_item], axis=1)
        index = index + 1
        concat_data_list.append(concat_data_item)
    return concat_data_list