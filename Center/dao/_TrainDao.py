from model import Train
from dao._BaseDao import BaseDao

"""
used for train related database operation
"""
class TrainDao(BaseDao):

    def __init__(self, db):
        super().__init__(db, Train)

    """
    provide functions of base class another name 
    """
    def addTrain(self, train):
        self.add(train)

    def deleteTrain(self, trainId):
        self.delete(trainId)

    def updateTrain(self, train):
        self.update(train)

    def queryTrainById(self, trainId):
        return self.queryById(trainId)

    """
    one task related with one train
    this function will return the train of the task
    """
    def queryTrainByTaskId(self, taskid):
        return Train.query.filter_by(task_id=taskid).first()

    """
    return all trains whose status is not accepted by train_client
    """
    def getUndoTrainList(self):
        trans = Train.query.filter_by(status=1).all()
        return trans

    """
    return the active train of the device
    """
    def getTrainByDeviceId(self, device_id):
        train = Train.query.filter_by(device_id=device_id).filter_by(status=2).first()
        return train


