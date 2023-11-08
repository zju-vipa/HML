import request from '../utils/request'

export default {
  // 1023 决策树
  fetchDecisionTree1 (form) {
    return request({
      url: '/decision/apply/mam1',
      method: 'POST',
      data: {
        treeType: 'tree1'
      },
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  fetchDecisionTree2 (form) {
    return request({
      url: '/decision/apply/mam1',
      method: 'POST',
      data: {
        treeType: 'tree2'
      },
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 断面算法
  addMam (form) {
    return request({
      url: '/decision/apply/mam',
      method: 'POST',
      data: {
        // decision_name: form.decision_name,
        // decision_type: form.decision_type,
        // decision_parameters: form.decision_parameters,
        // learner_id: form.learner_id,
        // featureEng_id: form.featureEng_id,
        // dataset_id: form.dataset_id
        task: form.task,
        case: form.case
      },
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 添加数据集 - 应用决策者
  addAllDec (form) {
    return request({
      url: '/decision/apply/decision',
      method: 'POST',
      data: {
        decision_name: form.decision_name,
        decision_type: form.decision_type,
        decision_parameters: form.decision_parameters,
        learner_id: form.learner_id,
        featureEng_id: form.featureEng_id,
        dataset_id: form.dataset_id
      },
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 添加数据集 - 应用特征工程
  addHumanFea (form) {
    return request({
      url: '/decision/apply/featureEng',
      method: 'POST',
      data: {
        decision_name: form.decision_name,
        decision_type: form.decision_type,
        decision_parameters: form.decision_parameters,
        featureEng_id: form.featureEng_id,
        dataset_id: form.dataset_id
      },
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 添加数据集 - 应用学习器
  addLearner (form) {
    return request({
      url: '/decision/apply/learner',
      method: 'POST',
      data: {
        decision_name: form.decision_name,
        decision_type: form.decision_type,
        decision_parameters: form.decision_parameters,
        learner_id: form.learner_id,
        dataset_id: form.dataset_id
      },
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 查询学习器
  query () {
    return request({
      url: '/learner/query',
      method: 'GET'
    })
  },
  // 下载数据集
  downloadPrediction (id) {
    return request({
      url: `/learner/download/prediction?learner_id=${id}`,
      method: 'GET',
      responseType: 'blob'
    })
  },
  // 下载数据集
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
  }
}
