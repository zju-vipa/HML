import request from '../utils/request'

export default {
  // 注册
  register (formName) {
    return request({
      url: '/user/register',
      method: 'post',
      data: {
        email: formName.email,
        username: formName.username,
        password: formName.password
        // formName
      },
      transformRequest: [
        function (data) {
          let ret = ''
          for (const it in data) {
            ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
          }
          return ret
        }]
    })
  },
  // 登录
  login (formName) {
    return request({
      url: '/user/login',
      method: 'post',
      data: {
        email: formName.email,
        password: formName.password
      },
      transformRequest: [
        function (data) {
          let ret = ''
          for (const it in data) {
            ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
          }
          return ret
        }]
    })
  },
  // 退出系统
  logout (token) {
  }
}
