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
  queryAlgorithmByType (type) {
    return request({
      url: `/algorithm/queryByType?algorithm_type=${type}`,
      method: 'GET'
    })
  },
  queryAlgorithmParas (name) {
    return request({
      url: `/algorithm/queryParameters?algorithm_name=${name}`,
      method: 'GET'
    })
  },
  // 提交创建特征工程表单
  submitFeatureEngForm (form) {
    return request({
      url: '/featureEng/task/addFeatureEngTask',
      method: 'POST',
      data: {
        featureEng_name: form.featureEng_name,
        featureEng_type: form.featureEng_type,
        featureEng_operationMode: form.run_mode,
        featureEng_modules: form.checkedModules,
        featureEng_processes: form.featureEng_processes,
        original_dataset_id: form.original_dataset_id,
        new_dataset_name: form.new_dataset_name,
        retrain: form.retrain,
        imported_featureEng: form.importedFeatureEng
      },
      headers: {
        // 'content-type': 'application/x-www-form-urlencoded'
        'Content-Type': 'application/json'
      }
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
  },
  queryTaskProgress (id) {
    return request({
      url: `/featureEng/task/queryTaskStatus?task_id=${id}`,
      method: 'GET'
    })
  }
}
