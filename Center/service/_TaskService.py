from dao import TaskDao, TrainDao, DatasetDao, transfer_list
from model import Task, db
import json
from utils.CommonUtil import get_uid

class TaskService:

    def __init__(self):
        self.taskDao = TaskDao(db)
        self.trainDao = TrainDao(db)
        self.datasetDao = DatasetDao(db)

    def addTask(self, userid, name, dataset_id, type, is_public):
        print("is public:",is_public)
        task = Task()
        task.id = get_uid()
        task.created_by = userid
        task.name = name
        task.dataset_id = dataset_id
        task.type = type
        task.public = int(is_public)
        self.taskDao.add(task)

    def getTaskById(self, userid, task_id):
        task = self.taskDao.queryTaskById(task_id)

        if (task.public is None or task.public == 0) and task.created_by != userid:
            raise ValueError

        if task is not None:
            task = task.serialize
            dataset_id = task['dataset_id']
            dataset = self.datasetDao.queryDatasetById(dataset_id)
            if dataset is not None:
                dataset = dataset.serialize
                extra_info = {
                    'dataset_name': dataset.get('name')
                }
                task.update(extra_info)
        return task

    def getMyTaskList(self, userid):
        tasks = self.taskDao.getMyTaskList(userid)
        return self.process(tasks)

    # support task means tasks whose model is provided by me
    def getMySupportTaskList(self, userid):
        tasks = self.taskDao.getMySupportTaskList(userid)
        return self.process(tasks)

    def getPublicTaskList(self):
        tasks = self.taskDao.getPublicTaskList()
        return self.process(tasks)

    def process(self, tasks):
        task_template = ['type', 'name', 'created_time', 'updated_time', 'public', 'id', 'configfile', 'status']
        dataset_template = ['name']
        tasks = [dict(zip(task.keys(), task)) for task in tasks]
        new_tasks = []
        for task in tasks:
            new_task = {}
            for key in task_template:
                new_task[key] = getattr(task['Task'], key, None)
            for key in dataset_template:
                new_task['dataset_' + key] = getattr(task['Dataset'], key, None)
            new_tasks.append(new_task)
        return new_tasks