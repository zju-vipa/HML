from model import Decision
from dao._BaseDao import BaseDao

"""
used for Decision related database operation
"""


class DecisionDao(BaseDao):

    def __init__(self, db):
        super().__init__(db, Decision)

    """
    provide functions of base class another name 
    """
    def addDecision(self, decision):
        self.add(decision)

    def deleteDecision(self, decision_id):
        decision = Decision.query.filter_by(decision_id=decision_id).first()
        self.delete(decision)

    def queryDecisionById(self, decision_id):
        decision = Decision.query.filter_by(decision_id=decision_id).first()
        return decision

    def queryDecisionListByUserId(self, user_id):
        decisions = Decision.query.filter_by(user_id=user_id).all()
        return decisions

    def updateDecision(self, decision_bean):
        decision = Decision.query.filter_by(decision_id=decision_bean.decision_id).first()
        # not update task_id
        decision.decision_name = decision_bean.decision_name
        decision.decision_type = decision_bean.decision_type
        decision.decision_parameters = decision_bean.decision_parameters
        decision.featureEng_id = decision_bean.featureEng_id
        decision.learner_id = decision_bean.learner_id
        decision.apply_state = decision_bean.apply_state
        decision.dataset_id = decision_bean.dataset_id
        decision.user_id = decision_bean.user_id
        decision.username = decision_bean.username
        self.db.session.commit()
