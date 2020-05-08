from model import Task, Dataset, Train
from dao._BaseDao import BaseDao
from sqlalchemy import or_,and_

"""
used for task related database operation
"""
class TaskDao(BaseDao):

    def __init__(self, db):
        super().__init__(db, Task)

    """
    provide functions of base class another name 
    """
    def addTask(self, task):
        self.add(task)

    def deleteTask(self, taskId):
        self.delete((taskId))

    def updateTask(self, device):
        self.update(device)

    def queryTaskById(self, deviceId):
        return self.queryById(deviceId)

    """
    get tasks created by the user
    """
    def getMyTaskList(self, userid):
        # the result contains two model{Task,Dataset}
        query = self.db.session().query(Task, Dataset)
        # the task.dataset_id is related with dataset.id,
        # and the created_id should be the user
        query = query.join(Task, Task.dataset_id == Dataset.id).filter(Task.created_by==userid)
        return query.all()

    def getPublicTaskList(self):
        # a bit complicated filter
        # 1. the task should be public
        # 2. the status of the task should be 0 or None (which means waiting for a model)
        task_filter = {
            and_(
                or_(
                    Task.status.is_(None),
                    Task.status==0
                ),
                Task.public == 1
            )
        }
        query = self.db.session().query(Task, Dataset)
        query = query.join(Task, Task.dataset_id == Dataset.id).filter(*task_filter)
        return query.all()

    # support task means tasks whose model is provided by me
    def getMySupportTaskList(self, userid):
        # the result contains three model{Task,Dataset}
        query = self.db.session().query(Train, Task, Dataset)
        # the task.dataset_id is related with dataset.id,
        # and the created_id should be the user
        query = query.join(
            Train, Task.id == Train.task_id
        ).join(
            Dataset, Task.dataset_id == Dataset.id
        ).filter(
            Train.created_by==userid
        ).filter(
            Task.created_by!=userid
        )
        return query.all()