from app.db import db
import json

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


class PowerNetDataset(db.Model):
    __tablename__ = 'power_net_dataset'

    power_net_dataset_id = db.Column(db.String(32), primary_key=True, info='电网数据集ID')
    power_net_dataset_name = db.Column(db.String(32), nullable=False, info='数据集名')
    task_id = db.Column(db.String(36), nullable=True, info='任务ID')
    power_net_dataset_type = db.Column(db.Text, nullable=True, info='生成方式')
    power_net_dataset_description = db.Column(db.Text, nullable=True, info='任务描述')
    init_net_name = db.Column(db.String(32), nullable=True, info='初始电网样例')
    # 潮流参数
    disturb_src_type_list = db.Column(db.String(64), nullable=True, info='扰动源类型')
    disturb_n_var = db.Column(db.Integer, nullable=True, info='扰动源个数')
    disturb_radio = db.Column(db.Integer, nullable=True, info='扰动范围')
    disturb_n_sample = db.Column(db.Integer, nullable=True, info='扰动次数')
     # 暂稳参数
    load_list = db.Column(db.Text, nullable=True, info='负荷范围列表')
    fault_line_list = db.Column(db.Text, nullable=True, info='故障线路列表')
    line_percentage_list = db.Column(db.Text, nullable=True, info='线路故障位置列表')
    fault_time_list = db.Column(db.Text, nullable=True, info='故障持续时间列表')
    # ctgan参数
    n_sample = db.Column(db.Integer, nullable=True, info='样本数')
    cond_stability = db.Column(db.Integer, nullable=True, info='稳定条件')
    cond_load = db.Column(db.String(32), nullable=True, info='负荷条件')
    set_human = db.Column(db.Boolean, nullable=True, default=False, info='是否人在回路调参')
    # unbiased generate 参数
    sample_num = db.Column(db.Integer, nullable=True, info='生成样本数')
    fault_line = db.Column(db.Integer, nullable=True, info='故障线路')
    generate_algorithm = db.Column(db.Integer, nullable=True, info='生成算法选择')

    start_time = db.Column(db.DateTime, nullable=True, info='开始时间')
    generate_state = db.Column(db.String(1), nullable=False, default='0', info='生成状态')
    user_id = db.Column(db.String(32), nullable=False, info='用户ID')
    username = db.Column(db.String(32), nullable=False, info='用户名')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class FeatureEng(db.Model):
    __tablename__ = 'featureEng'

    featureEng_id = db.Column(db.String(32), primary_key=True, info='特征工程ID')
    featureEng_name = db.Column(db.String(32), nullable=False, info='特征工程名')
    featureEng_operationMode = db.Column(db.String(32), nullable=False, info='运行方式')
    featureEng_type = db.Column(db.String(32), nullable=False, info='特征工程类型')
    featureEng_modules = db.Column(db.String(32), nullable=True, info='功能模块')
    featureEng_processes = db.Column(db.Text, nullable=False, info='特征工程流程')
    operate_state = db.Column(db.String(1), nullable=False, default='0', info='操作状态')
    FeatureEng_efficiency = db.Column(db.String(32), nullable=True, info='特征有效率')
    FeatureEng_accuracy = db.Column(db.String(32), nullable=True, info='任务准确率')
    task_id = db.Column(db.String(36), nullable=False, info='操作任务ID')
    new_dataset_id = db.Column(db.String(32), nullable=True, info='新数据集ID')
    original_dataset_id = db.Column(db.String(32), nullable=False, info='原数据集ID')
    user_id = db.Column(db.String(32), nullable=False, info='用户ID')
    username = db.Column(db.String(32), nullable=False, info='用户名')
    start_time = db.Column(db.DateTime, nullable=True, info='创建时间')
    retrain = db.Column(db.String(32), nullable=False, default=False, info='是否重新训练')
    end_time = db.Column(db.DateTime, nullable=True, info='任务完成时间')
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
    action = db.Column(db.Integer, nullable=True, info='动作')

    start_time = db.Column(db.DateTime, nullable=False, info='创建时间')
    
    test_task_id = db.Column(db.String(36), nullable=False, info='测试任务ID')
    test_state = db.Column(db.String(1), nullable=False, default='0', info='测试状态')
    @property
    def serialize(self):
        return to_json(self, self.__class__)
    @property
    def serialize_all(self):
        d = to_json(self, self.__class__)
        v = getattr(self, 'learner_parameters')
        d['learner_parameters'] = json.loads(v)
        return d


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
