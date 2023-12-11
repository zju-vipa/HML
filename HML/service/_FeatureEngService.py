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

    def addFeatureEng(self, featureEng, featureEng_processes, original_dataset, original_dataset_file_path, new_dataset_name, imported_featureEng):
        featureEng.featureEng_id = get_uid()
        featureEng.operate_state = '1'

        task = FeatureEngTasks.operate.apply_async((featureEng.serialize,
                                                          featureEng_processes,
                                                          original_dataset.serialize,
                                                          original_dataset_file_path,
                                                          new_dataset_name, imported_featureEng), countdown=1)

        featureEng.task_id = task.id
        self.featureEngDao.addFeatureEng(featureEng)

        return featureEng

    def deleteFeatureEng(self, featureEng_id, file_directory):
        shutil.rmtree(file_directory)
        return self.featureEngDao.deleteFeatureEng(featureEng_id)

    def deleteFeatureEngRecord(self, featureEng_id):
        return self.featureEngDao.deleteFeatureEng(featureEng_id)

    def updateFeatureEng(self, featureEng):
        return self.featureEngDao.updateFeatureEng(featureEng)

    def updateTaskStatus(self, featureEng_id):
        return self.featureEngDao.updateTaskStatus(featureEng_id)

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

    def stopTask(self, task_id):
        result = FeatureEngTasks.operate.AsyncResult(task_id)
        result.revoke(terminate=True)
        return 'SUCCESS'

    def queryFeatureEngList(self, user_id):
        featureEngs = self.featureEngDao.queryFeatureEngListByUserId(user_id)
        featureEngList = []
        for i in range(len(featureEngs)):
            featureEng = {}
            featureEng['featureEng_id'] = featureEngs[i].featureEng_id
            featureEng['featureEng_name'] = featureEngs[i].featureEng_name
            featureEng['featureEng_type'] = featureEngs[i].featureEng_type
            if featureEngs[i].FeatureEng_accuracy:
                featureEng['FeatureEng_accuracy'] = round(float(featureEngs[i].FeatureEng_accuracy), 2)
                featureEng['FeatureEng_efficiency'] = round(float(featureEngs[i].FeatureEng_efficiency), 2)
            else:
                featureEng['FeatureEng_accuracy'] = None
                featureEng['FeatureEng_efficiency'] = None
            featureEng['operate_state'] = featureEngs[i].operate_state
            featureEng['start_time'] = featureEngs[i].start_time
            if featureEngs[i].end_time:
                duration = featureEngs[i].end_time - featureEngs[i].start_time
                days = duration.days
                hours = int(duration.seconds / 3600)
                minutes = int((duration.seconds - hours * 3600) / 60)
                seconds = duration.seconds - hours * 3600 - minutes * 60
                days = str(days)
                if hours < 10:
                    hours = '0' + str(hours)
                else:
                    hours = str(hours)
                if minutes < 10:
                    minutes = '0' + str(minutes)
                else:
                    minutes = str(minutes)
                if seconds < 10:
                    seconds = '0' + str(seconds)
                else:
                    seconds = str(seconds)
                spent_time = days + ':' + hours + ':' + minutes + ':' + seconds
                featureEng['spent_time'] = spent_time
            else:
                featureEng['spent_time'] = None
            task_id = featureEngs[i].task_id
            message = self.getTaskStatus(task_id)
            if len(message) == 0:
                task_progress = None
            else:
                task_progress = message['progress']
            featureEng['task_progress'] = task_progress
            featureEngList.append(featureEng)
        if len(featureEngList) != 0:
            return featureEngList
        else:
            return None

    def queryImportFeatureEngList(self, user_id):
        featureEngs = self.featureEngDao.queryFinishedFeatureEngListByUserId(user_id)
        featureEngList = []
        for i in range(len(featureEngs)):
            featureEng = {}
            new_dataset_id = featureEngs[i].new_dataset_id
            new_dataset = self.datasetDao.queryDatasetById(new_dataset_id)
            new_dataset_introduction = new_dataset.introduction
            featureEng['featureEng_id'] = featureEngs[i].featureEng_id
            featureEng['featureEng_name'] = featureEngs[i].featureEng_name
            featureEng['task'] = new_dataset_introduction
            featureEng['featureEng_type'] = featureEngs[i].featureEng_type
            featureEng['FeatureEng_accuracy'] = round(float(featureEngs[i].FeatureEng_accuracy), 2)
            featureEng['FeatureEng_efficiency'] = round(float(featureEngs[i].FeatureEng_efficiency), 2)
            featureEngList.append(featureEng)
        if len(featureEngList) != 0:
            return featureEngList
        else:
            return None

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
            feature_construct, feature_generation, feature_decoupling, feature_learning, feature_derive, feature_selection = "无", "无", "无", "无", "无", "无"
            if featureEng_processes:
                for j in range(len(featureEng_processes)):
                    if featureEng_processes[j]['process_name'] == 'Feature_Construct':
                        feature_construct = featureEng_processes[j]['operate_name']
                        if feature_construct == 'Expert-Experience':
                            feature_construct = '基于专家经验的特征构建'
                    if featureEng_processes[j]['process_name'] == 'Feature_Generation':
                        feature_generation = featureEng_processes[j]['operate_name']
                        if feature_generation == 'FETCH':
                            feature_generation = 'FETCH自动化特征工程'
                    if featureEng_processes[j]['process_name'] == 'Feature_Decoupling':
                        feature_decoupling = featureEng_processes[j]['operate_name']
                        if feature_decoupling == 'FactorGNN':
                            feature_decoupling = '基于因子图的特征解耦'
                    if featureEng_processes[j]['process_name'] == 'Feature_Learning':
                        feature_learning = featureEng_processes[j]['operate_name']
                        if feature_learning == 'GNN':
                            feature_learning = '基于GNN的特征提取'
                    if featureEng_processes[j]['process_name'] == 'Feature_Derive':
                        feature_derive = featureEng_processes[j]['operate_name']
                        if feature_derive == 'HumanMachineCooperation':
                            feature_derive = '人机协同特征生成'
                    if featureEng_processes[j]['process_name'] == 'Feature_Selection':
                        feature_selection = featureEng_processes[j]['operate_name']
                        if feature_selection == 'ModelBased':
                            feature_selection = '基于模型的特征选择'
            if new_dataset_file_type == 'csv':
                data_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id + '.csv'
                if os.path.exists(data_path):
                    columns = pd.read_csv(data_path, delimiter=',', encoding='utf-8').columns.tolist()
                    for k in range(len(columns)-1):
                        feature_item = {}
                        feature_item['name'] = columns[k]
                        feature_item['dataset'] = new_dataset_name
                        feature_item['task'] = new_dataset_introduction
                        feature_item['featureConstruct'] = feature_construct
                        feature_item['featureGeneration'] = feature_generation
                        feature_item['featureDecoupling'] = feature_decoupling
                        feature_item['featureLearning'] = feature_learning
                        feature_item['featureDerivation'] = feature_derive
                        feature_item['featureSelection'] = feature_selection
                        featureLibrary.append(feature_item)
            elif new_dataset_file_type == 'zip':
                new_dataset_save_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id + '.zip'
                if os.path.exists(new_dataset_save_path):
                    decompress_dataset_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id
                    if not os.path.exists(decompress_dataset_path):
                        with zipfile.ZipFile(new_dataset_save_path, "r") as zipobj:
                            zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
                    file_num = len(os.listdir(decompress_dataset_path))
                    sample_file = os.listdir(decompress_dataset_path)[int(file_num / 2)]
                    columns = pd.read_csv(os.path.join(decompress_dataset_path, sample_file), delimiter=',', encoding='utf-8').columns.tolist()
                    for k in range(len(columns)-1):
                        feature_item = {}
                        feature_item['name'] = columns[k]
                        feature_item['dataset'] = new_dataset_name
                        feature_item['task'] = new_dataset_introduction
                        feature_item['featureConstruct'] = feature_construct
                        feature_item['featureGeneration'] = feature_generation
                        feature_item['featureDecoupling'] = feature_decoupling
                        feature_item['featureLearning'] = feature_learning
                        feature_item['featureDerivation'] = feature_derive
                        feature_item['featureSelection'] = feature_selection
                        featureLibrary.append(feature_item)
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
        feature_construct, feature_generation, feature_decoupling, feature_learning, feature_derive, feature_selection = "无", "无", "无", "无", "无", "无"
        if featureEng_processes:
            for j in range(len(featureEng_processes)):
                if featureEng_processes[j]['process_name'] == 'Feature_Construct':
                    feature_construct = featureEng_processes[j]['operate_name']
                    if feature_construct == 'Expert-Experience':
                        feature_construct = '基于专家经验的特征构建'
                if featureEng_processes[j]['process_name'] == 'Feature_Generation':
                    feature_generation = featureEng_processes[j]['operate_name']
                    if feature_generation == 'FETCH':
                        feature_generation = 'FETCH自动化特征工程'
                if featureEng_processes[j]['process_name'] == 'Feature_Decoupling':
                    feature_decoupling = featureEng_processes[j]['operate_name']
                    if feature_decoupling == 'FactorGNN':
                        feature_decoupling = '基于因子图的特征解耦'
                if featureEng_processes[j]['process_name'] == 'Feature_Learning':
                    feature_learning = featureEng_processes[j]['operate_name']
                    if feature_learning == 'GNN':
                        feature_learning = '基于GNN的特征提取'
                if featureEng_processes[j]['process_name'] == 'Feature_Derive':
                    feature_derive = featureEng_processes[j]['operate_name']
                    if feature_derive == 'HumanMachineCooperation':
                        feature_derive = '人机协同特征生成'
                if featureEng_processes[j]['process_name'] == 'Feature_Selection':
                    feature_selection = featureEng_processes[j]['operate_name']
                    if feature_selection == 'ModelBased':
                        feature_selection = '基于模型的特征选择'
        featureList = []
        if new_dataset_file_type == 'csv':
            data_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id + '.csv'
            if os.path.exists(data_path):
                columns = pd.read_csv(data_path, delimiter=',', encoding='utf-8').columns.tolist()
                score_file_path = os.path.join(current_app.config['SAVE_FE_MODEL_PATH'], featureEng_id, 'score.csv')
                with open(score_file_path, 'r') as file:
                    reader = csv.reader(file)
                    header = next(reader)
                    data = [row for row in reader]
                    data_num = len(columns) - 1
                    effective_data_num = int(data_num * float(featureEng.FeatureEng_efficiency) / 100)
                    sorted_data = data[:effective_data_num]
                    key = []
                    for row in sorted_data:
                        key.append(row[0])
                    file.close()
                for k in range(len(columns)-1):
                    feature_item = {}
                    feature_item['name'] = columns[k]
                    feature_item['dataset'] = new_dataset_name
                    feature_item['task'] = new_dataset_introduction
                    feature_item['featureConstruct'] = feature_construct
                    feature_item['featureGeneration'] = feature_generation
                    feature_item['featureDecoupling'] = feature_decoupling
                    feature_item['featureLearning'] = feature_learning
                    feature_item['featureDerivation'] = feature_derive
                    feature_item['featureSelection'] = feature_selection
                    if columns[k] in key:
                        feature_item['effective'] = '是'
                    else:
                        feature_item['effective'] = '否'
                    featureList.append(feature_item)
            else:
                return None
        elif new_dataset_file_type == 'zip':
            new_dataset_save_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id + '.zip'
            if os.path.exists(new_dataset_save_path):
                decompress_dataset_path = current_app.config['SAVE_DATASET_PATH'] + '/' + new_dataset_id
                if not os.path.exists(decompress_dataset_path):
                    with zipfile.ZipFile(new_dataset_save_path, "r") as zipobj:
                        zipobj.extractall(current_app.config['SAVE_DATASET_PATH'])
                file_num = len(os.listdir(decompress_dataset_path))
                sample_file = os.listdir(decompress_dataset_path)[int(file_num / 2)]
                columns = pd.read_csv(os.path.join(decompress_dataset_path, sample_file), delimiter=',', encoding='utf-8').columns.tolist()
                for k in range(len(columns)-1):
                    feature_item = {}
                    feature_item['name'] = columns[k]
                    feature_item['dataset'] = new_dataset_name
                    feature_item['task'] = new_dataset_introduction
                    feature_item['featureConstruct'] = feature_construct
                    feature_item['featureGeneration'] = feature_generation
                    feature_item['featureDecoupling'] = feature_decoupling
                    feature_item['featureLearning'] = feature_learning
                    feature_item['featureDerivation'] = feature_derive
                    feature_item['featureSelection'] = feature_selection
                    featureList.append(feature_item)
            else:
                return None
        return featureList

    def getLatestRecord(self, user_id):
        latestTask = self.featureEngDao.queryLatestFeatureEngByUserId(user_id)
        latestTask_id = latestTask.featureEng_id
        record_path = os.path.join(current_app.config['SAVE_FE_MODEL_PATH'], latestTask_id, 'record.csv')
        record_list = []
        if os.path.exists(record_path):
            with open(record_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    record_item = {}
                    accuracy = row[0]
                    efficiency = row[1]
                    record_item['record_accuracy'] = accuracy
                    record_item['record_efficiency'] = efficiency
                    record_list.append(record_item)
                file.close()
            return record_list
        else:
            return None

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
                    # sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
                    sorted_data = data
                    score_dict = {}
                    key = []
                    value = []
                    if len(sorted_data) > 100:
                        sorted_data = sorted_data[0:100]
                    for row in sorted_data:
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
                for row in reader:
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
                    # sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
                    sorted_data = data
                    score_dict = {}
                    key = []
                    value = []
                    if len(sorted_data) > 100:
                        sorted_data = sorted_data[0:100]
                    for row in sorted_data:
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
        return running_message