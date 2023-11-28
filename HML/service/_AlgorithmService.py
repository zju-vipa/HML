from dao import AlgorithmDao
from model import db
from utils.EncryptUtil import get_uid


class AlgorithmService:

    def __init__(self):
        self.algorithmDao = AlgorithmDao(db)

    def addAlgorithm(self, algorithm):
        algorithm.algorithm_id = get_uid()
        self.algorithmDao.addAlgorithm(algorithm)
        return algorithm

    def deleteAlgorithm(self, algorithm_id):
        return self.algorithmDao.deleteAlgorithm(algorithm_id)

    def updateAlgorithm(self, algorithm):
        return self.algorithmDao.updateAlgorithm(algorithm)

    def queryAlgorithmById(self, algorithm_id):
        algorithm = self.algorithmDao.queryAlgorithmById(algorithm_id)
        if algorithm:
            return algorithm
        else:
            return None

    def queryAlgorithmListByCategory(self, algorithm_category):
        algorithms = self.algorithmDao.queryAlgorithmListByCategory(algorithm_category)
        if algorithms:
            return algorithms
        else:
            return None

    def queryAlgorithmListByType(self, algorithm_type):
        algorithms = self.algorithmDao.queryAlgorithmListByType(algorithm_type)
        if algorithms:
            return algorithms
        else:
            return None

    def queryAlgorithmParams(self, algorithm_name):
        algorithm = self.algorithmDao.queryAlgorithmParams(algorithm_name)
        if algorithm:
            return algorithm
        else:
            return None