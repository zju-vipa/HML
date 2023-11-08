import request from '../utils/request'

export default {
  // 添加
  add (form) {
    return request({
      url: '/learner/add',
      method: 'POST',
      data: {
        learner_name: form.learner_name,
        learner_type: form.learner_type,
        learner_parameters: form.learner_parameters,
        dataset_id: form.dataset_id
      },
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 删除
  deleteData (id) {
    return request({
      url: `/learner/delete?learner_id=${id}`,
      method: 'GET'
    })
  },
  // 查询学习器
  query () {
    return request({
      url: '/learner/query',
      method: 'GET'
    })
  },
  // 查询算法接口
  getMethods (methodCate) {
    return request({
      url: `/algorithm/query?algorithm_category=${methodCate}`,
      method: 'GET'
    })
  },
  // 下载预测
  downloadPrediction (id) {
    return request({
      url: `/learner/download/prediction?learner_id=${id}`,
      method: 'GET',
      responseType: 'blob'
    })
  },
  // 下载报告
  downloadReport (id) {
    return request({
      url: `/learner/download/report?learner_id=${id}`,
      method: 'GET',
      responseType: 'blob'
    })
  },
  // 查看任务分析进度条
  searchProgress (id) {
    return request({
      url: `/learner/task/train/state?task_id=${id}`,
      method: 'GET'
    })
  },
  // 算法接口
  queryAlgorithm (algorithmCategory) {
    return request({
      url: `/algorithm/query?algorithm_category=${algorithmCategory}`,
      method: 'GET'
    })
  },
  // 学习器训练方法描述接口
  queryAlgorithmTrainMethodsIntroductions (trainName) {
    return request({
      url: `/algorithm/queryIntroductions?trainName=${trainName}`,
      method: 'GET'
    })
  },
  // 查询待处理学习器危险警告信息
  queryDangerWarnInfo (id) {
    return request({
      url: `/learner/action/queryDangerWarnInfo?learner_id=${id}`,
      method: 'GET'
    })
  },
  // 查询待处理学习器信息
  queryActionDetail (id) {
    return request({
      url: `/learner/action/query?learner_id=${id}`,
      method: 'GET'
    })
  },
  // 提交待处理学习器的动作
  submitAction (form) {
    return request({
      url: '/learner/action/input',
      method: 'POST',
      data: {
        learner_id: form.learner_id,
        learner_action: form.learner_action
      },
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }
}
