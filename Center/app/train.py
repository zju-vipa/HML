import traceback
from flask import Blueprint, request, g, jsonify
from app.auth import login_required, device_required
from app.constant import get_error, RET
from app import trainService

bp = Blueprint('train', __name__, url_prefix='/train')

@bp.route('/create', methods=('POST',))
@login_required
def add():
    # add a train using the params in request
    """
    request params:
    :task_id the id of the task **required**
    :model_id the id of the model **required**
    """
    if request.method == 'POST':
        userid = g.userid
        task_id = request.form.get('task_id')
        model_id = request.form.get('model_id')
        print('model is',model_id)
        print('task is', task_id)
        if task_id is None or model_id is None:
            return get_error(RET.PARAMERR)
        # todo: add user validation of the task and model
        # description: the task_id must be (public) or (private but same user)
        #              the model_id must be (public) or (private but same user)
        #              the task_id should not have been training
        trainService.addTrain(userid, task_id,model_id)
        return {"msg": "add train success"}

    return {"msg": "method not allowed"}, 404


"""
used for device
"""

@bp.route('/undo_list', methods=('GET',))
@device_required
def get_undo_list():
    # get undo list, this function is for devices
    undo_trains = trainService.getUndoTrainList()
    return jsonify(undo_trains)

@bp.route('/accept/<string:train_id>', methods=('GET',))
@device_required
def accept_train(train_id):
    # accept a train, this function is for devices
    device_id = g.device_id
    try:
        trainService.acceptTrain(device_id, train_id)
    except ValueError:
        print(traceback.format_exc())
        return {"msg": "parameter wrong"}, 404
    except Exception:
        print(traceback.format_exc())
        return {"msg": "unknown exception"}, 404
    return {"msg": "OK"}

@bp.route('/active_list', methods=('GET',))
@device_required
def get_active_train():
    # get undo list, this function is for devices
    detail_trian = trainService.getDeviceActiveTrain(g.device_id)
    return jsonify(detail_trian)

@bp.route('/update/<string:train_id>', methods=('POST',))
@device_required
def update_train_detail(train_id):
    # update status, this function is for devices
    # form_data:
    #   @detail: the detail you want to upload
    # todo: function test
    device_id = g.device_id
    detail = request.form.get("detail")
    trainService.update_detail(device_id, train_id, detail)
    return "OK"

@bp.route('/complete/<string:train_id>', methods=('GET','POST'))
@device_required
def complete_train(train_id):
    # todo: complete a train, this function is for devices
    try:
        device_id = g.device_id
        trainService.complete_train(device_id,train_id)
    except ValueError:
        print(traceback.format_exc())
        return {"msg": "parameter wrong"}, 404
    except Exception:
        print(traceback.format_exc())
        return {"msg": "unknown exception"}, 404
    return {"msg": "OK"}