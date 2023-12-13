from model import Learner
from dao._BaseDao import BaseDao

"""
used for Learner related database operation
"""


class LearnerDao(BaseDao):

    def __init__(self, db):
        super().__init__(db, Learner)

    """
    provide functions of base class another name 
    """
    def addLearner(self, learner):
        self.add(learner)

    def deleteLearner(self, learner_id):
        learner = Learner.query.filter_by(learner_id=learner_id).first()
        self.delete(learner)

    def queryLearnerById(self, learner_id):
        learner = Learner.query.filter_by(learner_id=learner_id).first()
        return learner

    def queryLearnerListByUserId(self, user_id):
        learners = Learner.query.filter_by(user_id=user_id).all()
        return learners

    def updateLearner(self, learner_bean):
        learner = Learner.query.filter_by(learner_id=learner_bean.learner_id).first()
        # not update task_id
        learner.learner_name = learner_bean.learner_name
        learner.learner_type = learner_bean.learner_type
        learner.learner_parameters = learner_bean.learner_parameters
        learner.train_state = learner_bean.train_state
        learner.dataset_id = learner_bean.dataset_id
        learner.user_id = learner_bean.user_id
        learner.username = learner_bean.username
        learner.action = learner_bean.action
        print(learner_bean.action)
        self.db.session.commit()
    # update task_id
    def updateLearnerAll(self, learner_bean):
        learner = Learner.query.filter_by(learner_id=learner_bean.learner_id).first()
        learner.learner_name = learner_bean.learner_name
        learner.learner_type = learner_bean.learner_type
        learner.learner_parameters = learner_bean.learner_parameters
        learner.train_state = learner_bean.train_state
        learner.dataset_id = learner_bean.dataset_id
        learner.user_id = learner_bean.user_id
        learner.username = learner_bean.username
        learner.action = learner_bean.action
        learner.test_task_id = learner_bean.test_task_id
        learner.task_id = learner_bean.task_id
        self.db.session.commit()
