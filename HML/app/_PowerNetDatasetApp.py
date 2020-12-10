from flask import Blueprint, request, g, json
from app.constant import get_error, RET
from app._UserApp import login_required
from utils.CommonUtil import download_file
from model import PowerNetDataset
from service import PowerNetDatasetService
import os
powerNetDatasetService = PowerNetDatasetService()

bp = Blueprint('powerNetDataset', __name__, url_prefix='/api/private/v1/data/powerNetDataset')

# 查询所有电网数据集
@bp.route('/query', methods=('GET', 'POST'))
@login_required
def query_power_net_dataset_list():
    if request.method == 'GET':
        powerNetDatasets = powerNetDatasetService.queryPowerNetDatasetList()
        if powerNetDatasets:
            powerNetDatasets = [powerNetDataset.serialize for powerNetDataset in powerNetDatasets]
        else:
            powerNetDatasets = None
        return {'meta': {'msg': 'query powerNetDataset list success', 'code': 200}, 'data': powerNetDatasets}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

# 根据当前用户ID查询该用户的所有电网数据集
@bp.route('/queryByUserId', methods=('GET', 'POST'))
@login_required
def query_power_net_dataset_list_by_user_id():
    if request.method == 'GET':
        user_id = g.user_id
        powerNetDatasets = powerNetDatasetService.queryPowerNetDatasetListByUserId(user_id)
        if powerNetDatasets:
            powerNetDatasets = [powerNetDataset.serialize for powerNetDataset in powerNetDatasets]
        else:
            powerNetDatasets = None
        return {'meta': {'msg': 'query powerNetDataset list success', 'code': 200}, 'data': powerNetDatasets}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

# 根据ID查询电网数据集和结果
@bp.route('/queryById', methods=('GET', 'POST'))
@login_required
def query_power_net_dataset_result():
    if request.method == 'GET':
        try:
            power_net_dataset_id = request.args.get('id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not power_net_dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks power_net_dataset_id')

        powerNetDataset = powerNetDatasetService.queryPowerNetDatasetById(power_net_dataset_id)

        if not powerNetDataset:
            return get_error(RET.PARAMERR, 'Error: power_net_dataset_id not exists')

        result_path = powerNetDatasetService.getPowerNetResultPath(power_net_dataset_id)
        result_data = powerNetDatasetService.getPowerNetResultData(result_path)

        return {'meta': {'msg': 'query powerNetDataset result success', 'code': 200},
                'data': {'powerNetDataset': powerNetDataset.serialize, 'resultData': result_data}}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

# 根据样例名称查询电网样例
@bp.route('/queryNetDescription', methods=('GET', 'POST'))
@login_required
def query_net_description():
    if request.method == 'GET':
        try:
            net_name = request.args.get('name')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not net_name:
            return get_error(RET.PARAMERR, 'Error: request lacks net_name')

        init_net, description = powerNetDatasetService.queryInitNetByName(net_name)

        # 图片先搞个样例的
        img_url = "http://10.214.211.205:8030/img/example_" + net_name + ".png"

        return {'meta': {'msg': 'query init net success', 'code': 200},
                'data': {'example': net_name,
                         'description': {'bus_number': description['bus'],
                                         'load_number': description['load'],
                                         'gen_number': description['gen'],
                                         'line_number': description['line']},
                         'component': {'bus': json.loads(init_net['bus'].to_json(orient="records")),
                                       'load': json.loads(init_net['load'].to_json(orient="records")),
                                       'gen': json.loads(init_net['gen'].to_json(orient="records")),
                                       'line': json.loads(init_net['line'].to_json(orient="records")),
                                       'shunt': json.loads(init_net['shunt'].to_json(orient="records")),
                                       'switch': json.loads(init_net['switch'].to_json(orient="records")),
                                       'impedance': json.loads(init_net['impedance'].to_json(orient="records")),
                                       'trafo': json.loads(init_net['trafo'].to_json(orient="records"))},
                         'img_url': img_url}}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


# 删除
@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete_powerNetDataset():
    if request.method == 'GET':
        try:
            power_net_dataset_id = request.args.get('id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not power_net_dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks power_net_dataset_id')

        powerNetDataset = powerNetDatasetService.queryPowerNetDatasetById(power_net_dataset_id)

        if not powerNetDataset:
            return get_error(RET.PARAMERR, 'Error: power_net_dataset_id not exists')

        file_path = powerNetDatasetService.getPowerNetResultPath(power_net_dataset_id)
        # if not os.path.exists(file_path):
        #     return get_error(RET.FILEERR, 'Error: powerNetDataset file not exists')

        powerNetDatasetService.deletePowerNetDataset(power_net_dataset_id, file_path)

        return {'meta': {'msg': 'delete powerNetDataset success', 'code': 200}, 'data': None}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

# 新建
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_powerNetDataset():
    # add a powerNetDataset using the params in request
    """
    request params:
    name: the name of the powerNetDataset **required**
    """
    if request.method == 'POST':
        try:
            power_net_dataset_name = request.json.get('pn_job_name')
            power_net_dataset_type = request.json.get('pn_job_type')
            power_net_dataset_description = request.json.get('pn_job_description')
            init_net_name = request.json.get('init_net_name')
            disturb_src_type_list = request.json.get('disturb_src_type_list')
            disturb_n_var = request.json.get('disturb_n_var')
            disturb_radio = request.json.get('disturb_radio')
            disturb_n_sample = request.json.get('disturb_n_sample')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        try:
            user_id = g.user_id
            username = g.user.username
        except Exception:
            return get_error(RET.SESSIONERR, 'Error: no login')

        if not power_net_dataset_name:
            return get_error(RET.PARAMERR, 'Error: request lacks power_net_dataset_name')
        if not power_net_dataset_type:
            return get_error(RET.PARAMERR, 'Error: request lacks power_net_dataset_type')
        if not init_net_name:
            return get_error(RET.PARAMERR, 'Error: request lacks init_net_name')
        if not disturb_src_type_list:
            return get_error(RET.PARAMERR, 'Error: request lacks disturb_src_type_list')
        if not disturb_n_var:
            return get_error(RET.PARAMERR, 'Error: request lacks disturb_n_var')
        if not disturb_radio:
            return get_error(RET.PARAMERR, 'Error: request lacks disturb_radio')
        if not disturb_n_sample:
            return get_error(RET.PARAMERR, 'Error: request lacks disturb_n_sample')

        #
        power_net_dataset_bean = PowerNetDataset()

        power_net_dataset_bean.power_net_dataset_name = power_net_dataset_name
        power_net_dataset_bean.power_net_dataset_type = power_net_dataset_type
        power_net_dataset_bean.power_net_dataset_description = power_net_dataset_description
        power_net_dataset_bean.init_net_name = init_net_name
        # 数组转成可存储的字符串
        power_net_dataset_bean.disturb_src_type_list = ','.join(disturb_src_type_list)
        power_net_dataset_bean.disturb_n_var = disturb_n_var
        power_net_dataset_bean.disturb_radio = disturb_radio
        power_net_dataset_bean.disturb_n_sample = disturb_n_sample
        # power_net_dataset_bean.start_time = start_time
        # power_net_dataset_bean.generate_state = generate_state
        power_net_dataset_bean.user_id = user_id
        power_net_dataset_bean.username = username

        powerNetDataset = powerNetDatasetService.addPowerNetDataset(power_net_dataset_bean).serialize

        msg = 'add powerNetDataset success and train immediately'
        code = 204

        return {'meta': {'msg': msg, 'code': code}, 'data': powerNetDataset}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

# 下载结果
@bp.route('/download/result', methods=('GET', 'POST'))
@login_required
def download_result():
    if request.method == 'GET':
        try:
            power_net_dataset_id = request.args.get('id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not power_net_dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks power_net_dataset_id')

        powerNetDataset = powerNetDatasetService.queryPowerNetDatasetById(power_net_dataset_id)

        if not powerNetDataset:
            return get_error(RET.PARAMERR, 'Error: power_net_dataset_id not exists')

        file_path = powerNetDatasetService.getPowerNetResultPath(power_net_dataset_id)
        if not os.path.exists(file_path):
            return get_error(RET.FILEERR, 'Error: result file not exists')

        file = download_file(file_path)

        return file, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

# 任务状态
@bp.route('/generate_state', methods=('GET', 'POST'))
@login_required
def get_task_generate_state():
    if request.method == 'GET':
        try:
            task_id = request.args.get('id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not task_id:
            return get_error(RET.PARAMERR, 'Error: request lacks task_id')

        data = powerNetDatasetService.getTaskGenerateState(task_id)

        return {'meta': {'msg': 'get state success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405
