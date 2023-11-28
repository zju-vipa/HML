import os
from flask import Blueprint, request, g, json, current_app
from app.constant import get_error, RET
from app._UserApp import login_required
from model import FeatureEng
from service import FeatureEngService
from service import DatasetService
from datetime import datetime
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
            file_directory = os.path.join(current_app.config["SAVE_FE_MODEL_PATH"], featureEng.featureEng_id)
            if os.path.exists(file_directory):
                featureEngService.deleteFeatureEng(featureEng_id, file_directory)
        else:
            featureEngService.deleteFeatureEng(featureEng_id, file_directory)
            file_directory = os.path.join(current_app.config["SAVE_FE_MODEL_PATH"], featureEng.featureEng_id)
            if os.path.exists(file_directory):
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

# 最新结果：任务概况
@bp.route('/task/queryLatestResult', methods=('GET', 'POST'))
@login_required
def queryLatestResult():
    if request.method == 'GET':
        try:
            user_id = g.user_id
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not user_id:
            return get_error(RET.PARAMERR, 'Error: request lacks user_id')
        featureEng = featureEngService.getLatestTaskDetails(user_id)
        if featureEng:
            dataset = datasetService.queryDatasetById(featureEng.original_dataset_id)
            taskDetails = {}
            taskDetails['isNewResult'] = True
            taskDetails['name'] = featureEng.featureEng_name
            if featureEng.featureEng_type == 'Machine':
                taskDetails['type'] = '纯机器方法'
            elif featureEng.featureEng_type == 'HumanInLoop':
                taskDetails['type'] = '人机协同特征学习与衍生技术'
            else:
                taskDetails['type'] = '纯人工方法'
            if featureEng.featureEng_operationMode == '1':
                taskDetails['mode'] = '001夏平初始'
            taskDetails['network'] = '300节点电网'
            taskDetails['checkedModules'] = featureEng.featureEng_modules
            taskDetails['original_efficiency'] = featureEng.FeatureEng_efficiency
            taskDetails['original_accuracy'] = featureEng.FeatureEng_accuracy
            taskDetails['dataset'] = dataset.dataset_name
        else:
            taskDetails = {}
            taskDetails['isNewResult'] = False
        return {'meta': {'msg': 'get details of latest task success', 'code': 200}, 'data': taskDetails}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


# 最新结果：当前任务交互记录
@bp.route('/task/queryLatestRecord', methods=('GET', 'POST'))
@login_required
def queryLatestRecord():
    if request.method == 'GET':
        try:
            user_id = g.user_id
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')
        if not user_id:
            return get_error(RET.PARAMERR, 'Error: request lacks user_id')
        record = featureEngService.getLatestRecord(user_id)
        if record:
            record = json.dumps(record)
        else:
            record = None
        return {'meta': {'msg': 'query latest record', 'code': 200}, 'data': record}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


# 最新结果：当前任务特征
@bp.route('/task/queryLatestFeature', methods=('GET', 'POST'))
@login_required
def queryLatestFeature():
    if request.method == 'GET':
        try:
            user_id = g.user_id
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not user_id:
            return get_error(RET.PARAMERR, 'Error: request lacks user_id')
        featureEng = featureEngService.getLatestTaskDetails(user_id)
        featureList = featureEngService.getTaskFeatureList(featureEng.featureEng_id)
        if featureList:
            featureList = json.dumps(featureList)
        else:
            featureList = None
        return {'meta': {'msg': 'query featureEng list success', 'code': 200}, 'data': featureList}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


# 最新结果：前100特征重要性
@bp.route('/task/queryLatestImportance', methods=('GET', 'POST'))
@login_required
def queryLatestImportance():
    if request.method == 'GET':
        try:
            user_id = g.user_id
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')
        scores = featureEngService.queryFeatureScores(user_id)
        if scores:
            scores = json.dumps(scores)
        else:
            scores = None
        return {'meta': {'msg': 'query feature importance success', 'code': 200}, 'data': scores}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


# 特征库
@bp.route('/task/queryFeatureLibrary', methods=('GET', 'POST'))
@login_required
def queryFeatureLibrary():
    if request.method == 'GET':
        user_id = g.user_id
        featureLibrary = featureEngService.queryFeatureLibraryByUserId(user_id)
        if featureLibrary:
            featureLibrary = json.dumps(featureLibrary)
        else:
            featureLibrary = None
        return {'meta': {'msg': 'query featureEng list success', 'code': 200}, 'data': featureLibrary}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

# 创建特征工程任务
@bp.route('/task/addFeatureEngTask', methods=('GET', 'POST'))
@login_required
def addFeatureEngTask():
    if request.method == 'POST':
        try:
            featureEng_name = request.json.get('featureEng_name')
            featureEng_type = request.json.get('featureEng_type')
            featureEng_operationMode = request.json.get('featureEng_operationMode')
            featureEng_modules = request.json.get('featureEng_modules')
            featureEng_processes = request.json.get('featureEng_processes')
            original_dataset_id = request.json.get('original_dataset_id')
            new_dataset_name = request.json.get('new_dataset_name')
            current_app.logger.info('featureEng_processes')
            current_app.logger.info(featureEng_processes)
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
        if not featureEng_operationMode:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_operationMode')
        if not featureEng_modules:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_modules')
        if not featureEng_processes:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_processes')
        if not original_dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks original_dataset_id')
        if not new_dataset_name:
            return get_error(RET.PARAMERR, 'Error: request lacks new_dataset_name')
        current_app.logger.info('load original dataset')
        original_dataset = datasetService.queryDatasetById(original_dataset_id)
        current_app.logger.info(original_dataset)
        if not original_dataset:
            return get_error(RET.PARAMERR, 'Error: original_dataset_id not exists')


        original_dataset_file_path = datasetService.getDatasetFilePath(original_dataset)

        current_app.logger.info(original_dataset_file_path)

        if not original_dataset_file_path:
            return get_error(RET.FILEERR, 'Error: original dataset file not exists')

        featureEng_bean = FeatureEng()
        featureEng_bean.featureEng_name = featureEng_name
        featureEng_bean.featureEng_type = featureEng_type
        featureEng_bean.featureEng_operationMode = featureEng_operationMode
        moduleString = ''
        for i in range(len(featureEng_modules)):
            moduleString = moduleString + str(featureEng_modules[i]) + ','
        moduleString = moduleString[:-1]
        current_app.logger.info('moduleString')
        current_app.logger.info(moduleString)
        featureEng_bean.featureEng_modules = moduleString
        featureEng_bean.featureEng_processes = json.dumps(featureEng_processes, ensure_ascii=False)
        featureEng_bean.original_dataset_id = original_dataset_id
        featureEng_bean.user_id = user_id
        featureEng_bean.username = username
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        featureEng_bean.start_time = start_time
        featureEng = featureEngService.addFeatureEng(featureEng_bean,
                                                     featureEng_processes,
                                                     original_dataset,
                                                     original_dataset_file_path,
                                                     new_dataset_name).serialize

        msg = 'add featureEng success and operate immediately'
        code = 204
        return {'meta': {'msg': msg, 'code': code}, 'data': featureEng}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

@bp.route('/task/queryTaskStatus', methods=('GET', 'POST'))
@login_required
def queryTaskStatus():
    if request.method == 'GET':
        try:
            task_id = request.args.get('task_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: request lacks task_id')

        running_message = featureEngService.getTaskStatus(task_id)
        return {'meta': {'msg': 'query featureEng list success', 'code': 200}, 'data': json.dumps(running_message)}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/result/querySelectedTaskResults', methods=('GET', 'POST'))
@login_required
def querySelectedTaskResults():
    if request.method == 'GET':
        try:
            featureEng_id = request.args.get('featureEng_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not featureEng_id:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_id')

        featureEng = featureEngService.queryFeatureEngById(featureEng_id)
        if featureEng:
            dataset = datasetService.queryDatasetById(featureEng.original_dataset_id)
            taskDetails = {}
            taskDetails['isNewResult'] = True
            taskDetails['name'] = featureEng.featureEng_name
            if featureEng.featureEng_type == 'Machine':
                taskDetails['type'] = '纯机器方法'
            elif featureEng.featureEng_type == 'HumanInLoop':
                taskDetails['type'] = '人机协同特征学习与衍生技术'
            else:
                taskDetails['type'] = '纯人工方法'
            if featureEng.featureEng_operationMode == '1':
                taskDetails['mode'] = '001夏平初始'
            taskDetails['network'] = '300节点电网'
            taskDetails['checkedModules'] = featureEng.featureEng_modules
            taskDetails['original_efficiency'] = featureEng.FeatureEng_efficiency
            taskDetails['original_accuracy'] = featureEng.FeatureEng_accuracy
            taskDetails['dataset'] = dataset.dataset_name
        else:
            taskDetails = {}
            taskDetails['isNewResult'] = False
        return {'meta': {'msg': 'get details of latest task success', 'code': 200}, 'data': taskDetails}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

@bp.route('/result/querySelectedTaskFeatures', methods=('GET', 'POST'))
@login_required
def querySelectedTaskFeatures():
    if request.method == 'GET':
        try:
            featureEng_id = request.args.get('featureEng_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not featureEng_id:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_id')

        featureList = featureEngService.getTaskFeatureList(featureEng_id)
        if featureList:
            featureList = json.dumps(featureList)
        else:
            featureList = None
        return {'meta': {'msg': 'query featureEng list success', 'code': 200}, 'data': featureList}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

@bp.route('/result/querySelectedTaskRecord', methods=('GET', 'POST'))
@login_required
def querySelectedTaskRecord():
    if request.method == 'GET':
        try:
            featureEng_id = request.args.get('featureEng_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        record = featureEngService.querySelectedTaskRecord(featureEng_id)
        if record:
            record = json.dumps(record)
        else:
            record = None
        return {'meta': {'msg': 'query latest record', 'code': 200}, 'data': record}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

@bp.route('/result/querySelectedImportance', methods=('GET', 'POST'))
@login_required
def querySelectedImportance():
    if request.method == 'GET':
        try:
            featureEng_id = request.args.get('featureEng_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')
        scores = featureEngService.querySelectedTaskScores(featureEng_id)
        if scores:
            scores = json.dumps(scores)
        else:
            scores = None
        return {'meta': {'msg': 'query feature importance success', 'code': 200}, 'data': scores}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405
