import request from '../utils/request'

export default {
  // 查询决策
  query () {
    return request({
      url: '/decision/query',
      method: 'GET'
    })
  },
  // 删除数据集
  deleteData (id) {
    return request({
      url: `/decision/delete?decision_id=${id}`,
      method: 'GET'
    })
  },
  // 下载决策特征工程的
  downloadHumanFea (id) {
    return request({
      url: `/decision/download/transform?decision_id=${id}`,
      method: 'GET',
      responseType: 'blob'
    })
  },
  // 下载预测结果
  downloadPredicition (id) {
    return request({
      url: `/decision/download/prediction?decision_id=${id}`,
      method: 'GET',
      responseType: 'blob'
    })
  },
  // 下载数据集
  downloadReport (id) {
    return request({
      url: `/decision/download/report?decision_id=${id}`,
      method: 'GET',
      responseType: 'blob'
    })
  },
  // 查看任务分析进度条
  searchHFProgress (id) {
    return request({
      url: `/decision/task/apply/featureEng/state?task_id=${id}`,
      method: 'GET'
    })
  },
  searchLeaProgress (id) {
    return request({
      url: `/decision/task/apply/learner/state?task_id=${id}`,
      method: 'GET'
    })
  },
  searchAllProgress (id) {
    return request({
      url: `/decision/task/apply/decision/state?task_id=${id}`,
      method: 'GET'
    })
  }
}
