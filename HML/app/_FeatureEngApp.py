from flask import Blueprint, request, g, json
from app.constant import get_error, RET
from app._UserApp import login_required
from model import FeatureEng
from service import FeatureEngService
from service import DatasetService
featureEngService = FeatureEngService()
datasetService = DatasetService()

bp = Blueprint('featureEng', __name__, url_prefix='/api/private/v1/featureEng')


@bp.route('/query', methods=('GET', 'POST'))
@login_required
def query_featureEng_list():
    if request.method == 'GET':
        user_id = g.user_id
        featureEngs = featureEngService.queryFeatureEngListByUserId(user_id)
        if featureEngs:
            featureEngs = [featureEng.serialize for featureEng in featureEngs]
        else:
            featureEngs = None
        return {'meta': {'msg': 'query featureEng list success', 'code': 200}, 'data': featureEngs}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete_featureEng():
    if request.method == 'GET':
        try:
            featureEng_id = request.args.get('featureEng_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not featureEng_id:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_id')

        featureEng = featureEngService.queryFeatureEngById(featureEng_id)

        if not featureEng:
            return get_error(RET.PARAMERR, 'Error: featureEng_id not exists')

        file_directory = featureEngService.getFeatureEngFileDirectory(featureEng)

        if not file_directory:
            return get_error(RET.FILEERR, 'Error: featureEng file directory not exists')

        featureEngService.deleteFeatureEng(featureEng_id, file_directory)

        return {'meta': {'msg': 'delete featureEng success', 'code': 200}, 'data': None}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_featureEng():
    # add a featureEng using the params in request
    """
    request params:
    name: the name of the featureEng **required**
    """
    if request.method == 'POST':
        try:
            featureEng_name = request.json.get('featureEng_name')
            featureEng_type = request.json.get('featureEng_type')
            featureEng_processes = request.json.get('featureEng_processes')
            original_dataset_id = request.json.get('original_dataset_id')
            new_dataset_name = request.json.get('new_dataset_name')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        try:
            user_id = g.user_id
            username = g.user.username
        except Exception:
            return get_error(RET.SESSIONERR, 'Error: no login')

        if not featureEng_name:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_name')
        if not featureEng_type:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_type')
        if not featureEng_processes:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_processes')
        if not original_dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks original_dataset_id')
        if not new_dataset_name:
            return get_error(RET.PARAMERR, 'Error: request lacks new_dataset_name')

        original_dataset = datasetService.queryDatasetById(original_dataset_id)

        if not original_dataset:
            return get_error(RET.PARAMERR, 'Error: original_dataset_id not exists')

        original_dataset_file_path = datasetService.getDatasetFilePath(original_dataset)

        if not original_dataset_file_path:
            return get_error(RET.FILEERR, 'Error: original dataset file not exists')

        featureEng_bean = FeatureEng()
        featureEng_bean.featureEng_name = featureEng_name
        featureEng_bean.featureEng_type = featureEng_type
        featureEng_bean.featureEng_processes = json.dumps(featureEng_processes, ensure_ascii=False)
        featureEng_bean.original_dataset_id = original_dataset_id
        featureEng_bean.user_id = user_id
        featureEng_bean.username = username

        featureEng = featureEngService.addFeatureEng(featureEng_bean,
                                                     featureEng_processes,
                                                     original_dataset,
                                                     original_dataset_file_path,
                                                     new_dataset_name).serialize

        msg = 'add featureEng success and operate immediately'
        code = 204

        return {'meta': {'msg': msg, 'code': code}, 'data': featureEng}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/task/operate/state', methods=('GET', 'POST'))
@login_required
def get_task_operate_state():
    if request.method == 'GET':
        try:
            task_id = request.args.get('task_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not task_id:
            return get_error(RET.PARAMERR, 'Error: request lacks task_id')

        data = featureEngService.getTaskOperateState(task_id)

        return {'meta': {'msg': 'get state success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405
