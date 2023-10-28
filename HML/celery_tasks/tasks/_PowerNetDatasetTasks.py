from celery_tasks.celery import celery_app
import pandas as pd
import os
import joblib
# import sys
# UTILPATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# UTILPATH = os.path.join(UTILPATH, "utils")
# sys.path.append(UTILPATH)
# print("utils sys.path=", sys.path)
from dao import PowerNetDatasetDao
from model import db, PowerNetDataset
from utils.data_generation import emergency_data_generation_a
from utils.network import read_examples
from utils.matlab_data_generation import matlab_data_generation_b
from utils.ctgan_data_generation import ctgan_data_generation_c, ctgan_data_train_tablenet_loss
from celery_tasks.algorithms import UnbiasedGeneration
from flask import current_app
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
    # 潮流任务参数
    power_net_dataset_bean.disturb_src_type_list = power_net_dataset_json['disturb_src_type_list']
    power_net_dataset_bean.disturb_n_var = power_net_dataset_json['disturb_n_var']
    power_net_dataset_bean.disturb_radio = power_net_dataset_json['disturb_radio']
    power_net_dataset_bean.disturb_n_sample = power_net_dataset_json['disturb_n_sample']
    # 暂稳任务参数
    power_net_dataset_bean.load_list = power_net_dataset_json['load_list']
    power_net_dataset_bean.fault_line_list = power_net_dataset_json['fault_line_list']
    power_net_dataset_bean.line_percentage_list = power_net_dataset_json['line_percentage_list']
    power_net_dataset_bean.fault_time_list = power_net_dataset_json['fault_time_list']
    # ctgan参数
    power_net_dataset_bean.n_sample = power_net_dataset_json['n_sample']
    power_net_dataset_bean.cond_stability = power_net_dataset_json['cond_stability']
    power_net_dataset_bean.cond_load = power_net_dataset_json['cond_load']
    power_net_dataset_bean.set_human = power_net_dataset_json['set_human']
    # unbiased generate 参数
    power_net_dataset_bean.sample_num = power_net_dataset_json['sample_num']
    power_net_dataset_bean.fault_line = power_net_dataset_json['fault_line']
    power_net_dataset_bean.generate_algorithm = power_net_dataset_json['generate_algorithm']

    power_net_dataset_bean.start_time = power_net_dataset_json['start_time']
    power_net_dataset_bean.generate_state = power_net_dataset_json['generate_state']
    power_net_dataset_bean.user_id = power_net_dataset_json['user_id']
    power_net_dataset_bean.username = power_net_dataset_json['username']

    return power_net_dataset_bean


@celery_app.task(bind=True, name='power_net_dataset.generate')
def generate(self, power_net_dataset_json, file_path):
    # 开始
    current_app.logger.info("p1 task generate")
    self.update_state(state='PROCESS', meta={'progress': 0.01, 'message': 'start'})
    power_net_dataset_bean = power_net_dataset_to_bean(power_net_dataset_json)
    # power_net_dataset_id = power_net_dataset_bean.power_net_dataset_id
    current_app.logger.info("p2 task generate")
    power_net_dataset_type = power_net_dataset_bean.power_net_dataset_type
    current_app.logger.info(power_net_dataset_type)
    # A:潮流数据生成任务； B:暂稳数据生成任务
    if power_net_dataset_type == 'A':
        # 扰动参数转换
        current_app.logger.info("p3 task generate")
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
        current_app.logger.info("p4 task generate")
        # 生成电网数据集并且计算潮流结果
        self.update_state(state='PROCESS', meta={'progress': 0.10, 'message': 'generating'})
        res = emergency_data_generation_a(vars=pn_vars, if_random=True, n_var=power_net_dataset_bean.disturb_n_var,
                                          net=init_net, radio=power_net_dataset_bean.disturb_radio,
                                          n_sample=power_net_dataset_bean.disturb_n_sample)
        current_app.logger.info("p5 task generate")
        res.drop(columns=['net'], axis=1, inplace=True)
        # 保存结果
        self.update_state(state='PROCESS', meta={'progress': 0.90, 'message': 'saving result'})
        res.to_csv(file_path, header=True, index=False)
        current_app.logger.info("p6 task generate")
        current_app.logger.info(file_path)
    elif power_net_dataset_type == 'B':
        # 故障参数转换：负荷范围列表，
        current_app.logger.info("p7 task generate")
        self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read transient stability params'})
        load_list = list(map(float, power_net_dataset_bean.load_list.split(',')))
        fault_line_list = list(map(int, power_net_dataset_bean.fault_line_list.split(',')))
        line_percentage_list = list(map(float, power_net_dataset_bean.line_percentage_list.split(',')))
        fault_time_list = list(map(int, power_net_dataset_bean.fault_time_list.split(',')))
        current_app.logger.info("p8 task generate")
        current_app.logger.info(load_list)
        current_app.logger.info(fault_line_list)
        current_app.logger.info(line_percentage_list)
        current_app.logger.info(fault_time_list)
        # 初始电网样例默认为case39
        # init_net = read_examples(power_net_dataset_bean.init_net_name)

        # 进行暂稳计算生成电网数据集,保存结果
        self.update_state(state='PROCESS', meta={'progress': 0.10, 'message': 'generating'})
        res = matlab_data_generation_b(file_path="aaa.mat", load_list=load_list, fault_line_list=fault_line_list, line_percentage_list=line_percentage_list, fault_time_list=fault_time_list)
        current_app.logger.info("p9 task generate")
        current_app.logger.info(res)
        self.update_state(state='PROCESS', meta={'progress': 0.90, 'message': 'saving result'})
        # res.to_csv(file_path, header=True, index=False)
    elif power_net_dataset_type == 'C':
        # ctgan参数转换
        current_app.logger.info("p3.1 task generate")
        self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read disturb params'})
        n_sample = power_net_dataset_bean.n_sample
        cond_stability = power_net_dataset_bean.cond_stability
        cond_load = float(power_net_dataset_bean.cond_load)
        set_human = power_net_dataset_bean.set_human
        current_app.logger.info("p3.2 task generate")
        # 生成电网数据集并且计算潮流结果
        self.update_state(state='PROCESS', meta={'progress': 0.10, 'message': 'generating'})
        file_path_csv = file_path + '.csv'
        res = ctgan_data_generation_c(file_path=file_path_csv, n_sample=n_sample,
                                      cond_stability=cond_stability, cond_load=cond_load)
        current_app.logger.info(file_path_csv)
        self.update_state(state='PROCESS', meta={'progress': 0.90, 'message': 'saving result'})
        # 人在回路调参，展示loss图
        if set_human:
            res = ctgan_data_train_tablenet_loss(file_path)
            current_app.logger.info(res)
        current_app.logger.info("p3.4 task generate")
        current_app.logger.info(file_path)
    elif power_net_dataset_type == 'D':
        # unbiased generation: MC or unbiased
        current_app.logger.info("p3.1 task generate")
        self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read disturb params'})
        sample_num = power_net_dataset_bean.sample_num
        fault_line = power_net_dataset_bean.fault_line
        dataset_id = power_net_dataset_bean.power_net_dataset_id
        generate_algorithm = power_net_dataset_bean.generate_algorithm
        init_net_name = power_net_dataset_bean.init_net_name
        current_app.logger.info("p3.2 task generate")
        # 生成电网数据集
        self.update_state(state='PROCESS', meta={'progress': 0.10, 'message': 'generating'})
        if generate_algorithm == 2:
            res = UnbiasedGeneration.unbiased_generation_d(file_path=file_path, dataset_id=dataset_id,
                                                           sample_num=sample_num, fault_line=fault_line,
                                                           init_net_name=init_net_name)
        elif generate_algorithm == 1:
            res = UnbiasedGeneration.montecarlo_generation_d(file_path=file_path, dataset_id=dataset_id,
                                                             sample_num=sample_num, fault_line=fault_line,
                                                             init_net_name=init_net_name)
        current_app.logger.info(file_path)
        current_app.logger.info("p3.3 task generate")
        self.update_state(state='PROCESS', meta={'progress': 0.90, 'message': 'saving result'})

    # 完成生成任务 更新任务状态为2
    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': 'update generate_state'})
    power_net_dataset_bean.generate_state = '2'
    current_app.logger.info("p10 task generate")
    power_net_datasetDao.updatePowerNetDataset(power_net_dataset_bean)
    current_app.logger.info("p11 task generate")
    # except Exception:
    #     self.update_state(state='FAILURE', meta={'progress': 1.0, 'message': 'failure'})
    #     power_net_dataset_bean.generate_state = '3'
    #     power_net_datasetDao.updatePowerNetDataset(power_net_dataset_bean)
    #     return 'FAILURE'

    return 'SUCCESS'


