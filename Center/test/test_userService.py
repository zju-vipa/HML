from app import userService
from model import User

def test_register():
    user = User()
    user.username = 'sontal'
    user.email = '418773551@qq.com'
    user.password = 'qqqqq'
    userService.addUser(user)

def test_error():
    from app.constant import RET, get_error

    x = get_error(RET.IOERR)

    code = RET.IOERR
    print(int(code[:3]))
    print(x)