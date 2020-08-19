"""
error codes and their messages
"""


class RET:
    OK = "0"
    DBERR = "4001"
    NODATA = "4002"
    DATAEXIST = "4003"
    DATAERR = "4004"
    SESSIONERR = "4101"
    LOGINERR = "4102"
    PARAMERR = "4103"
    USERERR = "4104"
    ROLEERR = "4105"
    PWDERR = "4106"
    EMAILEXIST = "4107"
    UNAMEEXIST = "4108"
    FILEERR = "4109"
    REQERR = "4201"
    IPERR = "4202"
    THIRDERR = "4301"
    IOERR = "4302"
    SERVERERR = "4500"
    UNKOWNERR = "4501"

    error_message = {
        OK: u"成功",
        DBERR: u"数据库查询错误",
        NODATA: u"无数据",
        DATAEXIST: u"数据已存在",
        DATAERR: u"数据错误",
        SESSIONERR: u"用户未登录",
        LOGINERR: u"用户登录失败",
        PARAMERR: u"参数错误",
        USERERR: u"用户不存在或未激活",
        ROLEERR: u"用户身份错误",
        PWDERR: u"密码错误",
        EMAILEXIST: u"邮箱已存在",
        UNAMEEXIST: u"用户名已存在",
        FILEERR: u"无文件",
        REQERR: u"非法请求或请求次数受限",
        IPERR: u"IP受限",
        THIRDERR: u"第三方系统错误",
        IOERR: u"文件读写错误",
        SERVERERR: u"内部错误",
        UNKOWNERR: u"未知错误",
    }


def get_error(code, extra_message=None):
    print('---------------------- extra_message ----------------------')
    print(extra_message, '\n')
    error = {
        "code": int(code),
        "message": RET.error_message[code],
        "extra_message": extra_message
    }, int(code[:3])
    return error
