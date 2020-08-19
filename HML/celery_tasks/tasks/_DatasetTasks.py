from celery_tasks.celery import celery_app
import pandas as pd
from pandas_profiling import ProfileReport
from dao import DatasetDao
from model import db, Dataset
datasetDao = DatasetDao(db)


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


@celery_app.task(bind=True, name='dataset.analyzeProfile')
def analyze_profile(self, dataset_json, file_path, profile_path):

    self.update_state(state='PROCESS', meta={'progress': 0.01, 'message': 'start'})
    dataset_bean = dataset_to_bean(dataset_json)

    # try:
    self.update_state(state='PROCESS', meta={'progress': 0.05, 'message': 'read csv'})
    data = pd.read_csv(file_path, delimiter=',', header=0, encoding='utf-8')

    self.update_state(state='PROCESS', meta={'progress': 0.20, 'message': 'generate profile report'})
    profile = ProfileReport(data, title='Pandas Profiling Report', html={'style': {'full_width': True}})

    self.update_state(state='PROCESS', meta={'progress': 0.70, 'message': 'save profile report'})
    profile.to_file(output_file=profile_path)

    self.update_state(state='PROCESS', meta={'progress': 0.95, 'message': 'update profile_state'})
    dataset_bean.profile_state = '2'
    datasetDao.updateDataset(dataset_bean)

    # except Exception:
    #     self.update_state(state='FAILURE', meta={'progress': 1.0, 'message': 'failure'})
    #     dataset_bean.profile_state = '3'
    #     datasetDao.updateDataset(dataset_bean)
    #     return 'FAILURE'

    return 'SUCCESS'

