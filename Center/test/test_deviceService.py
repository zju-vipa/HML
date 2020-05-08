from app import deviceService
from model import Device

def test_addDevice():
    device = Device()
    device.id = '123123'
    device.created_by = '123'
    device.name = "205"
    device.token = " "
    deviceService.addDevice(device)

def test_getDeviceList():
    devices = deviceService.getMyDeviceList("a8439e6632b14b11b62a88a849546658")
    print(devices)