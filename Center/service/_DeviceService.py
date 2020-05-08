from dao import DeviceDao
from model import Device, db
import uuid
from utils.EncryptUtil import create_machine_token

class DeviceService:

    def __init__(self):
        self.deviceDao = DeviceDao(db)

    def addDevice(self,device):
        device.id = str(uuid.uuid4()).replace('-', '')
        device.token = create_machine_token(device.id)
        self.deviceDao.addDevice(device)

    def getMyDeviceList(self, userid):
        devices = self.deviceDao.getDeviceListByUserid(userid)
        new_devices = []
        for device in devices:
            new_device = device.serialize
            new_devices.append(new_device)
        return new_devices

    def getDeviceById(self, device_id):
        device = self.deviceDao.queryDeviceById(device_id)
        if device is not None:
            device = device.serialize
        return device

    """
    update the device info,
        which contains gpu usage, gpu remains
    """
    def updateInfo(self, device_id, info):
        device = self.deviceDao.queryDeviceById(device_id)
        if device is None:
            # todo: add illegal argument exception here
            pass
        device.info = info
        self.deviceDao.updateDevice(device)


