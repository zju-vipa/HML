<template>
    <div>
                  <!-- 面包屑区域 -->
      <!-- <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">人在回路</el-breadcrumb-item>
        <el-breadcrumb-item>决策</el-breadcrumb-item>
        <el-breadcrumb-item>查看决策</el-breadcrumb-item>
    </el-breadcrumb> -->
    <el-card>
      <!-- <el-button class="queryBtn" @click="gotoDecision"  type="primary">返回主决策页面</el-button> -->
        <!-- 当前任务 -->
      <h3>当前决策</h3>
      <div>
            <el-button class="opbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
      </div>
      <el-table :data="decisionData" border stripe  style="width: 100%">
        <!-- 操作 -->
        <el-table-column type="expand">
          <template slot-scope="scope">
            <el-button style="width:140px" size="mini" :disabled="scope.row.featureEng_id==null"
              @click="handleDownLoadFeaRes(scope.row)" icon="el-icon-download">决策特征工程结果</el-button>
            <el-button size="mini" :disabled="scope.row.learner_id==null"
              @click="handleDownLoadPrediction(scope.row)" icon="el-icon-download">预测结果</el-button>
            <el-button size="mini" :disabled="scope.row.learner_id==null"
              @click="handleDownLoadReport(scope.row)" icon="el-icon-download">预测报告</el-button>
            <el-button size="mini" plain type="danger"
              @click="handleDelete(scope.row.decision_id)" icon="el-icon-delete">删除</el-button>
            </template>
        </el-table-column>
        <el-table-column  label="序号" type="index"> </el-table-column>
        <el-table-column prop="decision_name" label="决策名"> </el-table-column>
        <el-table-column prop="decision_type" label="决策类型">
          <template slot-scope="scope">{{scope.row.decision_type | decisionTypeTrans}}</template>
        </el-table-column>
        <el-table-column prop="apply_state" label="应用状态">
          <template slot-scope="scope">{{scope.row.apply_state | applyStateTrans}}</template>
        </el-table-column>
        <el-table-column label="查询进度"  width="350">
          <template slot-scope="scope">
            <el-button size="mini" type="danger" :disabled="scope.row.featureEng_id==null"
            @click="queryHuFeaPrgress(scope.row.task_id)">应用特征工程</el-button>
            <el-button size="mini" type="warning" :disabled="scope.row.learner_id==null"
            @click="queryLearnerPrgress(scope.row.task_id)">应用学习器</el-button>
            <el-button size="mini" type="success" :disabled="scope.row.learner_id==null"
             @click="queryAllPrgress(scope.row.task_id)">应用决策</el-button>
          </template>
        </el-table-column>
        <!-- <el-table-column label="下载"  width="400">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" :disabled="scope.row.featureEng_id==null"
            @click="handleDownLoadFeaRes(scope.row)">决策特征工程结果</el-button>
            <el-button size="mini" type="primary" :disabled="scope.row.learner_id==null"
            @click="handleDownLoadPrediction(scope.row)">预测结果</el-button>
            <el-button size="mini" type="primary" :disabled="scope.row.learner_id==null"
             @click="handleDownLoadReport(scope.row)">预测报告</el-button>
            <el-button  size="mini" @click="handleDelete(scope.row.decision_id)" type="danger" icon="el-icon-delete"></el-button>
          </template>
        </el-table-column> -->
      </el-table>
    </el-card>
            <!-- 查看应用特征工程进度条的对话框 -->
    <el-dialog title="查看应用特征工程进度" :visible.sync="queryHFProgressVisible" width="30%">
      <el-progress type="circle" :percentage="progressFea*100"></el-progress>
    </el-dialog>
            <!-- 查看应用特征工程进度条的对话框 -->
    <el-dialog title="查看应用学习器进度" :visible.sync="queryLeaProgressVisible" width="30%">
      <el-progress type="circle" :percentage="progressLea*100"></el-progress>
    </el-dialog>
            <!-- 查看应用特征工程进度条的对话框 -->
    <el-dialog title="查看应用决策进度" :visible.sync="queryAllProgressVisible" width="30%">
      <el-progress type="circle" :percentage="progressAll*100"></el-progress>
    </el-dialog>
    </div>
</template>
<script>
import queryDecisionApi from './../../api/queryDecision'
// 操作状态
const applyStateOptions = [
  { type: '0', name: '不进行应用' },
  { type: '1', name: '应用中' },
  { type: '2', name: '应用完成' },
  { type: '3', name: '应用失败' }
]
// 学习器类型
const decisionTypeOptions = [
  { type: 'Manual_FE', name: '应用特征工程' },
  { type: 'Manual_L', name: '应用学习器' },
  { type: 'Manual_D', name: '应用决策者' }
]
export default {
  filters: {
    decisionTypeTrans (type) {
      const obj = decisionTypeOptions.find(item => item.type === type)
      return obj ? obj.name : null
    },
    // 过滤器中this指向的不是vue实例，所以无法直接获取data中的数据
    applyStateTrans (type) {
      const obj = applyStateOptions.find(item => item.type === type)
      return obj ? obj.name : null
    }
  },
  data () {
    return {
      // 决策列表
      decisionData: [],
      // 特征工程操作状态
      operateStatus: [],
      // 查看操作进度对话框
      queryProgressVisible: false,
      progressFea: 0,
      progressLea: 0,
      progressAll: 0,
      progressStatus: '',
      // 分别应用于特征，学习器和决策的对话框
      queryHFProgressVisible: false,
      queryLeaProgressVisible: false,
      queryAllProgressVisible: false
    }
  },
  created () {
    this.getHumanFeaInfo()
  },
  methods: {
    // 获取决策所有信息
    getHumanFeaInfo () {
      queryDecisionApi.query().then(response => {
        console.log(response)
        const resp = response.data
        if (resp.meta.code === 200) {
          // this.$message.success('加载决策成功')
          this.decisionData = resp.data
        }
      })
    },
    // 下载决策者数据集特征工程结果文件接口
    handleDownLoadFeaRes (row) {
      console.log(row)
      if (row.apply_state === '2') {
        queryDecisionApi.downloadHumanFea(row.decision_id).then(response => {
          console.log(response)
          const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }))
          const link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          link.setAttribute('download', row.decision_id + 'Feature' + '.csv')
          document.body.appendChild(link)
          link.click()
        })
      } else {
        return this.$message.error('未应用完成，不能下载')
      }
    },
    // 下载预测结果文件
    handleDownLoadPrediction (row) {
      console.log(row)
      if (row.apply_state === '2') {
        queryDecisionApi.downloadPredicition(row.decision_id).then(response => {
          console.log(response)
          const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }))
          const link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          link.setAttribute('download', row.dataset_id + 'predicition' + '.csv')
          document.body.appendChild(link)
          link.click()
        })
      } else {
        return this.$message.error('未应用完成，不能下载')
      }
    },
    // 下载预测报告文件
    handleDownLoadReport (row) {
      console.log(row)
      if (row.apply_state === '2') {
        queryDecisionApi.downloadReport(row.decision_id).then(response => {
          console.log(response)
          const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }))
          const link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          link.setAttribute('download', row.dataset_id + 'report' + '.csv')
          document.body.appendChild(link)
          link.click()
        })
      } else {
        return this.$message.error('未应用完成，不能下载')
      }
    },
    // 应用决策特征工程进度查询
    queryHuFeaPrgress (rowId) {
      // console.log(rowId)
      if (rowId) {
        this.queryHFProgressVisible = true
        queryDecisionApi.searchHFProgress(rowId).then(response => {
          // console.log(response)
          const resp = response.data.data
          this.progressFea = resp.progress
          // if (resp.state === 'FAILURE') {
          //   this.progress = 0
          // } else if (resp.state === 'SUCCESS') {
          //   this.progress = resp.progress
          // } else if (resp.state === 'PENDING') {
          //   this.progress = 0
          // }
        })
      } else {
        this.$message.error('该学习器未进行训练')
      }
    },
    // 应用学习器
    queryLearnerPrgress (rowId) {
      console.log(rowId)
      if (rowId) {
        this.queryLeaProgressVisible = true
        queryDecisionApi.searchLeaProgress(rowId).then(response => {
          console.log(response)
          const resp = response.data.data
          this.progressLea = resp.progress
          // if (resp.state === 'FAILURE') {
          //   this.progress = 0
          // } else if (resp.state === 'SUCCESS') {
          //   this.progress = resp.progress
          // } else if (resp.state === 'PENDING') {
          //   this.progress = 0
          // }
        })
      } else {
        this.$message.error('该学习器未进行训练')
      }
    },
    // 应用决策
    queryAllPrgress (rowId) {
      if (rowId) {
        this.queryAllProgressVisible = true
        queryDecisionApi.searchAllProgress(rowId).then(response => {
          // console.log(response)
          const resp = response.data.data
          this.progressAll = resp.progress
          // if (resp.state === 'FAILURE') {
          //   this.progress = 0
          // } else if (resp.state === 'SUCCESS') {
          //   this.progress = resp.progress
          // } else if (resp.state === 'PENDING') {
          //   this.progress = 0
          // }
        })
      } else {
        this.$message.error('该学习器未进行训练')
      }
    },
    gotoDecision () {
      this.$router.push('/decision')
    },
    // 删除按钮，删除数据集
    handleDelete (rowId) {
      // console.log(rowId)
      this.$confirm('此操作将永久删除该特征工程, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        queryDecisionApi.deleteData(rowId).then(response => {
          this.$message.success('删除成功')
          this.getHumanFeaInfo()
        })
      }).catch(error => {
        this.$message.info('已取消删除')
        return error
      })
    },
    // 返回上一页
    backPage () {
      this.$router.back()
    }
  }
}
</script>
<style scoped>
/* .queryBtn {
  margin-bottom: 20px;
} */
  /* h3{
    text-align: center;
  } */
  /* .backPage{
    margin-bottom: 30px;
    margin-left: 10px;
    font-size: 15px;
    color: #367FA9;
    font-weight: bold;
    margin-right: 10px;
  } */
  .el-card{
    margin: 10px 20px;
  }
  h3{
    padding-bottom: 10px;
    border-bottom: 3px solid rgb(102, 102, 102)
  }
  .opbtn{
    margin-bottom: 10px;
  }
</style>
