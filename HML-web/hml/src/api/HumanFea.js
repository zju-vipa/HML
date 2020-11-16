import request from '../utils/request'

export default {
  // 添加数据集
  add (form) {
    return request({
      url: '/featureEng/add',
      method: 'POST',
      // 'Content-Type': 'application/json',
      data: {
        featureEng_name: form.featureEng_name,
        featureEng_type: form.featureEng_type,
        featureEng_processes: form.featureEng_processes,
        original_dataset_id: form.original_dataset_id,
        new_dataset_name: form.new_dataset_name
      },
      headers: {
        // 'content-type': 'application/x-www-form-urlencoded'
        'Content-Type': 'application/json'
      }
      // transformRequest: [
      //   function (data) {
      //     let ret = ''
      //     for (const it in data) {
      //       ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
      //     }
      //     return ret
      //   }]
    })
  },
  // 查询数据集
  query () {
    return request({
      url: '/dataset/query',
      method: 'GET'
    })
  },
  // 下载数据集
  downloadFile (id) {
    return request({
      url: `/dataset/download/file?dataset_id=${id}`,
      method: 'GET',
      responseType: 'blob'
      // data: {
      //   dataset_id: id
      // }
    })
  },
  // 下载数据集
  downloadProfile (id) {
    return request({
      url: `/dataset/download/profile?dataset_id=${id}`,
      method: 'GET',
      responseType: 'blob'
      // data: {
      //   dataset_id: id
      // }
    })
  },
  // 查看任务分析进度条
  searchProgress (id) {
    return request({
      url: `/dataset/task/analyze/profile/state?task_id=${id}`,
      method: 'GET'
    })
  }
}