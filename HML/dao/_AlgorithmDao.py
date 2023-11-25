from model import Algorithm
from dao._BaseDao import BaseDao

"""
used for algorithm related database operation
"""


class AlgorithmDao(BaseDao):

    def __init__(self, db):
        super().__init__(db, Algorithm)

    """
    provide functions of base class another name 
    """
    def addAlgorithm(self, algorithm):
        self.add(algorithm)

    def deleteAlgorithm(self, algorithm_id):
        algorithm = Algorithm.query.filter_by(algorithm_id=algorithm_id).first()
        self.delete(algorithm)

    def queryAlgorithmById(self, algorithm_id):
        algorithm = Algorithm.query.filter_by(algorithm_id=algorithm_id).first()
        return algorithm

    def queryAlgorithmListByCategory(self, algorithm_category):
        algorithms = Algorithm.query.filter_by(algorithm_category=algorithm_category).all()
        return algorithms

    def updateAlgorithm(self, algorithm_bean):
        algorithm = Algorithm.query.filter_by(algorithm_id=algorithm_bean.algorithm_id).first()
        algorithm.algorithm_name = algorithm_bean.algorithm_name
        algorithm.algorithm_type = algorithm_bean.file_type
        algorithm.algorithm_category = algorithm_bean.algorithm_category
        algorithm.algorithm_parameters = algorithm_bean.algorithm_parameters
        algorithm.introduction = algorithm_bean.introduction
        self.db.session.commit()

    def queryAlgorithmListByType(self, algorithm_type):
        algorithms = Algorithm.query.filter_by(algorithm_type=algorithm_type).all()
        return algorithms

    def queryAlgorithmParams(self, algorithm_name):
        algorithm = Algorithm.query.filter_by(algorithm_name=algorithm_name).first()
        return algorithm
