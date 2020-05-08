"""
used to auth user
"""
import functools
from flask import Blueprint, current_app, request, g
from app.constant import RET, get_error
import requests
import json
from app.encrypt import create_token, verify_token, sha256, verify_machine_token
from app import userService, deviceService
from model import User
from app import dataturksUserService
import config

# a blue print of auth functions, urls defined will start with /auth like '/auth/login'
# prefix of url in this py
bp = Blueprint('auth', __name__, url_prefix='/user')


def login_required(view):
    """
    a wrapper of login required pages or apis
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        token = request.headers.get('auth')  # get token from auth
        if token is None:
            return get_error(RET.SESSIONERR)
        userid = verify_token(token)  # reverse, get userid by token
        user = userService.queryUserById(userid)
        if userid is None or user is None:
            return get_error(RET.SESSIONERR)
        else:
            g.userid = userid
            g.user = user
            print("auth success,userid is:", userid)
        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # register a user
    if request.method == 'POST':
        try:
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
        except Exception:
            return get_error(RET.PARAMERR)
        if not email or userService.queryUserByEmail(email) is not None:
            return get_error(RET.PARAMERR)
        elif not username or userService.queryUserByEmail(email) is not None:
            return get_error(RET.PARAMERR)
        elif not password:
            return get_error(RET.PARAMERR)
        else:
            dataturksUserService.register(email, password, username=username)
            user = User()
            user.username = username
            user.email = email
            user.password = password
            userService.addUser(user)
            return {"msg": "register success"}
    return {"msg": "method not allowed"}, 404


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    : only for POST method to login
    : login success: return {"msg": "login success","token": "...some token..."}
    : login failed: return error msg likes {"code": "4103","msg": "参数错误"}
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email:
            return get_error(RET.PARAMERR)
        if not password:
            return get_error(RET.PARAMERR)
        user_bean = User()
        user_bean.email = email
        user_bean.password = password
        user = userService.loginByPassword(user_bean)
        if not user:
            return get_error(RET.USERERR)
        elif not user['password'] == sha256(password):
            return get_error(RET.PWDERR)
        else:
            token = create_token(user['id'])  # query user, then create token
            return {'msg': 'login success', 'token': token}
    return {"msg": "method not allowed"}, 404


@bp.route('/dataturks', methods=('GET', 'POST'))
@login_required
def login_dataturks():
    # login to the dataturks, get the uid and token
    # used to auto-login
    user = g.user
    logininfo = dataturksUserService.login(user.email, user.password)
    # link of dataturks project
    return config.DATATURKS_INDEX + '/autologin.html?id={}&token={}'.format(logininfo['id'], logininfo['token'])


@bp.route('/test_login', methods=('GET', 'POST'))
@login_required
def test_login():
    # just for testing the login required function
    return 'ok'


# for device
def device_required(view):
    """
    a wrapper of device only pages or apis
    set device id here! can judge whether can get a task by gpu memory
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        token = request.headers.get('auth')
        # print("token is:",token)
        if token is None:
            return get_error(RET.SESSIONERR)
        device_id = verify_machine_token(token)
        # print("device id:",device_id)
        # device = get_device(device_id)
        device = deviceService.getDeviceById(device_id)
        if device_id is None or device is None:
            return get_error(RET.SESSIONERR)
        else:
            g.device_id = device_id
            g.device = device
            print("auth success,device_id is:", device_id)
        return view(**kwargs)

    return wrapped_view
