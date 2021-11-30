from flask import Blueprint, request, g, json
from app.constant import get_error, RET
from app._UserApp import login_required
from utils.CommonUtil import download_file
from model import Learner
from service import LearnerService
from service import DatasetService
import os
import pandas as pd
learnerService = LearnerService()
datasetService = DatasetService()

bp = Blueprint('learner', __name__, url_prefix='/api/private/v1/learner')


@bp.route('/query', methods=('GET', 'POST'))
@login_required
def query_learner_list():
    if request.method == 'GET':
        user_id = g.user_id
        learners = learnerService.queryLearnerListByUserId(user_id)
        if learners:
            learners = [learner.serialize for learner in learners]
        else:
            learners = None
        return {'meta': {'msg': 'query learner list success', 'code': 200}, 'data': learners}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete_learner():
    if request.method == 'GET':
        try:
            learner_id = request.args.get('learner_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not learner_id:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_id')

        learner = learnerService.queryLearnerById(learner_id)

        if not learner:
            return get_error(RET.PARAMERR, 'Error: learner_id not exists')

        file_directory = learnerService.getLearnerFileDirectory(learner)

        if not file_directory:
            return get_error(RET.FILEERR, 'Error: learner file directory not exists')

        learnerService.deleteLearner(learner_id, file_directory)

        return {'meta': {'msg': 'delete learner success', 'code': 200}, 'data': None}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_learner():
    # add a learner using the params in request
    """
    request params:
    name: the name of the learner **required**
    """
    if request.method == 'POST':
        try:
            learner_name = request.json.get('learner_name')
            learner_type = request.json.get('learner_type')
            learner_parameters = request.json.get('learner_parameters')
            dataset_id = request.json.get('dataset_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        try:
            user_id = g.user_id
            username = g.user.username
        except Exception:
            return get_error(RET.SESSIONERR, 'Error: no login')

        if not learner_name:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_name')
        if not learner_type:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_type')
        if not learner_parameters:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_parameters')
        if not dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_id')

        dataset = datasetService.queryDatasetById(dataset_id)

        if not dataset:
            return get_error(RET.PARAMERR, 'Error: dataset_id not exists')

        dataset_file_path = datasetService.getDatasetFilePath(dataset)

        if not dataset_file_path:
            return get_error(RET.FILEERR, 'Error: dataset file not exists')

        learner_bean = Learner()
        learner_bean.learner_name = learner_name
        learner_bean.learner_type = learner_type
        learner_bean.learner_parameters = json.dumps(learner_parameters, ensure_ascii=False)
        learner_bean.dataset_id = dataset_id
        learner_bean.user_id = user_id
        learner_bean.username = username

        learner = learnerService.addLearner(learner_bean,
                                            learner_parameters,
                                            dataset_file_path).serialize

        msg = 'add learner success and train immediately'
        code = 204

        return {'meta': {'msg': msg, 'code': code}, 'data': learner}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/download/prediction', methods=('GET', 'POST'))
@login_required
def download_prediction():
    if request.method == 'GET':
        try:
            learner_id = request.args.get('learner_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not learner_id:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_id')

        learner = learnerService.queryLearnerById(learner_id)

        if not learner:
            return get_error(RET.PARAMERR, 'Error: learner_id not exists')

        file_path = learnerService.getPredictionFilePath(learner)

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
            learner_id = request.args.get('learner_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not learner_id:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_id')

        learner = learnerService.queryLearnerById(learner_id)

        if not learner:
            return get_error(RET.PARAMERR, 'Error: learner_id not exists')

        file_path = learnerService.getReportFilePath(learner)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: report file not exists')

        file = download_file(file_path)

        return file, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/data/prediction', methods=('GET', 'POST'))
@login_required
def get_prediction_data():
    if request.method == 'GET':
        try:
            learner_id = request.args.get('learner_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not learner_id:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_id')

        learner = learnerService.queryLearnerById(learner_id)

        if not learner:
            return get_error(RET.PARAMERR, 'Error: learner_id not exists')

        file_path = learnerService.getPredictionFilePath(learner)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: prediction file not exists')

        data = learnerService.getPredictionData(file_path)

        if not data:
            return get_error(RET.DATAERR, 'Error: file lacks data or data format error')

        return {'meta': {'msg': 'get prediction data success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/data/report', methods=('GET', 'POST'))
@login_required
def get_report_data():
    if request.method == 'GET':
        try:
            learner_id = request.args.get('learner_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not learner_id:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_id')

        learner = learnerService.queryLearnerById(learner_id)

        if not learner:
            return get_error(RET.PARAMERR, 'Error: learner_id not exists')

        file_path = learnerService.getReportFilePath(learner)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: prediction file not exists')

        data = learnerService.getReportData(file_path)

        if not data:
            return get_error(RET.DATAERR, 'Error: file lacks data or data format error')

        return {'meta': {'msg': 'get prediction data success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/task/train/state', methods=('GET', 'POST'))
@login_required
def get_task_train_state():
    if request.method == 'GET':
        try:
            task_id = request.args.get('task_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not task_id:
            return get_error(RET.PARAMERR, 'Error: request lacks task_id')

        data = learnerService.getTaskTrainState(task_id)

        return {'meta': {'msg': 'get state success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

# action
@bp.route('/action/query', methods=('GET', 'POST'))
@login_required
def query_action_detail():
    if request.method == 'GET':
        try:
            learner_id = request.args.get('learner_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not learner_id:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_id')

        learner = learnerService.queryLearnerById(learner_id)
        if not learner:
            return get_error(RET.PARAMERR, 'Error: learner_id not exists')
        # p, q, v, theta
        file_path = learnerService.getActionFilePath(learner)
        detail = None
        if os.path.exists(file_path):
            # 先簡單處理一下
            file = pd.read_csv(file_path)
            detail = file.to_json(orient="records")

        return {'meta': {'msg': 'query learner action detail success', 'code': 200},
                'data': {'learner': learner.serialize, 'detail': detail}
                }, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/action/input', methods=('GET', 'POST'))
@login_required
def learner_action_input():
    # human in the loop: deal with the human action input
    """
    request params:
    name: the action(an integer number) of the learner **required**
    """
    if request.method == 'POST':
        try:
            learner_id = request.json.get('learner_id')
            learner_action = request.json.get('learner_action')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        # try:
        #     user_id = g.user_id
        #     username = g.user.username
        # except Exception:
        #     return get_error(RET.SESSIONERR, 'Error: no login')

        if not learner_id:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_id')
        if not learner_action:
            return get_error(RET.PARAMERR, 'Error: request lacks learner_action')

        learner = learnerService.queryLearnerById(learner_id)

        if not learner:
            return get_error(RET.PARAMERR, 'Error: learner_id not exists')
        # write the action into database
        learner.action = learner_action
        learnerService.updateLearner(learner)

        msg = 'input learner action success'
        code = 204

        return {'meta': {'msg': msg, 'code': code}}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405
