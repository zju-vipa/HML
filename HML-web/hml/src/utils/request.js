import axios from 'axios'
// 2,创建一个axios实例对象
const request = axios.create({
  baseURL: 'http://10.214.211.135:8021/api/private/v1',
  timeout: 1000000
})
// 请求拦截
request.interceptors.request.use(config => {
  // 这里一定要转成json，要不然就有双引号，token就出错了
  config.headers.Authorization = JSON.parse(localStorage.getItem('token'))
  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截
request.interceptors.response.use(config => {
  return config
}, error => {
  return Promise.reject(error)
})
// 3,导出这个封装好的实例
export default request
