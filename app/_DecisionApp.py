from flask import Blueprint, request, g, json
from app.constant import get_error, RET
from app._UserApp import login_required
from utils.CommonUtil import download_file
from model import Decision
from service import DecisionService
from service import DatasetService
from service import FeatureEngService
from service import LearnerService
decisionService = DecisionService()
datasetService = DatasetService()
featureEngService = FeatureEngService()
learnerService = LearnerService()

bp = Blueprint('decision', __name__, url_prefix='/api/private/v1/decision')


@bp.route('/query', methods=('GET', 'POST'))
@login_required
def query_decision_list():
    if request.method == 'GET':
        user_id = g.user_id
        decisions = decisionService.queryDecisionListByUserId(user_id)
        if decisions:
            decisions = [decision.serialize for decision in decisions]
        else:
            decisions = None
        return {'meta': {'msg': 'query decision list success', 'code': 200}, 'data': decisions}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete_decision():
    if request.method == 'GET':
        try:
            decision_id = request.args.get('decision_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not decision_id:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_id')

        decision = decisionService.queryDecisionById(decision_id)

        if not decision:
            return get_error(RET.PARAMERR, 'Error: decision_id not exists')

        file_directory = decisionService.getDecisionFileDirectory(decision)

        if not file_directory:
            return get_error(RET.FILEERR, 'Error: decision file directory not exists')

        decisionService.deleteDecision(decision_id, file_directory)

        return {'meta': {'msg': 'delete decision success', 'code': 200}, 'data': None}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/apply/featureEng', methods=('GET', 'POST'))
@login_required
def apply_featureEng():
    # add a decision using the params in request
    """
    request params:
    name: the name of the decision **required**
    """
    if request.method == 'POST':
        try:
            decision_name = request.json.get('decision_name')
            decision_type = request.json.get('decision_type')
            decision_parameters = request.json.get('decision_parameters')
            featureEng_id = request.json.get('featureEng_id')
            dataset_id = request.json.get('dataset_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        try:
            user_id = g.user_id
            username = g.user.username
        except Exception:
            return get_error(RET.SESSIONERR, 'Error: no login')

        if not decision_name:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_name')
        if not decision_type:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_type')
        if not decision_parameters:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_parameters')
        if not featureEng_id:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_id')
        if not dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_id')

        dataset = datasetService.queryDatasetById(dataset_id)

        if not dataset:
            return get_error(RET.PARAMERR, 'Error: dataset_id not exists')

        dataset_file_path = datasetService.getDatasetFilePath(dataset)

        if not dataset_file_path:
            return get_error(RET.FILEERR, 'Error: dataset file not exists')

        featureEng = featureEngService.queryFeatureEngById(featureEng_id)

        if not featureEng:
            return get_error(RET.PARAMERR, 'Error: featureEng_id not exists')

        featureEng_processes = json.loads(featureEng.featureEng_processes)

        decision_bean = Decision()
        decision_bean.decision_name = decision_name
        decision_bean.decision_type = decision_type
        decision_bean.decision_parameters = json.dumps(decision_parameters, ensure_ascii=False)
        decision_bean.featureEng_id = featureEng_id
        decision_bean.dataset_id = dataset_id
        decision_bean.user_id = user_id
        decision_bean.username = username

        decision = decisionService.applyFeatureEng(decision_bean,
                                                   decision_parameters,
                                                   featureEng_id,
                                                   featureEng_processes,
                                                   dataset_file_path).serialize

        msg = 'add decision success and apply immediately'
        code = 204

        return {'meta': {'msg': msg, 'code': code}, 'data': decision}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/apply/learner', methods=('GET', 'POST'))
@login_required
def apply_learner():
    # add a decision using the params in request
    """
    request params:
    name: the name of the decision **required**
    """
    if request.method == 'POST':
        try:
            decision_name = request.json.get('decision_name')
            decision_type = request.json.get('decision_type')
            decision_parameters = request.json.get('decision_parameters')
            learner_id = request.json.get('learner_id')
            dataset_id = request.json.get('dataset_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        try:
            user_id = g.user_id
            username = g.user.username
        except Exception:
            return get_error(RET.SESSIONERR, 'Error: no login')

        if not decision_name:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_name')
        if not decision_type:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_type')
        if not decision_parameters:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_parameters')
        if not learner_id:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_id')
        if not dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_id')

        dataset = datasetService.queryDatasetById(dataset_id)

        if not dataset:
            return get_error(RET.PARAMERR, 'Error: dataset_id not exists')

        dataset_file_path = datasetService.getDatasetFilePath(dataset)

        if not dataset_file_path:
            return get_error(RET.FILEERR, 'Error: dataset file not exists')

        learner = learnerService.queryLearnerById(learner_id)

        if not learner:
            return get_error(RET.PARAMERR, 'Error: learner_id not exists')

        learner_parameters = json.loads(learner.learner_parameters)

        decision_bean = Decision()
        decision_bean.decision_name = decision_name
        decision_bean.decision_type = decision_type
        decision_bean.decision_parameters = json.dumps(decision_parameters, ensure_ascii=False)
        decision_bean.learner_id = learner_id
        decision_bean.dataset_id = dataset_id
        decision_bean.user_id = user_id
        decision_bean.username = username

        decision = decisionService.applyLearner(decision_bean,
                                                decision_parameters,
                                                learner_id,
                                                learner_parameters,
                                                dataset_file_path).serialize

        msg = 'add decision success and apply immediately'
        code = 204

        return {'meta': {'msg': msg, 'code': code}, 'data': decision}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/apply/decision', methods=('GET', 'POST'))
@login_required
def apply_decision():
    # add a decision using the params in request
    """
    request params:
    name: the name of the decision **required**
    """
    if request.method == 'POST':
        try:
            decision_name = request.json.get('decision_name')
            decision_type = request.json.get('decision_type')
            decision_parameters = request.json.get('decision_parameters')
            featureEng_id = request.json.get('featureEng_id')
            learner_id = request.json.get('learner_id')
            dataset_id = request.json.get('dataset_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        try:
            user_id = g.user_id
            username = g.user.username
        except Exception:
            return get_error(RET.SESSIONERR, 'Error: no login')

        if not decision_name:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_name')
        if not decision_type:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_type')
        if not decision_parameters:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_parameters')
        if not featureEng_id:
            return get_error(RET.PARAMERR, 'Error: request lacks featureEng_id')
        if not learner_id:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_id')
        if not dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_id')

        dataset = datasetService.queryDatasetById(dataset_id)

        if not dataset:
            return get_error(RET.PARAMERR, 'Error: dataset_id not exists')

        dataset_file_path = datasetService.getDatasetFilePath(dataset)

        if not dataset_file_path:
            return get_error(RET.FILEERR, 'Error: dataset file not exists')

        featureEng = featureEngService.queryFeatureEngById(featureEng_id)

        if not featureEng:
            return get_error(RET.PARAMERR, 'Error: featureEng_id not exists')

        featureEng_processes = json.loads(featureEng.featureEng_processes)

        learner = learnerService.queryLearnerById(learner_id)

        if not learner:
            return get_error(RET.PARAMERR, 'Error: learner_id not exists')

        learner_parameters = json.loads(learner.learner_parameters)

        decision_bean = Decision()
        decision_bean.decision_name = decision_name
        decision_bean.decision_type = decision_type
        decision_bean.decision_parameters = json.dumps(decision_parameters, ensure_ascii=False)
        decision_bean.featureEng_id = featureEng_id
        decision_bean.learner_id = learner_id
        decision_bean.dataset_id = dataset_id
        decision_bean.user_id = user_id
        decision_bean.username = username

        decision = decisionService.applyDecision(decision_bean,
                                                 decision_parameters,
                                                 featureEng_id,
                                                 featureEng_processes,
                                                 learner_id,
                                                 learner_parameters,
                                                 dataset_file_path).serialize

        msg = 'add decision success and apply immediately'
        code = 204

        return {'meta': {'msg': msg, 'code': code}, 'data': decision}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/download/transform', methods=('GET', 'POST'))
@login_required
def download_transform():
    if request.method == 'GET':
        try:
            decision_id = request.args.get('decision_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not decision_id:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_id')

        decision = decisionService.queryDecisionById(decision_id)

        if not decision:
            return get_error(RET.PARAMERR, 'Error: decision_id not exists')

        file_path = decisionService.getTransformFilePath(decision)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: transform file not exists')

        file = download_file(file_path)

        return file, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/download/prediction', methods=('GET', 'POST'))
@login_required
def download_prediction():
    if request.method == 'GET':
        try:
            decision_id = request.args.get('decision_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not decision_id:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_id')

        decision = decisionService.queryDecisionById(decision_id)

        if not decision:
            return get_error(RET.PARAMERR, 'Error: decision_id not exists')

        file_path = decisionService.getPredictionFilePath(decision)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: prediction file not exists')

        file = download_file(file_path)

        return file, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/download/report', methods=('GET', 'POST'))
@login_required
def download_report():
    if request.method == 'GET':
        try:
            decision_id = request.args.get('decision_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not decision_id:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_id')

        decision = decisionService.queryDecisionById(decision_id)

        if not decision:
            return get_error(RET.PARAMERR, 'Error: decision_id not exists')

        file_path = decisionService.getReportFilePath(decision)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: report file not exists')

        file = download_file(file_path)

        return file, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/data/transform', methods=('GET', 'POST'))
@login_required
def get_transform_data():
    if request.method == 'GET':
        try:
            decision_id = request.args.get('decision_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not decision_id:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_id')

        decision = decisionService.queryDecisionById(decision_id)

        if not decision:
            return get_error(RET.PARAMERR, 'Error: decision_id not exists')

        file_path = decisionService.getTransformFilePath(decision)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: transform file not exists')

        data = decisionService.getTransformData(file_path)

        if not data:
            return get_error(RET.DATAERR, 'Error: file lacks data or data format error')

        return {'meta': {'msg': 'get prediction data success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/data/prediction', methods=('GET', 'POST'))
@login_required
def get_prediction_data():
    if request.method == 'GET':
        try:
            decision_id = request.args.get('decision_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not decision_id:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_id')

        decision = decisionService.queryDecisionById(decision_id)

        if not decision:
            return get_error(RET.PARAMERR, 'Error: decision_id not exists')

        file_path = decisionService.getPredictionFilePath(decision)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: prediction file not exists')

        data = decisionService.getPredictionData(file_path)

        if not data:
            return get_error(RET.DATAERR, 'Error: file lacks data or data format error')

        return {'meta': {'msg': 'get prediction data success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/data/report', methods=('GET', 'POST'))
@login_required
def get_report_data():
    if request.method == 'GET':
        try:
            decision_id = request.args.get('decision_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not decision_id:
            return get_error(RET.PARAMERR, 'Error: request lacks decision_id')

        decision = decisionService.queryDecisionById(decision_id)

        if not decision:
            return get_error(RET.PARAMERR, 'Error: decision_id not exists')

        file_path = decisionService.getReportFilePath(decision)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: prediction file not exists')

        data = decisionService.getReportData(file_path)

        if not data:
            return get_error(RET.DATAERR, 'Error: file lacks data or data format error')

        return {'meta': {'msg': 'get prediction data success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/task/apply/state', methods=('GET', 'POST'))
@login_required
def get_task_apply_state():
    if request.method == 'GET':
        try:
            task_id = request.args.get('task_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not task_id:
            return get_error(RET.PARAMERR, 'Error: request lacks task_id')

        data = decisionService.getTaskApplyState(task_id)

        return {'meta': {'msg': 'get state success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/task/apply/featureEng/state', methods=('GET', 'POST'))
@login_required
def get_task_apply_featureEng_state():
    if request.method == 'GET':
        try:
            task_id = request.args.get('task_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not task_id:
            return get_error(RET.PARAMERR, 'Error: request lacks task_id')

        data = decisionService.getTaskApplyState(task_id, 'featureEng')

        return {'meta': {'msg': 'get state success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/task/apply/learner/state', methods=('GET', 'POST'))
@login_required
def get_task_apply_learner_state():
    if request.method == 'GET':
        try:
            task_id = request.args.get('task_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not task_id:
            return get_error(RET.PARAMERR, 'Error: request lacks task_id')

        data = decisionService.getTaskApplyState(task_id, 'learner')

        return {'meta': {'msg': 'get state success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/task/apply/decision/state', methods=('GET', 'POST'))
@login_required
def get_task_apply_decision_state():
    if request.method == 'GET':
        try:
            task_id = request.args.get('task_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not task_id:
            return get_error(RET.PARAMERR, 'Error: request lacks task_id')

        data = decisionService.getTaskApplyState(task_id, 'decision')

        return {'meta': {'msg': 'get state success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405