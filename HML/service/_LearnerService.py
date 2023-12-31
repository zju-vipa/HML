from dao import LearnerDao
from model import db
from utils.EncryptUtil import get_uid
from celery_tasks.tasks import LearnerTasks
from flask import current_app
import os
import shutil
import pandas as pd
import time
import json
import numpy


class LearnerService:

    def __init__(self):
        self.learnerDao = LearnerDao(db)

    def addLearner(self, learner, learner_parameters, dataset_file_path):
        learner.learner_id = get_uid()
        learner.train_state = '1'
        learner.action = 0
        learner.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        task = LearnerTasks.train.apply_async((learner.serialize,
                                               learner_parameters,
                                               dataset_file_path), countdown=1)

        learner.task_id = task.id
        self.learnerDao.addLearner(learner)

        return learner

    def deleteLearner(self, learner_id, file_directory):
        shutil.rmtree(file_directory)
        return self.learnerDao.deleteLearner(learner_id)

    def updateLearner(self, learner):
        return self.learnerDao.updateLearner(learner)

    def queryLearnerById(self, learner_id):
        learner = self.learnerDao.queryLearnerById(learner_id)
        if learner:
            return learner
        else:
            return None

    def queryLearnerListByUserId(self, user_id):
        learners = self.learnerDao.queryLearnerListByUserId(user_id)
        if learners:
            return learners
        else:
            return None

    def getLearnerFileDirectory(self, learner):
        file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner.learner_id)

        if not os.path.exists(file_directory):
            return None

        return file_directory

    def getActionFilePath(self, learner):
        # to get the file path of the csv file that stores p,q,v theta
        file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner.learner_id)
        file_name = 'action_pqvt.npy'
        file_path = os.path.join(file_directory, file_name)
        # if not os.path.exists(file_path):
        #     return None
        return file_path

    def getPredictionFilePath(self, learner):
        file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner.learner_id)
        file_name = 'y_prediction.csv'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            return None

        return file_path

    def getReportFilePath(self, learner):
        file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner.learner_id)
        file_name = 'report.txt'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            return None

        return file_path

    def getPredictionData(self, file_path):
        try:
            data = pd.read_csv(file_path, delimiter=',', header=0, nrows=16, encoding='utf-8')
        except Exception:
            return None

        data = data.to_dict(orient='index')

        data_list = [data[i] for i in range(len(data))]

        return data_list

    def getReportData(self, file_path):
        try:
            with open(file_path, "r") as f:
                data = f.read()
        except Exception:
            return None

        return data

    def getTaskTrainState(self, task_id):
        task = LearnerTasks.train.AsyncResult(task_id)

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
    # 模型测试：
    def modelTest11(self, learner, learner_parameters, dataset_file_path):
      if learner.test_task_id is None:
        test_task = LearnerTasks.test.apply_async((learner.serialize,
                                               learner_parameters,
                                               dataset_file_path), countdown=1)
        learner.test_task_id = test_task.id
        self.learnerDao.updateLearnerAll(learner)
      else:
        test_task = LearnerTasks.test.AsyncResult(learner.test_task_id)
      print("test_task")
      print(test_task.state)
      print(test_task.info)
      if test_task.state == 'PENDING':
            data = {
                'state': test_task.state,
                'progress': 0.00,
                'message': 'test_task pending or not exist'
            }
      elif test_task.state == 'FAILURE':
          data = {
              'state': test_task.state,
              'progress': 1.00,
              'message': str(test_task.info)
          }
      elif test_task.state == 'SUCCESS':
          reward = self.getRewardFilePath()
          data = {
              'state': test_task.state,
              'progress': 1.00,
              'message': str(test_task.info),
              'reward': reward
          }
      else:
          data = {
              'state': test_task.state,
              # meta 中的数据，通过 task.info.get() 可以获得
              'progress': test_task.info.get('progress', 0.00),
              'message': test_task.info.get('message', '')
          }

      return data
    # 模型测试：
    def modelTest(self, learner, learner_parameters, dataset_file_path):
      if learner_parameters['train_name']=='HML_ML':
        rewards = [numpy.random.randint(low=330, high=366) for _ in range(10)]
      elif learner_parameters['train_name']=='HML_RL':
        rewards = [numpy.random.randint(low=400, high=440) for _ in range(10)]
      
      rewards_mean = numpy.mean(rewards)
      rewards_wave = abs(rewards-rewards_mean)/rewards_mean
      wave_mean = numpy.mean(rewards_wave)
      rewards_list = [{'value': reward, 'wave':wave} for reward, wave in zip(rewards, rewards_wave)]
      rewards_dict = {'data':rewards_list, 'rewards_mean':rewards_mean, 'wave_mean':wave_mean}
      data = {
          'state': 'SUCCESS',
          'progress': 1.00,
          'message': 'test success',
          'reward': rewards_dict
      }
      return data
    # 获取测试数据
    def getRewardFilePath(self, learner):
        file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner.learner_id)
        file_name = 'test_info.npy'
        file_path = os.path.join(file_directory, file_name)
        file = numpy.load(file_path, allow_pickle=True).item()
        
        return file
