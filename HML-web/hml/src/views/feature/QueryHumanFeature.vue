<template>
    <div>
    <el-card>
        <!-- 当前任务 -->
        <h3 v-if="!isHFeaDialog">当前特征工程</h3>
        <div>
            <el-button class="opbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
        </div>
        <!-- <div @click="backPage"><i class="el-icon-arrow-left backPage"></i><span>返回</span></div> -->
        <el-table :data="HumanFeaData" border stripe  style="width: 100%"
        :highlight-current-row="isHFeaDialog" @current-change="clickCurrentChange">
          <!-- 操作 -->
          <el-table-column type="expand" v-if="!isHFeaDialog">
            <template slot-scope="scope">
              <el-button  size="mini" type="primary" plain  @click="taskProgress(scope.row.task_id)">操作进度</el-button>
              <el-button  size="mini" type="danger" plain icon="el-icon-delete" @click="handleDelete(scope.row.featureEng_id)">删除</el-button>
            </template>
          </el-table-column>
          <el-table-column  label="序号" type="index"> </el-table-column>
          <el-table-column prop="featureEng_name" label="特征工程名"> </el-table-column>
          <el-table-column prop="featureEng_type" label="特征工程类型"> </el-table-column>
          <el-table-column prop="operate_state" label="操作状态">
            <template slot-scope="scope">{{scope.row.operate_state | operateTypeTrans}}</template>
          </el-table-column>
          <!-- <el-table-column v-if="!isHFeaDialog" label="操作">
            <template slot-scope="scope">
              <el-button  size="mini" type="primary" @click="taskProgress(scope.row.task_id)">特征工程操作进度</el-button>
              <el-button  size="mini" @click="handleDelete(scope.row.featureEng_id)" type="danger" icon="el-icon-delete"></el-button>
            </template>
           </el-table-column> -->
        </el-table>
    </el-card>
        <!-- 查看进度条的对话框 -->
    <el-dialog title="查看特征工程操作任务进度" :visible.sync="queryProgressVisible" width="30%">
      <!-- <el-progress type="circle" :percentage="25"></el-progress> -->
      <el-progress type="circle" :percentage="progress*100"></el-progress>
    </el-dialog>
    </div>
</template>
<script>
import queryFeaApi from './../../api/queryFea'
// 操作状态
const operateStatus = [
  { type: '0', name: '不进行操作' },
  { type: '1', name: '操作中' },
  { type: '2', name: '操作完成' },
  { type: '3', name: '操作失败' }
]
export default {
  filters: {
    // 过滤器中this指向的不是vue实例，所以无法直接获取data中的数据
    operateTypeTrans (type) {
      const obj = operateStatus.find(item => item.type === type)
      return obj ? obj.name : null
    }
  },
  props: {
    isHFeaDialog: Boolean
  },
  data () {
    return {
      // 人工特征工程列表
      HumanFeaData: [],
      // 特征工程操作状态
      operateStatus: [],
      // 查看操作进度对话框
      queryProgressVisible: false,
      progress: 0,
      progressStatus: ''
    }
  },
  created () {
    this.getHumanFeaInfo()
  },
  methods: {
    // 获取数据集信息
    getHumanFeaInfo () {
      queryFeaApi.query().then(response => {
        console.log(response)
        const resp = response.data
        if (resp.meta.code === 200) {
          this.$message.success('加载人工特征工程成功')
          this.HumanFeaData = resp.data
        }
        console.log(response)
        console.log(this.HumanFeaData)
      })
    },
    // 查看分析任务进度
    taskProgress (rowId) {
      console.log(rowId)
      if (rowId) {
        this.queryProgressVisible = true
        queryFeaApi.searchProgress(rowId).then(response => {
          console.log(response)
          const resp = response.data.data
          if (resp.state === 'FAILURE') {
            this.progress = 0
          } else if (resp.state === 'SUCCESS') {
            this.progress = resp.progress
          } else if (resp.state === 'PENDING') {
            this.progress = 0
          }
        })
      } else {
        this.$message.error('该特征工程未进行操作')
      }
    },
    // 当点击某一行，调用这个函数，发送选中的特征到决策页面
    clickCurrentChange (currentRow) {
      this.$emit('choose-HumanFea', currentRow)
    },
    // 删除按钮，删除数据集
    handleDelete (rowId) {
      // console.log(rowId)
      this.$confirm('此操作将永久删除该特征工程, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        queryFeaApi.deleteData(rowId).then(response => {
          console.log(12)
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
  /* h3{
    text-align: center;
  } */
  .backPage{
    margin-bottom: 30px;
    margin-left: 10px;
    font-size: 15px;
    color: #367FA9;
    font-weight: bold;
    margin-right: 10px;
  }
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
  /* .el-button--goon.is-active,
  .el-button--goon:active {
    background: #20B2AA;
    border-color: #20B2AA;
    color: #fff;
  }
  .el-button--goon:focus,
  .el-button--goon:hover {
    background: #48D1CC;
    border-color: #48D1CC;
    color: #fff;
  }
  .el-button--goon {
    color: #FFF;
    background-color: #20B2AA;
    border-color: #20B2AA;
  } */

</style>
