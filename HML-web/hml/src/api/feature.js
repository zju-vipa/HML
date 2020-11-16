import request from '../utils/request'

export default {
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
  // 获取数据集列名接口
  getDatasetColumns (id) {
    return request({
      url: `/dataset/columns?dataset_id=${id}`,
      method: 'GET',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
        // 'Content-Type': 'application/json'
      }
    })
  },
  // 获取数据集数据接口
  getData (id) {
    return request({
      url: `/dataset/data?dataset_id=${id}`,
      method: 'GET'
    })
  }
}
