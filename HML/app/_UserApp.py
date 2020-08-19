"""
used to auth user
"""
import functools
from flask import Blueprint, request, g, current_app
from app.constant import RET, get_error
from utils.EncryptUtil import create_token, verify_token
from model import User
from service import UserService
userService = UserService()

# a blue print of user functions, urls defined will start with /user like '/user/register'
# prefix of url in this py
bp = Blueprint('user', __name__, url_prefix='/api/private/v1/user')


def login_required(view):
    """
    a wrapper of login required pages or apis
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        log_content = '\n\n' + '---------------------- request.headers ----------------------'
        log_content += '\n' + str(request.headers).strip()
        if request.method == 'POST':
            log_content += '\n\n' + '------------ request.method: POST (request.form) ------------'
            log_content += '\n' + str(request.form)
            log_content += '\n\n' + '------------ request.method: POST (request.json) ------------'
            log_content += '\n' + str(request.json)
        elif request.method == 'GET':
            log_content += '\n\n' + '------------- request.method: GET (request.args) -------------'
            log_content += '\n' + str(request.args)

        token = request.headers.get('Authorization')  # get token from auth
        if token is None:
            return get_error(RET.SESSIONERR, 'Error: header lacks token')
        user_id = verify_token(token)  # reverse, get userid by token
        user = userService.queryUserById(user_id)
        if user_id is None or user is None:
            return get_error(RET.SESSIONERR, 'Error: token wrong')

        g.user_id = user_id
        g.user = user
        log_content += '\n\n' + '------------------------ auth success ------------------------'
        log_content += '\n' + 'user_id is:' + str(user_id) + '\n\n'
        current_app.logger.info(log_content)
        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    : only for POST method to login
    : login success: return {"msg": "login success","token": "...some token..."}
    : login failed: return error msg likes {"code": "4103","msg": "参数错误"}
    """
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not email:
            return get_error(RET.PARAMERR, 'Error: request lacks email')
        if not password:
            return get_error(RET.PARAMERR, 'Error: request lacks password')

        user_bean = User()
        user_bean.email = email
        user_bean.password = password
        user = userService.loginByPassword(user_bean)

        if not user:
            return get_error(RET.LOGINERR, 'Error: email or password wrong')

        user = user.serialize
        user.pop('password')
        token = create_token(user['user_id'])  # query user, then create token
        user['token'] = token
        return {'meta': {'msg': 'login success', 'code': 200}, 'data': user}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    register a user
    """

    if request.method == 'POST':
        try:
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not email:
            return get_error(RET.PARAMERR, 'Error: request lacks email')
        if not username:
            return get_error(RET.PARAMERR, 'Error: request lacks username')
        if not password:
            return get_error(RET.PARAMERR, 'Error: request lacks password')
        if userService.queryUserByEmail(email):
            return get_error(RET.EMAILEXIST, 'Error: email exists')

        user_bean = User()
        user_bean.username = username
        user_bean.email = email
        user_bean.password = password
        user = userService.addUser(user_bean).serialize
        user.pop('password')
        return {'meta': {'msg': 'register success', 'code': 200}, 'data': user}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

