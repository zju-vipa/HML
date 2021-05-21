from dao import PowerNetDatasetDao
from model import db
from utils.EncryptUtil import get_uid
from utils.network import read_examples, net_description, get_networks
from celery_tasks.tasks import PowerNetDatasetTasks
from flask import current_app
import os
import shutil
import pandas as pd
import time


class PowerNetDatasetService:

    def __init__(self):
        self.powerNetDatasetDao = PowerNetDatasetDao(db)

    def addPowerNetDataset(self, power_net_dataset):
        power_net_dataset.power_net_dataset_id = get_uid()
        power_net_dataset.generate_state = '1'
        power_net_dataset.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        file_path = self.getPowerNetResultPath(power_net_dataset.power_net_dataset_id, power_net_dataset.power_net_dataset_type)
        task = PowerNetDatasetTasks.generate.apply_async((power_net_dataset.serialize, file_path), countdown=1)

        power_net_dataset.task_id = task.id
        self.powerNetDatasetDao.addPowerNetDataset(power_net_dataset)

        return power_net_dataset

    def deletePowerNetDataset(self, power_net_dataset_id, result_path):
        if os.path.exists(result_path):
            # shutil.rmtree(result_path)
            os.remove(result_path)
        return self.powerNetDatasetDao.deletePowerNetDataset(power_net_dataset_id)

    def updatePowerNetDataset(self, power_net_dataset):
        return self.powerNetDatasetDao.updatePowerNetDataset(power_net_dataset)

    def queryPowerNetDatasetById(self, power_net_dataset_id):
        power_net_dataset = self.powerNetDatasetDao.queryPowerNetDatasetById(power_net_dataset_id)
        if power_net_dataset:
            return power_net_dataset
        else:
            return None

    def queryPowerNetDatasetListByUserId(self, user_id):
        power_net_datasets = self.powerNetDatasetDao.queryPowerNetDatasetListByUserId(user_id)
        if power_net_datasets:
            return power_net_datasets
        else:
            return None

    # 查询全部电网数据集
    def queryPowerNetDatasetList(self):
        power_net_datasets = self.powerNetDatasetDao.queryPowerNetDatasetList()
        if power_net_datasets:
            return power_net_datasets
        else:
            return None

    def getPowerNetResultPath(self, power_net_dataset_id, pn_type):
        # file_directory = os.path.join(current_app.config["SAVE_PN_DATASET_PATH"], power_net_dataset_id)
        # file_name = 'pn_power_flow.csv'
        # file_path = os.path.join(file_directory, file_name)
        file_ext = ".csv"
        if pn_type == "B":
            file_ext = ".mat"
        file_path = os.path.join(current_app.config["SAVE_PN_DATASET_PATH"],
                                 str(power_net_dataset_id) + '_pn_power_flow' + file_ext)
        # if not os.path.exists(file_path):
        #     return None
        return file_path

    def getPowerNetResultData(self, file_path):
        try:
            data = pd.read_csv(file_path, delimiter=',', header=0, nrows=30, encoding='utf-8')
        except Exception:
            return None
        data = data.to_dict(orient='index')
        data_list = [data[i] for i in range(len(data))]
        return data_list

    def queryInitNetByName(self, name):
        initNet = read_examples(name)
        if not initNet:
            return None

        # example 样例描述找不到在哪里？？？

        description = net_description(initNet)
        # bus_number = description['bus']
        # load_number = description['load']
        # gen_number = description['gen']
        # line_number = description['line']

        # 组件就先不搞了 直接用比如 net['bus']
        # bus = get_networks(initNet, 'bus')
        return initNet, description

    def getTaskGenerateState(self, task_id):
        task = PowerNetDatasetTasks.generate.AsyncResult(task_id)
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
