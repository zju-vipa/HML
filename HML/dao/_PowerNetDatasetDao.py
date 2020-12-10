from model import PowerNetDataset
from dao._BaseDao import BaseDao

"""
used for Learner related database operation
"""


class PowerNetDatasetDao(BaseDao):

    def __init__(self, db):
        super().__init__(db, PowerNetDataset)

    """
    provide functions of base class another name 
    """
    def addPowerNetDataset(self, power_net_dataset):
        self.add(power_net_dataset)

    def deletePowerNetDataset(self, power_net_dataset_id):
        power_net_dataset = PowerNetDataset.query.filter_by(power_net_dataset_id=power_net_dataset_id).first()
        self.delete(power_net_dataset)

    def queryPowerNetDatasetById(self, power_net_dataset_id):
        power_net_dataset = PowerNetDataset.query.filter_by(power_net_dataset_id=power_net_dataset_id).first()
        return power_net_dataset

    def queryPowerNetDatasetListByUserId(self, user_id):
        power_net_datasets = PowerNetDataset.query.filter_by(user_id=user_id).order_by('start_time').all()
        return power_net_datasets

    def queryPowerNetDatasetList(self):
        power_net_datasets = PowerNetDataset.query.order_by('start_time').all()
        return power_net_datasets

    def updatePowerNetDataset(self, power_net_dataset_bean):
        power_net_dataset = PowerNetDataset.query.filter_by(power_net_dataset_id=power_net_dataset_bean.power_net_dataset_id).first()
        # not update task_id
        power_net_dataset.power_net_dataset_name = power_net_dataset_bean.power_net_dataset_name
        power_net_dataset.power_net_dataset_type = power_net_dataset_bean.power_net_dataset_type
        power_net_dataset.power_net_dataset_description = power_net_dataset_bean.power_net_dataset_description
        power_net_dataset.init_net_name = power_net_dataset_bean.init_net_name
        power_net_dataset.disturb_src_type_list = power_net_dataset_bean.disturb_src_type_list
        power_net_dataset.disturb_n_var = power_net_dataset_bean.disturb_n_var
        power_net_dataset.disturb_radio = power_net_dataset_bean.disturb_radio
        power_net_dataset.disturb_n_sample = power_net_dataset_bean.disturb_n_sample
        power_net_dataset.start_time = power_net_dataset_bean.start_time
        power_net_dataset.generate_state = power_net_dataset_bean.generate_state
        power_net_dataset.user_id = power_net_dataset_bean.user_id
        power_net_dataset.username = power_net_dataset_bean.username
        self.db.session.commit()
