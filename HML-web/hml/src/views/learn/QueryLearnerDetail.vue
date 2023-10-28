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
                <el-select disabled v-model="learnerInfo.learner_type" placeholder="学习器类型" style="width: 200px">
                  <el-option v-for="(option, index) in learnerTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>
                </el-select>
                <!-- <el-input disabled  v-model="learnerInfo.learner_type" style="width: 200px"></el-input> -->
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
                <!-- <el-input v-model="learnerInfo.learner_action" style="width: 200px"></el-input> -->
                <el-select  v-model="learnerInfo.learner_action" style="width: 200px">
                  <el-option v-for="(option, index) in actionOptions" :key="index" :label="option.name" :value="option.type"></el-option>
                  <!-- <el-option v-for="count in 106" :key="count-1" :label="count-1">{{((count-1)/2)}}号发电机调至{{((count-1)%2)? '0.5':'1.4'}}</el-option> -->
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-button class="dealBtn" type="primary" @click="submitAction">提交动作</el-button>
            </el-col>
          </el-row>
        </el-form>
        <el-row>
          <el-col :span="12">
            <!-- <el-card style="height: 400px"> -->
              <div><h4>电网当前状态</h4></div>
              <el-table :data="netDetailInfo" border stripe :cell-style="cellStyle"
                height="500" style="width:100%">
                <el-table-column label="序号" type="index" width="50" align="center">
                </el-table-column>
                <el-table-column width="120" v-for="(item,index) in detailColumns"
                  :key="index" :prop="item" :label="item" :formatter="formatValues"></el-table-column>
              </el-table>
            <!-- </el-card> -->
          </el-col>
          <el-col :span="12">
            <img :src="'http://10.214.211.137:8030/img/learner118.png'" style="width: 500px; height: 500px; object-fit: fill;">
            <!-- <img :src="'http://192.168.137.8:8030/img/learner118.png'" style="width: 500px; height: 500px; object-fit: fill;"> -->
          </el-col>
        </el-row>
        <!-- <el-row align="middle">
          <el-col :span="10">
            <img :src="'http://10.214.211.135:8030/img/learner118.png'" style="width: 500px; height: 500px; object-fit: fill;">
          </el-col>
        </el-row> -->
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
const detailColumns = ['P', 'Q', 'V', 'Theta']
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
      p_min: 0,
      p_max: 0,
      q_min: 0,
      q_max: 0,
      v_min: 0,
      v_max: 0,
      theta_min: 0,
      theta_max: 0,
      submitActionForm: {},
      learnerTypeOptions,
      actionOptions: [],
      detailColumns
    }
  },
  created () {
    this.setActionOptions()
    this.getLearnerInfo(this.$route.query.learnerId)
  },
  methods: {
    setActionOptions () {
      this.actionOptions = []
      const ratioOption = ['40%', '150%']
      for (var i = 0; i < 106; i++) {
        const genidx = Math.floor(i / 2)
        const ratio = ratioOption[i % 2]
        const s = `${genidx}号发电机出力水平调至${ratio}`
        this.actionOptions.push({ type: i, name: s })
      }
    },
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
          let pMin = 999
          let qMin = 999
          let vMin = 999
          let thetaMin = 999
          let pMax = -999
          let qMax = -999
          let vMax = -999
          let thetaMax = -999
          this.netDetailInfo.forEach(item => {
            if (item.P < pMin) {
              pMin = item.P
            }
            if (item.P > pMax) {
              pMax = item.P
            }
            if (item.Q < qMin) {
              qMin = item.Q
            }
            if (item.Q > qMax) {
              qMax = item.Q
            }
            if (item.V < vMin) {
              vMin = item.V
            }
            if (item.V > vMax) {
              vMax = item.V
            }
            if (item.Theta < thetaMin) {
              thetaMin = item.Theta
            }
            if (item.Theta > thetaMax) {
              thetaMax = item.Theta
            }
          })
          this.p_min = pMin
          this.p_max = pMax
          this.q_min = qMin
          this.q_max = qMax
          this.v_min = vMin
          this.v_max = vMax
          this.theta_min = thetaMin
          this.theta_max = thetaMax
          console.log(pMin, pMax, qMin, qMax, vMin, vMax, thetaMin, thetaMax)
          // console.log(this.netDetailInfo)
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
      return parseFloat(cellValue).toFixed(4)
    },
    cellStyle (row, column, rowIndex, columnIndex) {
      // 根据级别显示颜色
      // console.log(row);
      // console.log(row.column);
      if (row.column.label === 'P') {
        // const p = Math.floor((row.row.P - this.p_min) * 150 / (this.p_max - this.p_min))
        // let color = (p << 16) + 0x222222
        // while (color > 0xffffff) {
        //   color = color - 0x1000000
        // }
        const p = 255 - Math.floor((row.row.P - this.p_min) * 200 / (this.p_max - this.p_min))
        const color = 0xff0000 + (p << 8) + p
        return `color:black; font-size:16px; background:#${color.toString(16)};`
      } else if (row.column.label === 'Q') {
        // const q = Math.floor((row.row.Q - this.q_min) * 150 / (this.q_max - this.q_min))
        // // let color = ((q * 2) << 16) + (q << 8) + 0x111111
        // let color = (q << 16) + 0x222222
        // while (color > 0xffffff) {
        //   color = color - 0x1000000
        // }
        const q = 255 - Math.floor((row.row.Q - this.q_min) * 200 / (this.q_max - this.q_min))
        const color = 0xff0000 + (q << 8) + q
        return `color:black; font-size:16px; background:#${color.toString(16)}`
      } else if (row.column.label === 'V') {
        // const v = Math.floor((row.row.V - this.v_min) * 150 / (this.v_max - this.v_min))
        // let color = (v << 16) + 0x222222
        // while (color > 0xffffff) {
        //   color = color - 0x1000000
        // }
        const v = 255 - Math.floor((row.row.V - this.v_min) * 200 / (this.v_max - this.v_min))
        const color = 0xff0000 + (v << 8) + v
        return `color:black; font-size:16px; background:#${color.toString(16)}`
      } else if (row.column.label === 'Theta') {
        // const t = Math.floor((row.row.Theta - this.theta_min) * 150 / (this.theta_max - this.theta_min))
        // let color = (t << 16) + 0x222222
        // while (color > 0xffffff) {
        //   color = color - 0x1000000
        // }
        const t = 255 - Math.floor((row.row.Theta - this.theta_min) * 200 / (this.theta_max - this.theta_min))
        const color = 0xff0000 + (t << 8) + t
        return `color:black; font-size:16px; background:#${color.toString(16)}`
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
