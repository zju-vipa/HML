from dao import DatasetDao
from model import db
from utils.EncryptUtil import get_uid
import os
import shutil
import pandas as pd
from flask import current_app
from celery_tasks.tasks import DatasetTasks


class DatasetService:

    def __init__(self):
        self.datasetDao = DatasetDao(db)

    def uploadDataset(self, file):
        dataset_id = get_uid()
        file_type = os.path.splitext(file.filename)[-1]
        file_name = dataset_id + file_type
        tmp_file_path = os.path.join(current_app.config["SAVE_TMP_DATASET_PATH"], file_name)
        file.save(tmp_file_path)

        # hgs ignore type limitation
        # try:
        #     pd.read_csv(tmp_file_path, delimiter=',', header=0, nrows=16, encoding='utf-8')
        # except Exception:
        #     return None

        data = {'dataset_id': dataset_id, 'tmp_file_path': tmp_file_path}
        return data

    def addDataset(self, dataset, tmp_file_path):
        try:
            for _file_path in tmp_file_path:
                shutil.move(_file_path, current_app.config["SAVE_DATASET_PATH"])
        except Exception:
            pass
        file_path = self.getDatasetFilePath(dataset)
        dataset.profile_state = '0'

        task_id = None
        if dataset.if_profile:
            dataset.profile_state = '1'
            profile_name = dataset.dataset_id + '.html'
            profile_directory = current_app.config["SAVE_PROFILE_PATH"]
            profile_path = os.path.join(profile_directory, profile_name)
            task = DatasetTasks.analyze_profile.apply_async((dataset.serialize, file_path, profile_path), countdown=5)
            task_id = task.id

        dataset.task_id = task_id
        self.datasetDao.addDataset(dataset)

        return dataset

    def deleteDataset(self, dataset_id, file_path, profile_path):
        os.remove(file_path)
        if profile_path:
            os.remove(profile_path)
        return self.datasetDao.deleteDataset(dataset_id)

    def updateDataset(self, dataset):
        return self.datasetDao.updateDataset(dataset)

    def queryDatasetById(self, dataset_id):
        dataset = self.datasetDao.queryDatasetById(dataset_id)
        if dataset:
            return dataset
        else:
            return None

    def queryDatasetListByUserId(self, user_id, if_featureEng=None):
        datasets = self.datasetDao.queryDatasetListByUserId(user_id, if_featureEng)
        if datasets:
            return datasets
        else:
            return None

    def getDatasetFilePath(self, dataset):
        file_name = dataset.dataset_id + '.' + dataset.file_type
        file_directory = current_app.config["SAVE_DATASET_PATH"]
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            return None

        return file_path

    def getDatasetProfilePath(self, dataset):
        file_name = dataset.dataset_id + '.html'
        file_directory = current_app.config["SAVE_PROFILE_PATH"]
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            return None

        return file_path

    def getDatasetData(self, file_path):
        try:
            data = pd.read_csv(file_path, delimiter=',', header=0, nrows=16, encoding='utf-8')
        except Exception:
            return None

        data = data.to_dict(orient='index')

        data_list = [data[i] for i in range(len(data))]

        return data_list

    def getDatasetColumns(self, file_path):
        try:
            data = pd.read_csv(file_path, delimiter=',', header=0, nrows=16, encoding='utf-8').columns.tolist()
        except Exception:
            return None

        return data

    def getTaskAnalyzeProfileState(self, task_id):
        # 使用任务 id 初始化 AsyncResult 类，获得任务对象，然后就可以从任务对象中获得当前任务的信息。
        # 该方法会返回一个 JSON，其中包含了任务状态以及 meta 中指定的信息。
        task = DatasetTasks.analyze_profile.AsyncResult(task_id)

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
