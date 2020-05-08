from enum import Enum


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
    REQERR = "4201"
    IPERR = "4202"
    THIRDERR = "4301"
    IOERR = "4302"
    SERVERERR = "4500"
    UNKOWNERR = "4501"

error_map = {
    RET.OK: u"成功",
    RET.DBERR: u"数据库查询错误",
    RET.NODATA: u"无数据",
    RET.DATAEXIST: u"数据已存在",
    RET.DATAERR: u"数据错误",
    RET.SESSIONERR: u"用户未登录",
    RET.LOGINERR: u"用户登录失败",
    RET.PARAMERR: u"参数错误",
    RET.USERERR: u"用户不存在或未激活",
    RET.ROLEERR: u"用户身份错误",
    RET.PWDERR: u"密码错误",
    RET.EMAILEXIST: u"邮箱已存在",
    RET.UNAMEEXIST: u"用户名已存在",
    RET.REQERR: u"非法请求或请求次数受限",
    RET.IPERR: u"IP受限",
    RET.THIRDERR: u"第三方系统错误",
    RET.IOERR: u"文件读写错误",
    RET.SERVERERR: u"内部错误",
    RET.UNKOWNERR: u"未知错误",
}


def get_error(code):
    return {"code": code, "msg": error_map[code]}, int(code[:3])


class TaskType(Enum):
    TEXT_CLASSIFICATION = 0
    TEXT_SUMMARIZATION = 1
    POS_TAGGING = 2
    POS_TAGGING_GENERIC = 3
    TEXT_MODERATION = 4
    DOCUMENT_ANNOTATION = 5
    IMAGE_CLASSIFICATION = 6
    IMAGE_BOUNDING_BOX = 7
    IMAGE_POLYGON_BOUNDING_BOX = 8
    IMAGE_POLYGON_BOUNDING_BOX_V2 = 9
    VIDEO_CLASSIFICATION = 10
    VIDEO_BOUNDING_BOX = 11
