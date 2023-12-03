import zipfile

import pandas as pd
from celery_tasks.algorithms._FeatureEng_utils.factor import factorgnn as factor
from celery_tasks.algorithms._FeatureEng_utils.gcpool import graphcnn as gnn
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA
from flask import current_app
import os


def algorithm_GNN_train(self, process_idx, processes_num, data_path, featureEng_id, num_layers, n_components, epoch):
    progress = 0.1 + 0.8 * process_idx / processes_num + 0.05
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 加载模型'.format(process_idx + 1)})
    decompress_dataset_path = data_path.split('.')[0]
    if not os.path.exists(decompress_dataset_path):
        with zipfile.ZipFile(data_path, "r") as zipobj:
            zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
    result_path = os.path.join(current_app.config['SAVE_FE_MODEL_PATH'], featureEng_id, 'result')
    graphcnn = gnn.graphcnn(decompress_dataset_path, result_path, num_layers=num_layers, n_components=n_components,
                            epoch=epoch)
    progress = 0.1 + 0.8 * process_idx / processes_num + 0.8 * 0.6 / processes_num
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 训练模型'.format(process_idx + 1)})
    model_gnn = graphcnn.main()
    progress = 0.1 + 0.8 * (process_idx + 1) / processes_num - 0.05
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 特征学习'.format(process_idx + 1)})
    data_factor = graphcnn.Dim_Re(model_gnn, decompress_dataset_path)
    return data_factor, model_gnn


def algoritm_GNN_apply(data_path, model_GNN):
    decompress_dataset_path = data_path.split('.')[0]
    if not os.path.exists(decompress_dataset_path):
        with zipfile.ZipFile(data_path, "r") as zipobj:
            zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
    data_GNN = pd.DataFrame(model_GNN.transform(decompress_dataset_path))
    return data_GNN


def algorithm_factorgnn_train(self, process_idx, processes_num, data_path, featureEng_id, epoch, latent_dims,
                              lr):
    progress = 0.1 + 0.8 * process_idx / processes_num + 0.05
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 加载模型'.format(process_idx + 1)})
    decompress_dataset_path = data_path.split('.')[0]
    if not os.path.exists(decompress_dataset_path):
        with zipfile.ZipFile(data_path, "r") as zipobj:
            zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
    result_path = os.path.join(current_app.config['SAVE_FE_MODEL_PATH'], featureEng_id, 'result')
    factorgnn = factor.factorgnn(data_path=decompress_dataset_path, result_path=result_path, epoch=epoch,
                                 latent_dims=latent_dims, lr=lr)
    progress = 0.1 + 0.8 * process_idx / processes_num + 0.8 * 0.6 / processes_num
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 训练模型'.format(process_idx + 1)})
    model_factor = factorgnn.main()
    progress = 0.1 + 0.8 * (process_idx + 1) / processes_num - 0.05
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 特征解耦'.format(process_idx + 1)})
    data_factor = factorgnn.feature_decoupling(model_factor, decompress_dataset_path)
    return data_factor, model_factor


def algorithm_factorgnn_apply(data_path, model_factor):
    decompress_dataset_path = data_path.split('.')[0]
    if not os.path.exists(decompress_dataset_path):
        with zipfile.ZipFile(data_path, "r") as zipobj:
            zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
    data_factor = pd.DataFrame(model_factor.transform(decompress_dataset_path))
    return data_factor


def algorithm_OneHot_train(self, process_idx, processes_num, data_path, featureEng_process):
    progress = 0.1 + 0.8 * process_idx / processes_num + 0.8 * 0.6 / processes_num
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 编码器初始化'.format(process_idx + 1)})
    model_enc = OneHotEncoder(sparse=False)
    decompress_dataset_path = data_path.split('.')[0]
    if not os.path.exists(decompress_dataset_path):
        with zipfile.ZipFile(data_path, "r") as zipobj:
            zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
    data_list = []
    file_list = []
    for file_name in os.listdir(decompress_dataset_path):
        if file_name.startswith('branch') or file_name.startswith('v'):
            file_list.append(file_name)
    progress = 0.1 + 0.8 * process_idx / processes_num + 0.8 * 0.9 / processes_num
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 生成数据'.format(process_idx + 1)})
    for filename in file_list:
        data_item = pd.read_csv(os.path.join(decompress_dataset_path, filename), delimiter=',', header=0,
                                encoding='utf-8')
        col_retain = None
        if "col_retain" in featureEng_process:
            col_retain = featureEng_process["col_retain"]
        data_not_number = data_item.select_dtypes([object]).columns.tolist()
        if col_retain:
            col_retain = list(set(col_retain + data_not_number))
            data_item.drop(columns=col_retain, inplace=True)
        else:
            col_retain = data_not_number
            data_item.drop(columns=col_retain, inplace=True)
        model_enc.fit(data_item)
        data_onehot = pd.DataFrame(model_enc.transform(data_item))
        data_list.append(data_onehot)
    return data_list, model_enc


def algorithm_OneHot_apply(data_path, model_enc):
    decompress_dataset_path = data_path.split('.')[0]
    if not os.path.exists(decompress_dataset_path):
        with zipfile.ZipFile(data_path, "r") as zipobj:
            zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
    data_onehot = pd.DataFrame(model_enc.transform(decompress_dataset_path))
    return data_onehot


def algorithm_operator_train(self, process_idx, processes_num, data_path, featureEng_process):
    data_list = []
    file_list = []
    decompress_dataset_path = data_path.split('.')[0]
    if not os.path.exists(decompress_dataset_path):
        with zipfile.ZipFile(data_path, "r") as zipobj:
            zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
    for file_name in os.listdir(decompress_dataset_path):
        if file_name.startswith('branch') or file_name.startswith('v'):
            file_list.append(file_name)
    progress = 0.1 + 0.8 * process_idx / processes_num + 0.8 * 0.9 * process_idx / processes_num
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 生成数据'.format(process_idx + 1)})
    for filename in file_list:
        data = pd.read_csv(os.path.join(decompress_dataset_path, filename), delimiter=',', header=0, encoding='utf-8')
        col_retain = None
        if "col_retain" in featureEng_process:
            col_retain = featureEng_process["col_retain"]
        data_not_number = data.select_dtypes([object]).columns.tolist()
        if col_retain:
            col_retain = list(set(col_retain + data_not_number))
            data.drop(columns=col_retain, inplace=True)
        else:
            col_retain = data_not_number
            data.drop(columns=col_retain, inplace=True)
        data_list.append(data)
    return data_list


def algorithm_PCA_train(self, process_idx, processes_num, data, n_components, feature_process):
    progress = 0.1 + 0.8 * process_idx / processes_num + 0.8 * 0.6 / processes_num
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 模型初始化'.format(process_idx + 1)})
    model_pca = PCA(n_components=n_components)
    data_list = []
    dataset_length = 0
    # data - file_path
    if type(data) == str:
        decompress_dataset_path = data.split('.')[0]
        if not os.path.exists(decompress_dataset_path):
            with zipfile.ZipFile(data, "r") as zipobj:
                zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
        file_list = []
        for file_name in os.listdir(decompress_dataset_path):
            if file_name.startswith('branch') or file_name.startswith('v'):
                file_list.append(file_name)
        total_data = pd.DataFrame()
        for filename in file_list:
            data_item = pd.read_csv(os.path.join(decompress_dataset_path, filename), delimiter=',', header=0,
                                    encoding='utf-8')
            file_length = data_item.shape[0]
            total_data = pd.concat([total_data, data_item])
        dataset_length = len(file_list)
    #  data - list
    else:
        total_data = pd.DataFrame()
        for i in range(len(data)):
            data_item = data[i]
            file_length = data_item.shape[0]
            total_data = pd.concat([total_data, data_item])
        dataset_length = len(data)
    progress = 0.1 + 0.8 * process_idx / processes_num + 0.8 * 0.9 / processes_num
    self.update_state(state='PROCESS',
                      meta={'progress': progress, 'message': '模块{}： 生成数据'.format(process_idx + 1)})
    model_pca.fit(total_data)
    data_pca = pd.DataFrame(model_pca.transform(total_data))
    for i in range(dataset_length):
        data_temp = data_pca.iloc[i * file_length:(i + 1) * file_length, :]
        data_temp = data_temp.reset_index(drop=True)
        data_list.append(data_temp)
    return data_list, model_pca


def algorithm_PCA_apply(data, model_pca):
    data_pca = pd.DataFrame(model_pca.transform(data))
    return data_pca