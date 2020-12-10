from celery_tasks.celery import celery_app
import pandas as pd
import os
import joblib
from dao import PowerNetDatasetDao
from model import db, PowerNetDataset
from utils.data_generation import emergency_data_generation_a
from utils.network import read_examples
power_net_datasetDao = PowerNetDatasetDao(db)

def power_net_dataset_to_bean(power_net_dataset_json):
    power_net_dataset_bean = PowerNetDataset()
    # not task_id
    power_net_dataset_bean.power_net_dataset_id = power_net_dataset_json['power_net_dataset_id']
    power_net_dataset_bean.power_net_dataset_name = power_net_dataset_json['power_net_dataset_name']
    power_net_dataset_bean.power_net_dataset_type = power_net_dataset_json['power_net_dataset_type']
    # power_net_dataset_bean.power_net_dataset_parameters = power_net_dataset_json['power_net_dataset_parameters']
    power_net_dataset_bean.power_net_dataset_description = power_net_dataset_json['power_net_dataset_description']
    power_net_dataset_bean.init_net_name = power_net_dataset_json['init_net_name']
    power_net_dataset_bean.disturb_src_type_list = power_net_dataset_json['disturb_src_type_list']
    power_net_dataset_bean.disturb_n_var = power_net_dataset_json['disturb_n_var']
    power_net_dataset_bean.disturb_radio = power_net_dataset_json['disturb_radio']
    power_net_dataset_bean.disturb_n_sample = power_net_dataset_json['disturb_n_sample']
    power_net_dataset_bean.start_time = power_net_dataset_json['start_time']
    power_net_dataset_bean.generate_state = power_net_dataset_json['generate_state']
    power_net_dataset_bean.user_id = power_net_dataset_json['user_id']
    power_net_dataset_bean.username = power_net_dataset_json['username']
    
    return power_net_dataset_bean


@celery_app.task(bind=True, name='power_net_dataset.generate')
def generate(self, power_net_dataset_json, file_path):
    # 开始
    self.update_state(state='PROCESS', meta={'progress': 0.01, 'message': 'start'})
    power_net_dataset_bean = power_net_dataset_to_bean(power_net_dataset_json)
    power_net_dataset_id = power_net_dataset_bean.power_net_dataset_id

    # 扰动参数转换
    self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read disturb params'})
    # vars ([dict], optional): [扰动源类型]. Defaults to None.
    #                                 such as: {'gen':['p_mw', 'vm_pu'], 'load': ['p_mw', 'q_mvar']}
    pn_vars = {'gen': [], 'load': []}
    disturb_src_type_list = power_net_dataset_bean.disturb_src_type_list.split(',')
    if 'gen_p' in disturb_src_type_list:
        pn_vars['gen'].append('p_mw')
    if 'gen_v' in disturb_src_type_list:
        pn_vars['gen'].append('vm_pu')
    if 'load_p' in disturb_src_type_list:
        pn_vars['load'].append('p_mw')
    if 'load_q' in disturb_src_type_list:
        pn_vars['load'].append('q_mvar')
    # 初始电网样例
    init_net = read_examples(power_net_dataset_bean.init_net_name)

    # 生成电网数据集并且计算潮流结果
    self.update_state(state='PROCESS', meta={'progress': 0.10, 'message': 'generating'})
    res = emergency_data_generation_a(vars=pn_vars, if_random=True, n_var=power_net_dataset_bean.disturb_n_var,
                                      net=init_net, radio=power_net_dataset_bean.disturb_radio,
                                      n_sample=power_net_dataset_bean.disturb_n_sample)
    res.drop(columns=['net'], axis=1, inplace=True)
    # 保存结果
    self.update_state(state='PROCESS', meta={'progress': 0.90, 'message': 'saving result'})
    # file_directory = os.path.join(celery_app.conf["SAVE_PN_DATASET_PATH"], power_net_dataset_id)
    # file_path = os.path.join(file_directory, 'pn_power_flow.csv')
    res.to_csv(file_path, header=True, index=False)

    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': 'update generate_state'})
    power_net_dataset_bean.generate_state = '2'
    power_net_datasetDao.updatePowerNetDataset(power_net_dataset_bean)

    # except Exception:
    #     self.update_state(state='FAILURE', meta={'progress': 1.0, 'message': 'failure'})
    #     power_net_dataset_bean.generate_state = '3'
    #     power_net_datasetDao.updatePowerNetDataset(power_net_dataset_bean)
    #     return 'FAILURE'

    return 'SUCCESS'


def run_algorithm_train_with_label(data, data_label, power_net_dataset_id, power_net_dataset_parameters):
    if power_net_dataset_parameters['train_name'] == 'RFC':
        n_estimators = power_net_dataset_parameters['n_estimators']
        model_enc, model_rfc, y_prediction, report = Classification.algorithm_RFC_train(data, data_label, n_estimators)
        save_power_net_dataset_model(model_enc, 'Label.pkl', power_net_dataset_id)
        save_power_net_dataset_model(model_rfc, 'RFC.pkl', power_net_dataset_id)
        save_power_net_dataset_y_prediction(y_prediction, power_net_dataset_id)
        save_power_net_dataset_report(report, power_net_dataset_id)


def save_power_net_dataset_model(model_object, model_file_name, power_net_dataset_id):
    model_directory = os.path.join(celery_app.conf["SAVE_L_MODEL_PATH"], power_net_dataset_id)
    if not os.path.exists(model_directory):
        os.mkdir(model_directory)
    model_path = os.path.join(model_directory, model_file_name)
    joblib.dump(model_object, model_path)
    return model_path


def save_power_net_dataset_y_prediction(y_prediction, power_net_dataset_id):
    file_directory = os.path.join(celery_app.conf["SAVE_L_MODEL_PATH"], power_net_dataset_id)
    file_path = os.path.join(file_directory, 'y_prediction.csv')
    y_prediction.to_csv(file_path, header=True, index=False)
    return file_path


def save_power_net_dataset_report(report, power_net_dataset_id):
    file_directory = os.path.join(celery_app.conf["SAVE_L_MODEL_PATH"], power_net_dataset_id)
    file_path = os.path.join(file_directory, 'report.txt')
    with open(file_path, 'w') as f:
        f.write(report)
    return file_path
