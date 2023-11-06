from flask import Blueprint, request, g
from app.constant import get_error, RET
from app._UserApp import login_required
from utils.CommonUtil import download_file
from model import Dataset
from service import DatasetService
import os
import shutil
from pathlib import Path
datasetService = DatasetService()

bp = Blueprint('dataset', __name__, url_prefix='/api/private/v1/dataset')


@bp.route('/query', methods=('GET', 'POST'))
@login_required
def query_dataset_list():
    if request.method == 'GET':
        user_id = g.user_id

        if_featureEng = request.args.get('if_featureEng')
        if if_featureEng is not None:
            if_featureEng = (str(request.args.get('if_featureEng')) == "true")

        datasets = datasetService.queryDatasetListByUserId(user_id, if_featureEng)

        if datasets:
            datasets = [dataset.serialize for dataset in datasets]
        else:
            datasets = None
        return {'meta': {'msg': 'query dataset list success', 'code': 200}, 'data': datasets}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete_dataset():
    if request.method == 'GET':
        try:
            dataset_id = request.args.get('dataset_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_id')

        dataset = datasetService.queryDatasetById(dataset_id)

        if not dataset:
            return get_error(RET.PARAMERR, 'Error: dataset_id not exists')

        file_path = datasetService.getDatasetFilePath(dataset)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: dataset file not exists')

        profile_path = None
        if dataset.profile_state == '1':
            return get_error(RET.FILEERR, 'Error: profile is being generated')
        elif dataset.profile_state == '2':
            profile_path = datasetService.getDatasetProfilePath(dataset)
            if not profile_path:
                return get_error(RET.FILEERR, 'Error: profile not exists')

        datasetService.deleteDataset(dataset_id, file_path, profile_path)

        return {'meta': {'msg': 'delete dataset success', 'code': 200}, 'data': None}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload_dataset():
    if request.method == 'POST':
        try:
            file = request.files.get('file')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not file:
            return get_error(RET.PARAMERR, 'Error: request lacks file')

        data = datasetService.uploadDataset(file)

        if not data:
            return get_error(RET.DATAERR, 'Error: file lacks data or data format error')

        return {'meta': {'msg': 'upload dataset success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405



@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_dataset():
    # add a dataset using the params in request
    """
    request params:
    name: the name of the dataset **required**
    """
    if request.method == 'POST':
        try:
            dataset_id = request.form.get('dataset_id')
            dataset_name = request.form.get('dataset_name')
            if_profile = request.form.get('if_profile')
            if_public = request.form.get('if_public')
            introduction = request.form.get('introduction')
            if_featureEng = request.form.get('if_featureEng')
            featureEng_id = request.form.get('featureEng_id')
            original_dataset_id = request.form.get('original_dataset_id')
            tmp_file_path = request.form.get('tmp_file_path')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        try:
            user_id = g.user_id
            username = g.user.username
        except Exception:
            return get_error(RET.SESSIONERR, 'Error: no login')

        if not dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_id')
        if not dataset_name:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_name')
        if not tmp_file_path:
            return get_error(RET.PARAMERR, 'Error: request lacks tmp_file_path')
        if not os.path.exists(tmp_file_path):
            return get_error(RET.FILEERR, 'Error: file not exists')

        file_name = os.path.split(tmp_file_path)[-1]
        file_id = os.path.splitext(file_name)[0]
        file_type = os.path.splitext(file_name)[-1][1:]

        if file_id != dataset_id:
            return get_error(RET.PARAMERR, 'Error: dataset_id or tmp_file_path wrong')

        dataset_bean = Dataset()
        dataset_bean.dataset_id = dataset_id
        dataset_bean.dataset_name = dataset_name
        dataset_bean.file_type = file_type
        dataset_bean.if_profile = (str(if_profile) == "true")
        dataset_bean.if_public = (str(if_public) == "true")
        dataset_bean.introduction = introduction
        dataset_bean.if_featureEng = (str(if_featureEng) == "true")
        dataset_bean.featureEng_id = featureEng_id
        dataset_bean.original_dataset_id = original_dataset_id
        dataset_bean.user_id = user_id
        dataset_bean.username = username

        dataset = datasetService.addDataset(dataset_bean, tmp_file_path).serialize

        msg = 'add dataset success'

        if dataset['task_id']:
            msg = 'add dataset success and generate profile immediately'

        return {'meta': {'msg': msg, 'code': 200}, 'data': dataset}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/download/file', methods=('GET', 'POST'))
@login_required
def download_dataset():
    if request.method == 'GET':
        try:
            dataset_id = request.args.get('dataset_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_id')

        dataset = datasetService.queryDatasetById(dataset_id)

        if not dataset:
            return get_error(RET.PARAMERR, 'Error: dataset_id not exists')

        file_path = datasetService.getDatasetFilePath(dataset)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: dataset file not exists')

        file = download_file(file_path)

        return file, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/download/profile', methods=('GET', 'POST'))
@login_required
def download_profile():
    if request.method == 'GET':
        try:
            dataset_id = request.args.get('dataset_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_id')

        dataset = datasetService.queryDatasetById(dataset_id)

        if not dataset:
            return get_error(RET.PARAMERR, 'Error: dataset_id not exists')

        if dataset.profile_state == '0':
            return get_error(RET.FILEERR, 'Error: profile not generate')
        elif dataset.profile_state == '1':
            return get_error(RET.FILEERR, 'Error: profile is being generated')
        elif dataset.profile_state == '3':
            return get_error(RET.FILEERR, 'Error: profile generate failure')

        profile_path = datasetService.getDatasetProfilePath(dataset)

        if not profile_path:
            return get_error(RET.FILEERR, 'Error: profile not exists')

        profile = download_file(profile_path)

        return profile, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/data', methods=('GET', 'POST'))
@login_required
def get_dataset_data():
    if request.method == 'GET':
        try:
            dataset_id = request.args.get('dataset_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_id')

        dataset = datasetService.queryDatasetById(dataset_id)

        if not dataset:
            return get_error(RET.PARAMERR, 'Error: dataset_id not exists')

        file_path = datasetService.getDatasetFilePath(dataset)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: dataset file not exists')

        data = datasetService.getDatasetData(file_path)

        if not data:
            return get_error(RET.DATAERR, 'Error: file lacks data or data format error')

        return {'meta': {'msg': 'get dataset data success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/columns', methods=('GET', 'POST'))
@login_required
def get_dataset_columns():
    if request.method == 'GET':
        try:
            dataset_id = request.args.get('dataset_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not dataset_id:
            return get_error(RET.PARAMERR, 'Error: request lacks dataset_id')

        dataset = datasetService.queryDatasetById(dataset_id)

        if not dataset:
            return get_error(RET.PARAMERR, 'Error: dataset_id not exists')

        file_path = datasetService.getDatasetFilePath(dataset)

        if not file_path:
            return get_error(RET.FILEERR, 'Error: dataset file not exists')

        data = datasetService.getDatasetColumns(file_path)

        if not data:
            return get_error(RET.DATAERR, 'Error: file lacks data or data format error')

        return {'meta': {'msg': 'get dataset columns success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/task/analyze/profile/state', methods=('GET', 'POST'))
@login_required
def get_task_analyze_profile_state():
    if request.method == 'GET':
        try:
            task_id = request.args.get('task_id')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not task_id:
            return get_error(RET.PARAMERR, 'Error: request lacks task_id')

        data = datasetService.getTaskAnalyzeProfileState(task_id)

        return {'meta': {'msg': 'get state success', 'code': 200}, 'data': data}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405





# 断面算法
@bp.route('/uploadCrossSectionTrainingSet', methods=('POST',))
@login_required
def upload_cross_section_training_set():
    return upload_cross_section_file()

# 断面算法
@bp.route('/uploadCrossSectionTestSet', methods=('POST',))
@login_required
def upload_cross_section_test_set():
    return upload_cross_section_file()


# 断面算法
def upload_cross_section_file():
    file = request.files.get('file')
    folder_name = request.form.get('folderName', '').strip()

    if not file:
        return get_error(RET.PARAMERR, 'Error: request lacks file')

    filename = file.filename

    base_path = "/root/HML/Decision/MAM_Factor-main/data"
    save_path = base_path if not folder_name else os.path.join(base_path, folder_name)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = os.path.join(save_path, filename)
    file.save(file_path)

    return {'meta': {'msg': 'upload success', 'code': 200}, 'data': None}, 200

