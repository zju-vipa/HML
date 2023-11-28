import csv
import json
import zipfile

import pandas as pd
from dao import FeatureEngDao
from dao import DatasetDao
from model import db
from utils.EncryptUtil import get_uid
from celery_tasks.tasks import FeatureEngTasks
import os
import shutil
from flask import current_app


class FeatureEngService:

    def __init__(self):
        self.featureEngDao = FeatureEngDao(db)
        self.datasetDao = DatasetDao(db)

    def addFeatureEng(self, featureEng, featureEng_processes, original_dataset,
                      original_dataset_file_path, new_dataset_name):
        featureEng.featureEng_id = get_uid()
        featureEng.operate_state = '1'

        task = FeatureEngTasks.operate.apply_async((featureEng.serialize,
                                                          featureEng_processes,
                                                          original_dataset.serialize,
                                                          original_dataset_file_path,
                                                          new_dataset_name), countdown=1)

        featureEng.task_id = task.id
        self.featureEngDao.addFeatureEng(featureEng)

        return featureEng

    def deleteFeatureEng(self, featureEng_id, file_directory):
        shutil.rmtree(file_directory)
        return self.featureEngDao.deleteFeatureEng(featureEng_id)

    def updateFeatureEng(self, featureEng):
        return self.featureEngDao.updateFeatureEng(featureEng)

    def queryFeatureEngById(self, featureEng_id):
        featureEng = self.featureEngDao.queryFeatureEngById(featureEng_id)
        if featureEng:
            return featureEng
        else:
            return None

    def queryFeatureEngListByUserId(self, user_id):
        featureEngs = self.featureEngDao.queryFeatureEngListByUserId(user_id)
        if featureEngs:
            return featureEngs
        else:
            return None

    def getFeatureEngFileDirectory(self, featureEng):
        file_directory = os.path.join(current_app.config["SAVE_FE_MODEL_PATH"], featureEng.featureEng_id)

        if not os.path.exists(file_directory):
            return None

        return file_directory

    def getTaskOperateState(self, task_id):
        task = FeatureEngTasks.operate.AsyncResult(task_id)

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

    def queryFeatureLibraryByUserId(self, user_id):
        featureEngs = self.featureEngDao.queryFinishedFeatureEngListByUserId(user_id)
        featureLibrary = []
        for i in range(len(featureEngs)):
            new_dataset_id = featureEngs[i].new_dataset_id
            featureEng_processes = featureEngs[i].featureEng_processes
            featureEng_processes = json.loads(featureEng_processes)
            new_dataset = self.datasetDao.queryDatasetById(new_dataset_id)
            new_dataset_name = new_dataset.dataset_name
            new_dataset_introduction = new_dataset.introduction
            new_dataset_file_type = new_dataset.file_type
            feature_decoupling, feature_learning, feature_derive, feature_selection = "无", "无", "无", "无"
            if featureEng_processes:
                for j in range(len(featureEng_processes)):
                    current_app.logger.info("testtesttest")
                    current_app.logger.info(featureEng_processes[j])
                    if featureEng_processes[j]['process_name'] == 'Feature_Decoupling':
                        feature_decoupling = featureEng_processes[j]['operate_name']
                        if feature_decoupling == 'FactorGNN':
                            feature_decoupling = '基于因子图的特征解耦'
                    if featureEng_processes[j]['process_name'] == 'Feature_Learning':
                        feature_learning = featureEng_processes[j]['operate_name']
                        if feature_learning == 'GNN':
                            feature_learning = '基于GNN的特征提取'
                    if featureEng_processes[j]['process_name'] == 'Feature_Decoupling':
                        feature_derive = featureEng_processes[j]['operate_name']
                    if featureEng_processes[j]['process_name'] == 'Feature_Selection':
                        feature_selection = featureEng_processes[j]['operate_name']
            if new_dataset_file_type == 'csv':
                data_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id + '.csv'
                columns = pd.read_csv(data_path, delimiter=',', encoding='utf-8').columns.tolist()
                for k in range(len(columns)):
                    feature_item = {}
                    feature_item['name'] = columns[k]
                    feature_item['dataset'] = new_dataset_name
                    feature_item['task'] = new_dataset_introduction
                    feature_item['featureDecoupling'] = feature_decoupling
                    feature_item['featureLearning'] = feature_learning
                    feature_item['featureDerivation'] = feature_derive
                    feature_item['featureSelection'] = feature_selection
                    featureLibrary.append(feature_item)
            elif new_dataset_file_type == 'zip':
                new_dataset_save_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id + '.zip'
                decompress_dataset_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id
                if not os.path.exists(decompress_dataset_path):
                    with zipfile.ZipFile(new_dataset_save_path, "r") as zipobj:
                        zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
                file_num = len(os.listdir(decompress_dataset_path))
                sample_file = os.listdir(decompress_dataset_path)[int(file_num / 2)]
                columns = pd.read_csv(os.path.join(decompress_dataset_path, sample_file), delimiter=',', encoding='utf-8').columns.tolist()
                for k in range(len(columns)):
                    feature_item = {}
                    feature_item['name'] = columns[k]
                    feature_item['dataset'] = new_dataset_name
                    feature_item['task'] = new_dataset_introduction
                    feature_item['featureDecoupling'] = feature_decoupling
                    feature_item['featureLearning'] = feature_learning
                    feature_item['featureDerivation'] = feature_derive
                    feature_item['featureSelection'] = feature_selection
                    featureLibrary.append(feature_item)
        current_app.logger.info(featureLibrary)
        return featureLibrary

    def getTaskFeatureList(self, featureEng_id):
        featureEng = self.featureEngDao.queryFeatureEngById(featureEng_id)
        featureEng_processes = featureEng.featureEng_processes
        featureEng_processes = json.loads(featureEng_processes)
        new_dataset_id = featureEng.new_dataset_id
        new_dataset = self.datasetDao.queryDatasetById(new_dataset_id)
        new_dataset_name = new_dataset.dataset_name
        new_dataset_introduction = new_dataset.introduction
        new_dataset_file_type = new_dataset.file_type
        feature_decoupling, feature_learning, feature_derive, feature_selection = "无", "无", "无", "无"
        if featureEng_processes:
            for j in range(len(featureEng_processes)):
                if featureEng_processes[j]['process_name'] == 'Feature_Decoupling':
                    feature_decoupling = featureEng_processes[j]['operate_name']
                    if feature_decoupling == 'FactorGNN':
                        feature_decoupling = '基于因子图的特征解耦'
                if featureEng_processes[j]['process_name'] == 'Feature_Learning':
                    feature_learning = featureEng_processes[j]['operate_name']
                    if feature_learning == 'GNN':
                        feature_learning = '基于GNN的特征提取'
                if featureEng_processes[j]['process_name'] == 'Feature_Decoupling':
                    feature_derive = featureEng_processes[j]['operate_name']
                if featureEng_processes[j]['process_name'] == 'Feature_Selection':
                    feature_selection = featureEng_processes[j]['operate_name']
        featureList = []
        if new_dataset_file_type == 'csv':
            data_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id + '.csv'
            columns = pd.read_csv(data_path, delimiter=',', encoding='utf-8').columns.tolist()
            for k in range(len(columns)):
                feature_item = {}
                feature_item['name'] = columns[k]
                feature_item['dataset'] = new_dataset_name
                feature_item['task'] = new_dataset_introduction
                feature_item['featureDecoupling'] = feature_decoupling
                feature_item['featureLearning'] = feature_learning
                feature_item['featureDerivation'] = feature_derive
                feature_item['featureSelection'] = feature_selection
                featureList.append(feature_item)
        elif new_dataset_file_type == 'zip':
            new_dataset_save_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id + '.zip'
            decompress_dataset_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id
            if not os.path.exists(decompress_dataset_path):
                with zipfile.ZipFile(new_dataset_save_path, "r") as zipobj:
                    zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
            file_num = len(os.listdir(decompress_dataset_path))
            sample_file = os.listdir(decompress_dataset_path)[int(file_num / 2)]
            columns = pd.read_csv(os.path.join(decompress_dataset_path, sample_file), delimiter=',', encoding='utf-8').columns.tolist()
            for k in range(len(columns)):
                feature_item = {}
                feature_item['name'] = columns[k]
                feature_item['dataset'] = new_dataset_name
                feature_item['task'] = new_dataset_introduction
                feature_item['featureDecoupling'] = feature_decoupling
                feature_item['featureLearning'] = feature_learning
                feature_item['featureDerivation'] = feature_derive
                feature_item['featureSelection'] = feature_selection
                featureList.append(feature_item)
        return featureList

    def getLatestRecord(self, user_id):
        latestTask = self.featureEngDao.queryLatestFeatureEngByUserId(user_id)
        latestTask_id = latestTask.featureEng_id
        record_path = os.path.join(current_app.config['SAVE_FE_MODEL_PATH'], latestTask_id, 'record.csv')
        record_list = []
        with open(record_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            current_app.logger.info(header)
            for row in reader:
                current_app.logger.info(row)
                record_item = {}
                accuracy = row[0]
                efficiency = row[1]
                record_item['record_accuracy'] = accuracy
                record_item['record_efficiency'] = efficiency
                record_list.append(record_item)
            file.close()
        return record_list

    def getLatestTaskDetails(self, user_id):
        latestTask = self.featureEngDao.queryLatestFeatureEngByUserId(user_id)
        return latestTask

    def queryFeatureScores(self, user_id):
        featureEng = self.featureEngDao.queryLatestFeatureEngByUserId(user_id)
        if featureEng:
            featureEng_id = featureEng.featureEng_id
            score_file_path = os.path.join(current_app.config['SAVE_FE_MODEL_PATH'], featureEng_id, 'score.csv')
            if os.path.exists(score_file_path):
                with open(score_file_path, 'r') as file:
                    reader = csv.reader(file)
                    header = next(reader)
                    data = [row for row in reader]
                    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
                    score_dict = {}
                    key = []
                    value = []
                    if len(sorted_data) > 100:
                        sorted_data = sorted_data[0:100]
                    for row in sorted_data:
                        current_app.logger.info(row)
                        key.append(row[0])
                        value.append(row[1])
                    file.close()
                    score_dict['name'] = key
                    score_dict['value'] = value
            else:
                score_dict = None
        else:
            score_dict = None
        return score_dict

    def querySelectedTaskRecord(self, featureEng_id):
        record_path = os.path.join(current_app.config['SAVE_FE_MODEL_PATH'], featureEng_id, 'record.csv')
        if os.path.exists(record_path):
            record_list = []
            with open(record_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                current_app.logger.info(header)
                for row in reader:
                    current_app.logger.info(row)
                    record_item = {}
                    accuracy = row[0]
                    efficiency = row[1]
                    record_item['record_accuracy'] = accuracy
                    record_item['record_efficiency'] = efficiency
                    record_list.append(record_item)
                file.close()
        else:
            record_list = None
        return record_list

    def querySelectedTaskScores(self, featureEng_id):
        featureEng = self.featureEngDao.queryFeatureEngById(featureEng_id)
        if featureEng:
            featureEng_id = featureEng.featureEng_id
            score_file_path = os.path.join(current_app.config['SAVE_FE_MODEL_PATH'], featureEng_id, 'score.csv')
            if os.path.exists(score_file_path):
                with open(score_file_path, 'r') as file:
                    reader = csv.reader(file)
                    header = next(reader)
                    data = [row for row in reader]
                    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
                    score_dict = {}
                    key = []
                    value = []
                    if len(sorted_data) > 100:
                        sorted_data = sorted_data[0:100]
                    for row in sorted_data:
                        current_app.logger.info(row)
                        key.append(row[0])
                        value.append(row[1])
                    file.close()
                    score_dict['name'] = key
                    score_dict['value'] = value
            else:
                score_dict = None
        else:
            score_dict = None
        return score_dict

    def getTaskStatus(self, task_id):
        a = FeatureEngTasks.operate.AsyncResult(task_id)  # 实例化得到一个对象
        current_app.logger.info(a)
        running_message = {}
        if a.state == 'PENDING':
            running_message['status'] = 'PENDING'
            running_message['progress'] = 0
            running_message['message'] = '任务挂起'
        elif a.state == 'PROCESS':
            running_message['status'] = 'PROCESS'
            running_message['progress'] = a.info.get('progress')
            running_message['message'] = a.info.get('message')
        elif a.status == 'SUCCESS':
            running_message['status'] = 'SUCCESS'
            running_message['progress'] = 1.0
            running_message['message'] = '完成！'
        current_app.logger.info(running_message)
        return running_message