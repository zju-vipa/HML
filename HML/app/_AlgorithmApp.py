from flask import Blueprint, request, json, current_app
from app.constant import get_error, RET
from app._UserApp import login_required
from model import Algorithm
from service import AlgorithmService
algorithmService = AlgorithmService()

bp = Blueprint('algorithm', __name__, url_prefix='/api/private/v1/algorithm')


@bp.route('/query', methods=('GET', 'POST'))
@login_required
def query_algorithm_list():
    if request.method == 'GET':
        try:
            algorithm_category = request.args.get('algorithm_category')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not algorithm_category:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_category')

        algorithms = algorithmService.queryAlgorithmListByCategory(algorithm_category)
        if algorithms:
            algorithms = [algorithm.serialize for algorithm in algorithms]
        else:
            algorithms = None
        return {'meta': {'msg': 'query algorithm list success', 'code': 200}, 'data': algorithms}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_algorithm():
    """
    add a algorithm using the params in request
    :return:
    """
    if request.method == 'POST':
        try:

            algorithm_name = request.json.get('algorithm_name')
            algorithm_type = request.json.get('algorithm_type')
            algorithm_category = request.json.get('algorithm_category')
            algorithm_parameters = request.json.get('algorithm_parameters')
            introduction = request.json.get('introduction')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not algorithm_name:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_name')
        if not algorithm_type:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_type')
        if not algorithm_category:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_category')
        if not algorithm_parameters:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_parameters')

        algorithm_bean = Algorithm()
        algorithm_bean.algorithm_name = algorithm_name
        algorithm_bean.algorithm_type = algorithm_type
        algorithm_bean.algorithm_category = algorithm_category
        algorithm_bean.algorithm_parameters = json.dumps(algorithm_parameters, ensure_ascii=False)
        algorithm_bean.introduction = introduction

        algorithm = algorithmService.addAlgorithm(algorithm_bean).serialize

        return {'meta': {'msg': 'add algorithm success', 'code': 200}, 'data': algorithm}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

@bp.route('/queryByType', methods=('GET', 'POST'))
@login_required
def query_algorithm_list_byType():
    if request.method == 'GET':
        try:
            algorithm_type = request.args.get('algorithm_type')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not algorithm_type:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_type')
        algorithms = algorithmService.queryAlgorithmListByType(algorithm_type)
        if algorithms:
            algorithms = [algorithm.serialize for algorithm in algorithms]
        else:
            algorithms = None
        return {'meta': {'msg': 'query algorithm list success', 'code': 200}, 'data': algorithms}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

@bp.route('/queryParameters', methods=('GET', 'POST'))
@login_required
def query_algorithm_parameters():
    if request.method == 'GET':
        try:
            algorithm_name = request.args.get('algorithm_name')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not algorithm_name:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_type')
        algorithm = algorithmService.queryAlgorithmParams(algorithm_name)
        return {'meta': {'msg': 'query algorithm list success', 'code': 200}, 'data': algorithm.serialize}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405