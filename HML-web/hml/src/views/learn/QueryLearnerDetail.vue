<template>
  <div>
    <!-- 标题 -->
    <div>
      <el-col :span="2">
        <el-button class="backbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
      </el-col>
      <el-col :span="22">
        <h2>待处理学习器</h2>
      </el-col>
    </div>
    <div>
      <el-card>
        <!-- 任务信息 -->
        <div><h3>学习器信息</h3></div>
        <el-form label-position="right" label-width="150px" :model="learnerInfo">
          <el-row>
            <el-col :span="10">
              <el-form-item label="学习器名称" prop="learner_name">
                <el-input disabled  v-model="learnerInfo.learner_name" style="width: 200px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="10">
              <el-form-item label="学习器类型" prop="learner_type">
                <el-input disabled  v-model="learnerInfo.learner_name" style="width: 200px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
      <el-card>
        <!-- 任务信息 -->
        <div><h3>待处理</h3></div>
        <el-form label-position="right" label-width="150px" :model="learnerInfo">
          <el-row>
            <el-col :span="10">
              <el-form-item label="输入动作" prop="pn_job_name">
                <el-input v-model="learnerInfo.learner_action" style="width: 200px"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-button class="dealBtn" type="primary" @click="submitAction">提交动作</el-button>
            </el-col>
          </el-row>
        </el-form>
        <el-row>
          <el-col :span="14">
            <el-card style="height: 400px">
              <div><h3>电网当前状态</h3></div>
              <el-table :data="netDetailInfo" border stripe :cell-style="cellStyle"
                height="300" style="width:100%">
                <el-table-column width="120" v-for="(item,index) in detailColumns"
                  :key="index" :prop="item" :label="item" :formatter="formatValues"></el-table-column>
              </el-table>
            </el-card>
          </el-col>
        </el-row>
        <el-row align="middle">
          <el-col :span="10">
            <img :src="'http://10.214.211.135:8030/img/learner118.png'" style="width: 1000px">
          </el-col>
        </el-row>
      </el-card>
    </div>
  </div>
</template>
<script>
import learnApi from './../../api/learn'
// 学习器类型
const learnerTypeOptions = [
  { type: 'Manual', name: '人工' },
  { type: 'Machine', name: '自动化' },
  { type: 'HumanInLoop', name: '人在回路' }
]
// 有哪些列
const detailColumns = ['p', 'q', 'v', 't']
export default {
  filters: {
    // is_done转换成 “已完成” “未完成”
    // applyJobStatusTrans (type) {
    //   return type ? '已完成' : '未完成'
    // }
  },
  data () {
    return {
    //   // 电网数据生成任务列表
    //   powerNetData: [],
    //   // 全部任务数，已完成任务数，未完成任务数 (异步)
    //   powerNetJobCnt: 0,
    //   powerNetJobDoneCnt: 0,
    //   powerNetJobUndoneCnt: 0
      // 任务ID，名称，生成方式，描述
      learnerInfo: {
        learner_id: '',
        learner_name: '',
        learner_type: '',
        learner_parameters: '',
        train_state: '',
        task_id: '',
        dataset_id: '',
        learner_action: ''
      },
      netDetailInfo: [],
      submitActionForm: {},
      learnerTypeOptions,
      detailColumns
    }
  },
  created () {
    this.getLearnerInfo(this.$route.query.learnerId)
  },
  methods: {
    getLearnerInfo (learnerId) {
      learnApi.queryActionDetail(learnerId).then(response => {
        console.log(learnerId)
        const resp = response.data
        if (resp.meta.code === 200) {
          this.$message.success('加载学习器成功')
          this.learnerInfo = {
            learner_id: resp.data.learner.learner_id,
            learner_name: resp.data.learner.learner_name,
            learner_type: resp.data.learner.learner_type,
            learner_parameters: resp.data.learner.learner_parameters,
            train_state: resp.data.learner.train_state,
            task_id: resp.data.learner.task_id,
            dataset_id: resp.data.learner.dataset_id,
            learner_action: ''
          }
          this.netDetailInfo = resp.data.detail
        }
      })
    },
    // 提交动作
    submitAction () {
      this.submitActionForm = {
        learner_id: this.learnerInfo.learner_id,
        learner_action: parseInt(this.learnerInfo.learner_action)
      }
      learnApi.submitAction(this.submitActionForm).then(response => {
        const resp = response.data
        console.log(response)
        if (resp.meta.code === 204) {
          this.$message.success('动作提交成功')
          this.$router.back()
        } else {
          this.$message.error('动作提交失败')
        }
      })
    },
    formatValues (row, column, cellValue) {
      if (cellValue === null) {
        return 'null'
      }
      if (cellValue === true) {
        return 'true'
      }
      if (cellValue === false) {
        return 'false'
      }
      return cellValue
    },
    cellStyle (row, column, rowIndex, columnIndex) {
      // 根据级别显示颜色
      // console.log(row);
      // console.log(row.column);
      if (row.column.label === 'P') {
        let color = Math.floor(row.row.P)
        if (color > 0xffffff) {
          color = 0xffffff
        }
        return `background:#${color.toString(16)}`
      } else if (row.column.label === 'Q') {
        let color = Math.floor(row.row.Q)
        if (color > 0xffffff) {
          color = 0xffffff
        }
        return `background:#${color.toString(16)}`
      } else if (row.column.label === 'V') {
        let color = Math.floor(row.row.V)
        if (color > 0xffffff) {
          color = 0xffffff
        }
        return `background:#${color.toString(16)}`
      } else if (row.column.label === 'Theta') {
        let color = Math.floor(row.row.Theta)
        if (color > 0xffffff) {
          color = 0xffffff
        }
        return `background:#${color.toString(16)}`
      }
    },
    // 返回上一页
    backPage () {
      this.$router.back()
    }
  }
}
</script>
<style scoped>
  .el-card{
    margin: 10px 20px;
  }
  h2{
     text-align: center;
  }
  h3{
    padding-bottom: 10px;
    /* border-bottom: 3px solid rgb(102, 102, 102) */
    border-bottom: 3px solid rgb(180, 180, 180);
  }
  h4{
    padding-bottom: 10px;
    /* border-bottom: 2px solid rgb(102, 102, 102) */
  }
  .backbtn{
    margin-top: 20px;
    /* margin-bottom: 10px; */
    margin-left:20px;
  }
  .downloadbtn{
    float: right;
    margin-top: 20px;
    margin-bottom: 20px;
  }
  .el-col{
    min-height: 1px;
  }
  .el-form-item{
  margin-bottom: 30px;
  }
.dealBtn{
  float: left;
  /* margin-top: 10px; */
  margin-bottom: 10px;
  margin-left: 10px;
  margin-right: 10px;
}
</style>
