from flask import Blueprint, request, g, jsonify
from app.auth import login_required, device_required
from app.constant import RET, get_error
import json
from model import Device
from app import deviceService

bp = Blueprint('device', __name__, url_prefix='/device')

@bp.route('/list', methods=('GET', 'POST'))
@login_required
def get_list():
    template = ['name', 'token','info']
    device_list = deviceService.getMyDeviceList(g.userid)
    for idx,device in enumerate(device_list):
        device.update({"idx":idx})
        info = device['info']
        if info is not None and len(info) > 0:
            print('info is', info)
            info = json.loads(info)
            device.update({'info': info})
    print(device_list)
    return jsonify(device_list)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def add_device():
    if request.method == 'POST':
        userid = g.userid
        name = request.form.get('name')
        if name is None:
            return get_error(RET.PARAMERR)
        # add to database
        device = Device()
        device.created_by = userid
        device.name = name
        deviceService.addDevice(device)
        return {"msg": "add device success"}
    return {"msg": "method not allowed"}, 404


@bp.route('/update', methods=('GET', 'POST'))
@device_required
def update_usage():
    if request.method == 'POST':
        device_id = g.device_id
        info = request.form.get('info')
        print(request.form)
        if not info:
            return "Not OK",404
        deviceService.updateInfo(device_id, info)
        return "OK"

