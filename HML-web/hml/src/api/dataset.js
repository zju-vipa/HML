import request from '../utils/request'

export default {
  // 添加数据集
  addDataset (form) {
    return request({
      url: '/dataset/add',
      method: 'post',
      data: {
        dataset_id: form.dataset_id,
        dataset_name: form.dataset_name,
        tmp_file_path: form.tmp_file_path,
        introduction: form.introduction,
        if_profile: form.if_profile,
        if_public: form.if_public
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
  // 查询数据集
  query () {
    return request({
      url: '/dataset/query',
      method: 'GET',
      headers: {
        Authorization: JSON.parse(localStorage.getItem('token'))
      }
    })
  },
  // 查询人工特征处理后的数据集
  queryHuFea (Hufea) {
    return request({
      url: `/dataset/query?if_featureEng=${Hufea}`,
      method: 'GET'
    })
  },
  // 下载数据集
  downloadFile (id) {
    return request({
      url: `/dataset/download/file?dataset_id=${id}`,
      method: 'GET'
      // responseType: 'blob'
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
  },
  // 删除数据集
  deleteData (id) {
    return request({
      url: `/dataset/delete?dataset_id=${id}`,
      method: 'GET'
    })
  }
}
