# import all dao class to this module
from dao._UserDao import UserDao
from dao._DatasetDao import DatasetDao
from dao._DeviceDao import DeviceDao
from dao._TrainDao import TrainDao
from dao._ModelDao import ModelDao
from dao._TaskDao import TaskDao

# use the template to transfer the dao bean to a dict
def transfer(bean, template):
    new_bean = {}
    for key in template:
        new_bean[key] = getattr(bean, key, None)
    return new_bean

def transfer_list(bean_list, template):
    new_list = []
    for bean in bean_list:
        new_list.append(transfer(bean, template))
    return new_list