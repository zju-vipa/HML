from flask import Blueprint, request, g, jsonify
from app import modelService
from app.auth import login_required

bp = Blueprint('model', __name__, url_prefix='/model')


@bp.route('/list', methods=('GET', 'POST'))
@login_required
def get_list():
    model_list = modelService.getAvaliableModelList(g.userid)
    return jsonify(model_list)  # pass to frontend
