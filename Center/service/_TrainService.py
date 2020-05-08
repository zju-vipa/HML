from dao import TrainDao, TaskDao, ModelDao, DatasetDao, transfer_list
from model import Train, db
import json
import uuid

class TrainService:

    def __init__(self):
        self.trainDao = TrainDao(db)
        self.taskDao = TaskDao(db)
        self.modelDao = ModelDao(db)
        self.datasetDao = DatasetDao(db)

    def addTrain(self, userid, task_id, model_id):
        # description: the task_id must be (public) or (private but same user)
        #              the model_id must be (public) or (private but same user)
        #              the task_id should not have been training

        task = self.taskDao.queryTaskById(task_id)
        model = self.modelDao.queryModelById(model_id)
        if task is None or (task.public == 0 and task.created_by != userid):
            raise ValueError
        if task.status is not None and task.status != 0:
            raise ValueError
        if model is None or (model.public == 0 and model.created_by != userid):
            raise ValueError

        train = Train()
        train.id = str(uuid.uuid4()).replace('-', '')
        train.created_by = userid
        train.task_id = task_id
        train.model_id = model_id
        train.status = 1

        # update the task status and add a train
        task = self.taskDao.queryTaskById(task_id)
        if task is None or (task.status is not None and task.status > 0):
            raise ValueError # the request task_id is illegal
        task.status = 1
        self.taskDao.updateTask(task)
        self.trainDao.addTrain(train)

    def getTrainByTaskid(self, taskid):
        train:Train = self.getTrainByTaskid(taskid)
        if train is not None:
            train = train.serialize
        return train

    def getUndoTrainList(self):
        trains = self.trainDao.getUndoTrainList()
        new_trains = []
        for train in trains:
            new_trains.append(train.serialize)
        return new_trains

    def acceptTrain(self, device_id, train_id):
        # validate the device id and train id
        # description:
        #   the device should't have train
        #   the train should be at status 1(waiting for train
        # exception:
        #   if the arguments have problem,this function will raise ValueError

        device_train = self.trainDao.getTrainByDeviceId(device_id)
        if device_train is not None and device_train.status != 3:
            raise ValueError

        train = self.trainDao.queryTrainById(train_id)
        if train.status != 1:
            raise ValueError

        train.device_id = device_id
        train.status = 2

        task = self.taskDao.queryTaskById(train.task_id)
        task.status = 2

        self.taskDao.updateTask(task)
        self.trainDao.updateTrain(train)

    def getDeviceActiveTrain(self, device_id):
        # complete a detailed task description of the device
        # used for train
        # todo: generate a dataset to train
        train = self.trainDao.getTrainByDeviceId(device_id)

        detailed_info = None
        if train is not None:
            detailed_info = {}
            task_id = train.task_id
            task = self.taskDao.queryTaskById(task_id)
            dataset_id = task.dataset_id
            model_id = train.model_id
            dataset = self.datasetDao.queryDatasetById(dataset_id)
            model = self.modelDao.queryById(model_id)

            detailed_info.update({'id': train.id})

            dataset_info = {
                'dataset_name': dataset.name,
                'dataset_config': dataset.config
            }
            detailed_info.update(dataset_info)

            model_info = {
                'model_name': model.name,
                'model_path': model.code_path,
                'model_config': model.config
            }
            detailed_info.update(model_info)
        return detailed_info

    def update_detail(self, device_id, train_id, detail):
        # validate the device id and train id
        # description:
        #   the device should be responsible for the train
        # exception:
        #   if the arguments have problem,this function will raise ValueError
        train = self.trainDao.queryTrainById(train_id)
        if train is None or train.device_id != device_id:
            raise ValueError

        train.detail = detail
        self.trainDao.update(train)

    def complete_train(self, device_id, train_id):
        train = self.trainDao.queryTrainById(train_id)
        if train is None or train.device_id != device_id:
            raise ValueError
        task_id = train.task_id
        task = self.taskDao.queryTaskById(task_id)
        task.status = 3
        self.taskDao.update(task)
        train.status = 3
        self.trainDao.update(train)

    def getDetailByTaskId(self, user_id, task_id):
        train = self.trainDao.queryTrainByTaskId(task_id)
        task = self.taskDao.queryTaskById(task_id)
        if task is None:
            raise ValueError # no such task
        if task.created_by != user_id and train.created_by != user_id:
            raise ValueError  # not permitted
        if train is None:
            raise ValueError # no such train
        detail = train.detail
        return detail
