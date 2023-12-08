<template>
    <div>
    <!-- 面包屑区域 -->
    <!-- <el-breadcrumb v-if="!isLearnDialog" separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">人在回路</el-breadcrumb-item>
        <el-breadcrumb-item>学习</el-breadcrumb-item>
        <el-breadcrumb-item>查看学习器</el-breadcrumb-item>
    </el-breadcrumb> -->
    <el-card>
        <!-- 当前任务 -->
        <h1 v-if="!isLearnDialog">当前学习器</h1>
        <div v-if="!isLearnDialog">
            <el-button class="opbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left" style="font-size: 16px">返回</el-button>
        </div>
        <el-table :data="LearnerData" border stripe :row-style="{height:'80px'}" style="font-size: 20px" :cell-style="cellStyle"
        :highlight-current-row="isLearnDialog" @current-change="clickCurrentChange">
          <!-- 操作 -->
          <el-table-column type="expand" v-if="!isLearnDialog">
            <template slot-scope="scope" >
              <el-button v-if="scope.row.action===-1" size="mini" plain @click="handleLearner(scope.row.learner_id)" style="font-size: 16px">待处理</el-button>
              <el-button  size="mini" plain @click="trainProgress(scope.row.task_id)" style="font-size: 16px">训练进度</el-button>
              <el-button size="mini" plain @click="handleDownLoadPrediction(scope.row)" style="font-size: 16px">下载预测结果</el-button>
              <el-button size="mini" plain @click="handleDownLoadReport(scope.row)" style="font-size: 16px">下载预测报告</el-button>
              <el-button v-if="scope.row.train_state==='2' && (scope.row.learner_parameters.train_name ==='HML_RL'|| scope.row.learner_parameters.train_name === 'HML_ML')" size="mini" plain @click="handleModelTest(scope.row.learner_id)" style="font-size: 16px">模型测试</el-button>
              <el-button  size="mini" type="danger" plain icon="el-icon-delete" @click="handleDelete(scope.row.learner_id)" style="font-size: 16px">删除</el-button>
              <!-- <el-button  size="mini" type="primary" plain  @click="taskProgress(scope.row.task_id)">操作进度</el-button>
              <el-button  size="mini" type="danger" plain  @click="handleDelete(scope.row.featureEng_id)">删除</el-button> -->
            </template>
          </el-table-column>
          <el-table-column label="序号" type="index"> </el-table-column>
          <el-table-column prop="learner_name" label="学习器名" sortable :sort-method="sortByLearnerName"> </el-table-column>
          <el-table-column prop="learner_type" label="学习器类型" sortable :sort-method="sortByLearnerType">
            <template slot-scope="scope">{{scope.row.learner_type | learnerTypeTrans}}</template>
          </el-table-column>
          <el-table-column prop="start_time" label="创建时间" sortable :sort-method="sortByLearnerStartTime"> </el-table-column>
          <el-table-column prop="train_state" label="训练状态" sortable :sort-method="sortByTrainState">
            <template slot-scope="scope">{{scope.row.train_state | trainTypeTrans(scope)}}</template>
          </el-table-column>
          <!-- <el-table-column label="操作" width="400" v-if="!isLearnDialog">
            <template slot-scope="scope">
              <el-button  size="mini" type="primary" @click="trainProgress(scope.row.task_id)">训练进度</el-button>
              <el-button size="mini" type="primary" @click="handleDownLoadPrediction(scope.row)">下载预测结果</el-button>
              <el-button size="mini" type="primary"  @click="handleDownLoadReport(scope.row)">下载预测报告</el-button>
              <el-button  size="mini" type="danger" icon="el-icon-delete" @click="handleDelete(scope.row.learner_id)"></el-button>
            </template>
          </el-table-column> -->
        </el-table>
    </el-card>
        <!-- 查看进度条的对话框 -->
    <el-dialog title="查看学习器训练进度" :visible.sync="queryProgressVisible" width="30%">
      <el-progress type="circle" :percentage="progress*100"></el-progress>
    </el-dialog>
        <!-- 模型测试的对话框 -->
    <el-dialog title="查看学习器测试进度" :visible.sync="modelTestVisible" width="30%">
      <el-progress v-if="modelTestVisible != 'SUCCESS'" type="circle" :percentage="modelTestProgress*100"></el-progress>
      <div v-if="modelTestState === 'SUCCESS'" class = "basicGenPower" >平均reward为：{{ modelTestReward }}</div>
    </el-dialog>
    </div>
</template>
<script>
import learnApi from './../../api/learn'
// 操作状态
const trainStatus = [
  { type: '0', name: '不进行训练' },
  { type: '1', name: '训练中' },
  { type: '2', name: '训练完成' },
  { type: '3', name: '训练失败' }
]
// 学习器类型
const learnerTypeOptions = [
  { type: 'Manual', name: '人工' },
  { type: 'Machine', name: '自动化' },
  { type: 'HumanInLoop', name: '人在回路' }
]
export default {
  filters: {
    // 过滤器中this指向的不是vue实例，所以无法直接获取data中的数据
    learnerTypeTrans (type) {
      const obj = learnerTypeOptions.find(item => item.type === type)
      return obj ? obj.name : null
    },
    trainTypeTrans (type, ss) {
      console.log(ss)
      const obj = trainStatus.find(item => item.type === type)
      if (obj) {
        if (obj.type === '1' && ss.row.action === -1) {
          return '待处理'
        } else {
          return obj.name
        }
      }
      return null
    }
  },
  props: {
    // 这里接受父组件传过来的数据，如果isDialog为true，则为弹窗
    isLearnDialog: Boolean
  },
  data () {
    return {
      // 人工特征工程列表
      LearnerData: [],
      // 特征工程操作状态
      trainStatus: [],
      learnerTypeOptions: [],
      // 查看操作进度对话框
      queryProgressVisible: false,
      progress: 0,
      progressStatus: '',
      modelTestVisible: false,
      modelTestState: '',
      modelTestProgress: 0,
      modelTestReward: 0,
      timer: null
    }
  },
  created () {
    this.getLearnerInfo()
    this.timer = setInterval(() => {
      this.getLearnerInfo()
    }, 10000)
  },
  destroyed () {
    clearInterval(this.timer)
  },
  methods: {
    // 获取学习器信息
    getLearnerInfo () {
      // console.log('getLearnerInfo')
      learnApi.query().then(response => {
        // console.log(response)
        const resp = response.data
        if (resp.meta.code === 200) {
          // this.$message.success('加载学习器成功')
          this.LearnerData = resp.data
          console.log('this.LearnerData', this.LearnerData)
        }
      })
    },
    // 排序
    sortByLearnerType (obj1, obj2) {
      return obj1.learner_type.localeCompare(obj2.learner_type)
    },
    sortByLearnerName (obj1, obj2) {
      return obj1.learner_name.localeCompare(obj2.learner_name)
    },
    sortByTrainState (obj1, obj2) {
      return (obj1.train_state > obj2.train_state) ? 1 : ((obj1.train_state === obj2.train_state) ? (obj1.action - obj2.action) : -1)
    },
    sortByLearnerStartTime (obj1, obj2) {
      var date1 = new Date(obj1.start_time)
      var date2 = new Date(obj2.start_time)
      return (date1.getTime() - date2.getTime())
    },
    // 待处理
    handleLearner (rowId) {
      console.log(rowId)
      if (rowId) {
        this.$router.push({ path: '/learn/queryLearnerDetail', query: { learnerId: rowId } })
      } else {
        this.$message.error('该学习器未进行训练')
      }
    },
    // 模型测试
    handleModelTest (rowId) {
      console.log(rowId)
      this.modelTestVisible = true
      learnApi.learnerTest(rowId).then(response => {
        console.log(response)
        const resp = response.data.data
        this.modelTestProgress = resp.progress
        this.modelTestState = resp.state
        if (resp.state === 'SUCCESS') {
          this.modelTestReward = resp.reward
        }
      })
    },
    // 查看分析任务进度
    trainProgress (rowId) {
      console.log(rowId)
      if (rowId) {
        this.queryProgressVisible = true
        learnApi.searchProgress(rowId).then(response => {
          console.log(response)
          const resp = response.data.data
          this.progress = resp.progress
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
    // 下载预测结果文件
    handleDownLoadPrediction (row) {
      console.log(row)
      // console.log(row.learner_parameters)
      // console.log(row.learner_parameters.train_name)
      if (row.train_state === '2') {
        learnApi.downloadPrediction(row.learner_id).then(response => {
          console.log(response)
          const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }))
          const link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          link.setAttribute('download', row.dataset_id + 'predicition' + '.csv')
          document.body.appendChild(link)
          link.click()
        // const resp = response.data
        })
      } else {
        return this.$message.error('未训练完成，不能下载')
      }
    },
    // 下载预测报告文件
    handleDownLoadReport (row) {
      console.log(row)
      if (row.train_state === '2') {
        learnApi.downloadReport(row.learner_id).then(response => {
          console.log(response)
          const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }))
          const link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          link.setAttribute('download', row.dataset_id + 'report' + '.csv')
          document.body.appendChild(link)
          link.click()
        // const resp = response.data
        })
      } else {
        return this.$message.error('未训练完成，不能下载')
      }
    },
    // 发送给父组件决策
    clickCurrentChange (currentRow) {
      this.$emit('learner-choose', currentRow)
    },
    // 删除按钮，删除数据集
    handleDelete (rowId) {
      // console.log(rowId)
      this.$confirm('此操作将永久删除该特征工程, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        learnApi.deleteData(rowId).then(response => {
          this.$message.success('删除成功')
          this.getLearnerInfo()
        })
      }).catch(error => {
        this.$message.info('已取消删除')
        return error
      })
    },
    // 将待处理显示为红色
    cellStyle (row, column, rowIndex, columnIndex) {
      // 根据报警级别显示颜色
      // console.log(row);
      // console.log(row.column);
      if (row.column.label === '训练状态' && row.row.train_state === '1' && row.row.action === -1) {
        // 待处理
        return 'background:#FFDAB9'
      } else if (row.column.label === '训练状态' && row.row.train_state === '1') {
        // 训练中
        return 'background:#FFFACD'
      } else if (row.column.label === '训练状态' && row.row.train_state === '2') {
        // 训练完成
        return 'background:#bcf0c2'
      } else if (row.column.label === '训练状态' && row.row.train_state === '3') {
        // 训练失败
        return 'background:#c8cbc9'
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
  h1{
    padding-bottom: 10px;
    font-size: 32px;
    border-bottom: 3px solid rgb(102, 102, 102)
  }
  .opbtn{
    margin-bottom: 10px;
  }
</style>
