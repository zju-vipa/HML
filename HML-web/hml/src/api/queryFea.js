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
  // 停止特征工程
  stopTask (id) {
    return request({
      url: `/featureEng/stopTask?featureEng_id=${id}`,
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
  queryAllFeatureEng () {
    return request({
      url: '/featureEng/queryAllFeatureEng',
      method: 'GET'
    })
  },
  queryImportFeatureEng () {
    return request({
      url: '/featureEng/queryImportFeatureEng',
      method: 'GET'
    })
  },
  // 查询特征库
  queryFeatureLibrary () {
    return request({
      url: '/featureEng/task/queryFeatureLibrary',
      method: 'GET'
    })
  },
  // 查询任务概况+初始结果
  queryLatestResults () {
    return request({
      url: '/featureEng/task/queryLatestResult',
      method: 'GET'
    })
  },
  querySelectedTaskResults (id) {
    return request({
      url: `/featureEng/result/querySelectedTaskResults?featureEng_id=${id}`,
      method: 'GET'
    })
  },
  // 查询最新任务特征
  queryLatestFeatures () {
    return request({
      url: '/featureEng/task/queryLatestFeature',
      method: 'GET'
    })
  },
  querySelectedTaskFeatures (id) {
    return request({
      url: `/featureEng/result/querySelectedTaskFeatures?featureEng_id=${id}`,
      method: 'GET'
    })
  },
  // 查询最新交互记录
  queryLatestRecord () {
    return request({
      url: '/featureEng/task/queryLatestRecord',
      method: 'GET'
    })
  },
  querySelectedTaskRecord (id) {
    return request({
      url: `/featureEng/result/querySelectedTaskRecord?featureEng_id=${id}`,
      method: 'GET'
    })
  },
  // 查询前100特征
  queryFeatureScore () {
    return request({
      url: '/featureEng/task/queryLatestImportance',
      method: 'GET'
    })
  },
  querySelectedTaskScore (id) {
    return request({
      url: `/featureEng/result/querySelectedImportance?featureEng_id=${id}`,
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
  },
  importFeatureEng (id) {
    return request({
      url: `/featureEng/importFeatureEng?featureEng_id=${id}`,
      method: 'GET'
    })
  },
  // 下载数据集
  download (id) {
    return request({
      url: `/featureEng/download?dataset_id=${id}`,
      method: 'GET',
      responseType: 'blob'
      // data: {
      //   dataset_id: id
      // }
    })
  },
  // 获取数据集类型
  queryDatasetType (id) {
    return request({
      url: `/featureEng/queryDatasetType?dataset_id=${id}`,
      method: 'GET'
    })
  }
}
