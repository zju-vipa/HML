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
  // 删除数据集
  deleteData (id) {
    return request({
      url: `/featureEng/delete?featureEng_id=${id}`,
      method: 'GET'
    })
  },
  // 查询特征工程
  query () {
    return request({
      url: '/featureEng/query',
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
      url: `/featureEng/task/operate/state?task_id=${id}`,
      method: 'GET'
    })
  }
}
