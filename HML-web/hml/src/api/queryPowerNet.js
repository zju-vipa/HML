import request from '../utils/request'

export default {
  // 查询电网数据生成任务列表
  query () {
    return request({
      url: '/data/powerNet/query',
      method: 'GET'
    })
  },
  // 根据id查询任务
  queryJob (id) {
    return request({
      url: `/data/powerNet/queryJob?job_id=${id}`,
      method: 'GET'
    })
  },
  // 根据样例名称查询样例描述
  queryNetDescription (name) {
    return request({
      url: `/data/powerNet/queryNetDescription?name=${name}`,
      method: 'GET'
    })
  },
  // 创建电网数据生成任务（一键生成）
  addPowerNetDataset (form) {
    return request({
      url: '/data/powerNet/add',
      method: 'POST',
      // 'Content-Type': 'application/json',
      data: {
        pn_job_name: form.pn_job_name,
        pn_job_type: form.pn_job_type,
        pn_job_description: form.pn_job_description,
        init_net_name: form.init_net_name,
        disturb_src_type_list: form.disturb_src_type_list,
        disturb_n_var: form.disturb_n_var,
        disturb_radio: form.disturb_radio,
        disturb_n_sample: form.disturb_n_sample
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
  }
//   // 删除数据集
//   deleteData (id) {
//     return request({
//       url: `/decision/delete?decision_id=${id}`,
//       method: 'GET'
//     })
//   },
//   // 下载决策特征工程的
//   downloadHumanFea (id) {
//     return request({
//       url: `/decision/download/transform?decision_id=${id}`,
//       method: 'GET',
//       responseType: 'blob'
//     })
//   },
//   // 下载预测结果
//   downloadPredicition (id) {
//     return request({
//       url: `/decision/download/prediction?decision_id=${id}`,
//       method: 'GET',
//       responseType: 'blob'
//     })
//   },
//   // 下载数据集
//   downloadReport (id) {
//     return request({
//       url: `/decision/download/report?decision_id=${id}`,
//       method: 'GET',
//       responseType: 'blob'
//     })
//   },
//   // 查看任务分析进度条
//   searchHFProgress (id) {
//     return request({
//       url: `/decision/task/apply/featureEng/state?task_id=${id}`,
//       method: 'GET'
//     })
//   },
//   searchLeaProgress (id) {
//     return request({
//       url: `/decision/task/apply/learner/state?task_id=${id}`,
//       method: 'GET'
//     })
//   },
//   searchAllProgress (id) {
//     return request({
//       url: `/decision/task/apply/decision/state?task_id=${id}`,
//       method: 'GET'
//     })
//   }
}
