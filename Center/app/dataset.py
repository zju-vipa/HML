from flask import Blueprint, request, g, jsonify
from app.constant import get_error, RET
from app.auth import login_required
from model import Dataset
from app import datasetService, dataturksUserService, dataturksProjectService
import json

bp = Blueprint('dataset', __name__, url_prefix='/dataset')


@bp.route('/list', methods=('GET', 'POST'))
@login_required
def get_list():
    userid = g.userid
    datasets = datasetService.getDatasetListByUserid(g.userid)
    return jsonify(datasets)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def add_dataset():
    # add a dataset using the params in request
    """
    request params:
    name: the name of the dataset **required**
    """
    if request.method == 'POST':
        userid = g.userid
        dataset_name = request.form.get('dataset_name')
        dataset_type = request.form.get('dataset_type')
        task_type = request.form.get('task_type')
        tags = request.form.get('tags')

        rules = json.dumps({
            "tags": tags,
            "instructions": "this project is created by AIX Center"
        })

        if dataset_name is None or dataset_name is None:
            return get_error(RET.PARAMERR)
        if dataset_type == "UNLABELED" and (task_type is None or tags is None):
            return get_error(RET.PARAMERR)

        dataset = Dataset()
        if dataset_type == "UNLABELED":
            # create a project in dataturks
            # 1. get the id and token by login dataturks
            auth_dict = dataturksUserService.loginByUserId(userid)
            if auth_dict is None:
                return get_error(RET.UNKOWNERR)
            uid = auth_dict.get('id')
            token = auth_dict.get('token')

            # 2. create a project in dataturks
            project_id = dataturksProjectService.createProject(uid, token, dataset_name, task_type, rules)
            dataset.dataturks_id = project_id

        dataset.name = dataset_name
        dataset.created_by = userid
        datasetService.addDataset(dataset)
        return {"msg": "add dataset success"}
    return {"msg": "method not allowed"}, 404


@bp.route('/<string:dataset_id>', methods=('GET',))
@login_required
def get_detail(dataset_id):
    #todo: add user access validation
    if dataset_id is None:
        return get_error(RET.PARAMERR)
    userid = g.userid
    dataset = datasetService.getDatasetById(dataset_id)
    dataturks_id = dataset.get('dataturks_id')
    if dataturks_id is not None:
        auth_dict = dataturksUserService.loginByUserId(userid)
        if auth_dict is None:
            return get_error(RET.UNKOWNERR)
        uid = auth_dict.get('id')
        token = auth_dict.get('token')
        dataset_datail = dataturksProjectService.getProjectDetails(uid,token, dataturks_id)
        dataset.update(dataset_datail)
    return jsonify(dataset)
