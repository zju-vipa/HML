from flask import Blueprint, request, g, jsonify
from app.constant import get_error, RET
from app.auth import login_required
import os
from app import taskService, trainService
import json

bp = Blueprint('task', __name__, url_prefix='/task')
task_types = ['classification', 'detection', 'segmentation']

"""
apis used for user
"""


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def add():
    # add a task using the params in request
    """
    request params:
    :name the name of the task **required**
    :type the type of the task **required**
    :datasetId the id of dataset **required**
    """
    if request.method == 'POST':
        userid = g.userid
        name = request.form.get('name')
        type = request.form.get('type')
        dataset_id = request.form.get('datasetId')
        is_public = request.form.get('public')

        print("public:", is_public)

        if name is None or type is None or dataset_id is None:
            return get_error(RET.PARAMERR)
        if type not in task_types:
            print("task wrong")
            return get_error(RET.PARAMERR)
        taskService.addTask(userid,name,dataset_id,type,is_public)
        return {"msg": "add task success"}

    return {"msg": "method not allowed"}, 404

# get the task use the taskid
@bp.route('/<string:task_id>', methods=('GET',))
@login_required
def get_task(task_id):
    # used for the frontend to show the job list of a given userid
    userid = g.userid
    task = taskService.getTaskById(userid, task_id)
    return jsonify(task)

@bp.route('/private_list', methods=('GET', 'POST'))
@login_required
def get_task_list():
    # used for the frontend to show the job list of a given userid
    userid = g.userid
    tasks = taskService.getMyTaskList(userid)
    return jsonify(tasks)

@bp.route('/support_list', methods=('GET', 'POST'))
@login_required
def get_support_task_list():
    # used for the frontend to show the public job list
    userid = g.userid
    tasks = taskService.getMySupportTaskList(userid)
    return jsonify(tasks)

@bp.route('/public_list', methods=('GET', 'POST'))
@login_required
def get_public_task_list():
    # used for the frontend to show the public job list
    tasks = taskService.getPublicTaskList()
    return jsonify(tasks)

@bp.route('/<string:task_id>', methods=('POST','GET'))
@login_required
def accept_train(task_id):
    userid = g.userid
    detail = trainService.getDetailByTaskId(userid,task_id)
    if detail is not None:
        detail = json.loads(detail)
    return jsonify(detail)



#
# """
# restful APIs for config file
# """

# @bp.route('/config', methods=('PUT',))
# @login_required
# def update_config():
#     # same as post, not used now
#     pass


# @bp.route('/config', methods=('GET',))
# @login_required
# def get_config():
#     """
#     params: taskid
#     return the config file if exists
#     else return 404
#     """
#
#     taskId = request.args.get('taskId')
#     if taskId is None:
#         return {"msg": "task id must be specified"}, 404
#     config_file_path = get_config_file_path(taskId)
#     if not os.path.exists(config_file_path):
#         return {"msg": "no config file of this task"}, 404
#     with open(config_file_path, "r", encoding="utf-8") as f:
#         content = f.read()
#     return jsonify({"content": content})


# @bp.route('/config', methods=('POST',))
# @login_required
# def upload_config():
#     """
#     params: taskid,configfile
#     delete the old config file if it exists
#     save the new config file
#     """
#     taskId = request.form.get('taskId')
#     file = request.files.get('file')
#     if not taskId:
#         return {"msg": "task id must be specified"}, 404
#     if not file:
#         return {"msg": "file must be uploaded"}, 404
#     config_file_path = get_config_file_path(taskId)
#     if os.path.exists(config_file_path):
#         os.remove(config_file_path)
#     save_config_file(file, taskId)
#     db_upload_config(taskId)
#     return "ok"

# @bp.route('/choose_model', methods=('POST',))
# @login_required
# def choose_model():
#     # used for the frontend to show the job list of a given userid
#     userid = g.userid
#     task_id = request.form.get('task_id')
#     model_id = request.form.get('model_id')
#     if task_id is None or model_id is None:
#         return {"msg": "param wrong"}, 404
#     # todo: choose a model for the task, the task will be ok for train
#     tasks = taskService.getMyTaskList(userid)
#     return jsonify(tasks)



# """
# apis used for machine
# """
#
# # some functions
#
# def get_config_file_path(taskid):
#     save_path = os.path.join(os.getcwd(), 'uploads', "{}.yml".format(taskid))
#     return save_path
#
#
# def save_config_file(file, taskid):
#     print(file.filename)
#     print(os.getcwd())
#     save_path = get_config_file_path(taskid)
#     print(save_path)
#     file.save(save_path)
