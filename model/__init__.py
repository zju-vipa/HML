from app.db import db

"""
database model
"""


def to_json(inst, cls):
    d = dict()
    """
    获取表里面的列并存到字典里面
    """
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        d[c.name] = v
    return d


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.String(32), primary_key=True, info='用户ID')
    email = db.Column(db.String(32), nullable=False, unique=True, info='邮箱')
    username = db.Column(db.String(32), nullable=False, info='用户名')
    password = db.Column(db.String(64), nullable=False, info='密码')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class Dataset(db.Model):
    __tablename__ = 'dataset'

    dataset_id = db.Column(db.String(32), primary_key=True, info='数据集ID')
    dataset_name = db.Column(db.String(32), nullable=False, info='数据集名')
    file_type = db.Column(db.String(32), nullable=False, info='文件类型')
    if_profile = db.Column(db.Boolean, nullable=False, default=False, info='是否分析文件')
    profile_state = db.Column(db.String(1), nullable=False, default='0', info='分析文件状态')
    task_id = db.Column(db.String(36), nullable=True, info='分析任务ID')
    if_public = db.Column(db.Boolean, nullable=False, default=False, info='是否公开')
    introduction = db.Column(db.Text, nullable=True, info='简介')
    if_featureEng = db.Column(db.Boolean, nullable=False, default=False, info='是否特征工程')
    featureEng_id = db.Column(db.String(32), nullable=True, info='特征工程ID')
    original_dataset_id = db.Column(db.String(32), nullable=True, info='原数据集ID')
    user_id = db.Column(db.String(32), nullable=False, info='用户ID')
    username = db.Column(db.String(32), nullable=False, info='用户名')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class FeatureEng(db.Model):
    __tablename__ = 'featureEng'

    featureEng_id = db.Column(db.String(32), primary_key=True, info='特征工程ID')
    featureEng_name = db.Column(db.String(32), nullable=False, info='特征工程名')
    featureEng_type = db.Column(db.String(32), nullable=False, info='特征工程类型')
    featureEng_processes = db.Column(db.Text, nullable=False, info='特征工程流程')
    operate_state = db.Column(db.String(1), nullable=False, default='0', info='操作状态')
    task_id = db.Column(db.String(36), nullable=False, info='操作任务ID')
    new_dataset_id = db.Column(db.String(32), nullable=True, info='新数据集ID')
    original_dataset_id = db.Column(db.String(32), nullable=False, info='原数据集ID')
    user_id = db.Column(db.String(32), nullable=False, info='用户ID')
    username = db.Column(db.String(32), nullable=False, info='用户名')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class Learner(db.Model):
    __tablename__ = 'learner'

    learner_id = db.Column(db.String(32), primary_key=True, info='学习器ID')
    learner_name = db.Column(db.String(32), nullable=False, info='学习器名')
    learner_type = db.Column(db.String(32), nullable=False, info='学习器类型')
    learner_parameters = db.Column(db.Text, nullable=False, info='学习器参数')
    train_state = db.Column(db.String(1), nullable=False, default='0', info='训练状态')
    task_id = db.Column(db.String(36), nullable=False, info='训练任务ID')
    dataset_id = db.Column(db.String(32), nullable=False, info='数据集ID')
    user_id = db.Column(db.String(32), nullable=False, info='用户ID')
    username = db.Column(db.String(32), nullable=False, info='用户名')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class Decision(db.Model):
    __tablename__ = 'decision'

    decision_id = db.Column(db.String(32), primary_key=True, info='决策者ID')
    decision_name = db.Column(db.String(32), nullable=False, info='决策者名')
    decision_type = db.Column(db.String(32), nullable=False, info='决策者类型')
    decision_parameters = db.Column(db.Text, nullable=False, info='决策者参数')
    featureEng_id = db.Column(db.String(32), nullable=True, info='特征工程ID')
    learner_id = db.Column(db.String(32), nullable=True, info='学习器ID')
    apply_state = db.Column(db.String(1), nullable=False, default='0', info='应用状态')
    task_id = db.Column(db.String(36), nullable=False, info='应用任务ID')
    dataset_id = db.Column(db.String(32), nullable=False, info='数据集ID')
    user_id = db.Column(db.String(32), nullable=False, info='用户ID')
    username = db.Column(db.String(32), nullable=False, info='用户名')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class Algorithm(db.Model):
    __tablename__ = 'algorithm'

    algorithm_id = db.Column(db.String(32), primary_key=True, info='算法ID')
    algorithm_name = db.Column(db.String(32), nullable=False, info='算法名')
    algorithm_type = db.Column(db.String(32), nullable=False, info='算法类型')
    algorithm_category = db.Column(db.String(32), nullable=False, info='算法类别')
    algorithm_parameters = db.Column(db.Text, nullable=False, info='算法参数')
    introduction = db.Column(db.Text, nullable=True, info='简介')

    @property
    def serialize(self):
        return to_json(self, self.__class__)