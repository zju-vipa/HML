import request from '../utils/request'

export default {
  // 1226GCN决策器优化卡片
  addDecisionMaker (payload) {
    return request({
      url: '/decision/apply/adddecisionmaker',
      method: 'POST',
      data: payload,
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 1226GCN决策器蒸馏卡片
  addDecisionMaker1 (payload) {
    return request({
      url: '/decision/apply/adddecisionmaker1',
      method: 'POST',
      data: payload,
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 1226GCN决策器路径可视化卡片
  addDecisionMaker2 (payload) {
    return request({
      url: '/decision/apply/adddecisionmaker2',
      method: 'POST',
      data: payload,
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 1227决策树图像传输
  fetchVisualizationImage (params) {
    return request({
      url: '/decision/visualize/path',
      method: 'GET',
      params: params
    })
  },
  // 1229决策器名称传递
  fetchDecisionMakers () {
    return request({
      url: '/decision/get/decisionmakers',
      method: 'GET'
    })
  },
  // 1229蒸馏器名称传递
  fetchDecisionMakers1 () {
    return request({
      url: '/decision/get/decisionmakers1',
      method: 'GET'
    })
  },
  // 1230交互记录卡片——删除决策器名称，data请求体要写成json的格式，需要将数据包装在一个对象，不能直接写decisionMakerName，否则无法识别
  deleteDesionMaker (decisionMakerName) {
    return request({
      url: '/decision/delete/decisionmaker',
      method: 'POST',
      data: { decisionMakerName: decisionMakerName },
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 1230交互记录卡片——删除蒸馏器名称
  deleteDesionMaker1 (decisionMakerName) {
    return request({
      url: '/decision/delete/decisionmaker1',
      method: 'POST',
      data: { decisionMakerName: decisionMakerName },
      headers: {
        'Content-Type': 'application/json'
      }
    })
  },
  // 1023 决策树
  fetchDecisionTree1 (form) {
    return request({
      url: '/decision//apply/mam1',
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
      url: '/decision//apply/mam1',
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
