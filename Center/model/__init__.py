from app import sql_db as db
import json
import datetime
from datetime import date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def to_json(inst, cls):
    d = dict()
    '''
    获取表里面的列并存到字典里面
    '''
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        d[c.name] = v
    return d

class Dataset(db.Model):
    __tablename__ = 'dataset'

    id = db.Column(db.String(36), primary_key=True, info='数据集id')
    dataturks_id = db.Column(db.String(36), info='dataturks的对应id')
    name = db.Column(db.Text, info='数据集名')
    created_by = db.Column(db.String(36), nullable=False, info='创建者id')
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='创建时间')
    updated_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间')
    public = db.Column(db.Integer, info='访问权限')
    config = db.Column(db.Text, info='配置文件')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.String(36), primary_key=True, info='设备id')
    created_by = db.Column(db.String(36), nullable=False, info='创建人')
    name = db.Column(db.String(128), info='自定义设备名')
    token = db.Column(db.Text, nullable=False, info='token')
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='创建时间')
    updated_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间')
    info = db.Column(db.Text, info='设备信息')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class Model(db.Model):
    __tablename__ = 'model'

    id = db.Column(db.String(36), primary_key=True, info='模型id')
    created_by = db.Column(db.String(36), nullable=False, info='拥有者id')
    name = db.Column(db.Text, info='模型名')
    type = db.Column(db.String(36), info='数据集类型')
    code_path = db.Column(db.Text, info='模型路径')
    config = db.Column(db.Text, info='配置')
    public = db.Column(db.Integer, info='公开')
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='创建时间')
    updated_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.String(36), primary_key=True, info='任务id')
    name = db.Column(db.String(36), info='任务名')
    created_by = db.Column(db.String(36), info='创建人')
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='创建时间')
    type = db.Column(db.String(36), info='任务类型')
    public = db.Column(db.Integer, info='是否为公开任务')
    dataset_id = db.Column(db.String(36), info='数据集id')
    updated_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间')
    status = db.Column(db.Integer, info='任务状态,1为已接收，2为任务结束')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class Train(db.Model):
    __tablename__ = 'train'

    id = db.Column(db.String(36), primary_key=True, info='训练状态id')
    task_id = db.Column(db.String(36), nullable=False, info='任务id')
    model_id = db.Column(db.String(36), info='模型id')
    created_by = db.Column(db.String(36), nullable=False, info='创建者id')
    device_id = db.Column(db.String(36), info='设备id')
    status = db.Column(db.Integer, info='状态')
    detail = db.Column(db.Text, info='训练细节')
    updated_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间')

    @property
    def serialize(self):
        return to_json(self, self.__class__)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(36), primary_key=True, info='ID')
    email = db.Column(db.String(128), nullable=False, info='邮箱')
    username = db.Column(db.String(128), nullable=False, info='用户名')
    type = db.Column(db.String(36), info='角色')
    password = db.Column(db.String(36), nullable=False, info='密码')
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='创建时间 用户创建时间')
    updated_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间 用户信息更新时间')

    @property
    def serialize(self):
        return to_json(self, self.__class__)

class DUser(db.Model):
    __bind_key__ = 'dataturks_db'
    __tablename__ = 'd_users'

    id = db.Column(db.String(36), primary_key=True)
    oAuthId = db.Column(db.String(48), nullable=False, unique=True)
    oAuthType = db.Column(db.String(20))
    firstName = db.Column(db.String(50))
    secondName = db.Column(db.String(50))
    city = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    profileLink = db.Column(db.String(300))
    profilePic = db.Column(db.String(300))
    status = db.Column(db.String(10))
    notificationToken = db.Column(db.Text)
    password = db.Column(db.String(64))
    notes = db.Column(db.Text)
    created_timestamp = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_timestamp = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    @property
    def serialize(self):
        return to_json(self, self.__class__)