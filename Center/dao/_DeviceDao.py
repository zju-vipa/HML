from model import Device
from dao._BaseDao import BaseDao

"""
used for device related database operation
"""
class DeviceDao(BaseDao):

    def __init__(self, db):
        super().__init__(db, Device)

    """
    provide functions of base class another name 
    """
    def addDevice(self, device):
        self.add(device)

    def deleteDevice(self, deviceId):
        self.delete(deviceId)

    def updateDevice(self, device):
        self.update(device)

    def queryDeviceById(self, deviceId):
        return self.queryById(deviceId)


    """
    return the Devices of the user
    """
    def getDeviceListByUserid(self, userid):
        devices = Device.query.filter_by(created_by=userid).all()
        return devices