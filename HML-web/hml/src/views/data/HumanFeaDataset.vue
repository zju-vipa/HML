<template>
    <div>
      <el-card>
        <!-- 当前任务 -->
        <!-- <h3 v-if="!isDialog">特征处理的数据集</h3> -->
        <div @click="backPage"><i class="el-icon-arrow-left backPage"></i><span>返回</span></div>
        <el-table :data="datasetData" border stripe
        :highlight-current-row="isDialog" @current-change="clickCurrentChange">
         <el-table-column type="expand" v-if="!isDialog">
            <template slot-scope="scope">
              <el-button class="opbtn" size="mini" plain type="primary" @click="handleDownLoadFile(scope.row.dataset_id)">数据下载</el-button>
              <el-button  class="opbtn" size="mini" plain type="primary"  @click="handleDownLoadProfile(scope.row)">分析下载</el-button>
              <el-button   size="mini" type="primary" plain  @click="taskProgress(scope.row.task_id)">分析进度</el-button>
              <el-button  size="mini" plain type="danger" @click="handleDelete(scope.row.dataset_id)">删除数据</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="dataset_name" label="数据集名"> </el-table-column>
          <el-table-column prop="file_type" label="数据集类型"> </el-table-column>
          <el-table-column prop="introduction" label="数据集介绍"> </el-table-column>
          <el-table-column prop="if_public" label="是否公开">
            <template slot-scope="scope">
              <el-switch disabled="" v-model="scope.row.if_public" active-color="#13ce66">
              </el-switch>
            </template>
          </el-table-column>
          <el-table-column prop="if_featureEng" label="是否特征工程">
            <template slot-scope="scope">
              <el-switch disabled v-model="scope.row.if_featureEng" active-color="#13ce66">
              </el-switch>
            </template>
          </el-table-column>
          <el-table-column prop="profile_state" label="分析状态" >
            <template slot-scope="scope">{{scope.row.profile_state | profileTypeTrans}}</template>
          </el-table-column>
          <!-- <el-table-column width="250" label="操作" v-if="!isDialog">
            <template slot-scope="scope">
              <el-row >
                <el-col :span="10">
                  <el-button class="opbtn" size="mini" plain type="primary" @click="handleDownLoadFile(scope.row.dataset_id)">数据下载</el-button>
                </el-col>
                <el-col :span="10">
                 <el-button  class="opbtn" size="mini" plain type="primary"  @click="handleDownLoadProfile(scope.row)">分析下载</el-button>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="10">
                  <el-button   size="mini" type="primary" plain  @click="taskProgress(scope.row.task_id)">分析进度</el-button>
                </el-col>
                <el-col :span="10">
                 <el-button  size="mini" plain type="primary" @click="handleDelete(scope.row.dataset_id)">删除数据</el-button>
                </el-col>
              </el-row>
            </template>
           </el-table-column> -->
        </el-table>
      </el-card>
      <!-- 查看进度条的对话框 -->
      <el-dialog title="查看数据集分析进度" :visible.sync="queryProgressVisible" width="30%">
        <!-- <el-progress type="circle" :percentage="25"></el-progress> -->
        <el-progress type="circle" :percentage="progress*100"></el-progress>
      </el-dialog>
    </div>
</template>

<script>
import datasetApi from '../../api/dataset'

// 分析状态
const profileStatus = [
  { type: '0', name: '不进行分析' },
  { type: '1', name: '分析中' },
  { type: '2', name: '分析完成' },
  { type: '3', name: '分析失败，数据格式有误' }
]
export default {
  name: 'Dataset',
  props: {
    // 这里接受父组件传过来的数据，如果isDialog为true，则为弹窗
    isDialog: Boolean
  },
  computed: {
  },
  filters: {
    // 过滤器中this指向的不是vue实例，所以无法直接获取data中的数据
    profileTypeTrans (type) {
      const obj = profileStatus.find(item => item.type === type)
      return obj ? obj.name : null
    }
  },
  data () {
    return {
      // 数据集表单
      datasetData: [],
      profileStatus,
      progress: 0,
      queryProgressVisible: false,
      huFea: true
    }
  },
  created () {
    this.getDatasetInfo()
  },
  methods: {
    // 获取数据集信息
    getDatasetInfo () {
      datasetApi.queryHuFea(this.huFea).then(response => {
        const resp = response.data
        if (resp.meta.code === 200) {
          this.$message.success('加载数据集成功')
          this.datasetData = resp.data
        }
        console.log(this.datasetData)
      })
    },
    // 发送给父组件，特征
    clickCurrentChange (currentRow) {
      this.$emit('dataset-choose', currentRow)
    },
    // 根据id下载数据集
    handleDownLoadFile (rowId) {
      console.log(rowId)
      datasetApi.downloadFile(rowId).then(response => {
        console.log(response)
        const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }))
        const link = document.createElement('a')
        link.style.display = 'none'
        link.href = url
        link.setAttribute('download', rowId + '.csv')
        document.body.appendChild(link)
        link.click()
        // const resp = response.data
      })
    },
    // 下载分析文件
    handleDownLoadProfile (row) {
      console.log(row)
      if (row.profile_state === '2') {
        datasetApi.downloadProfile(row.dataset_id).then(response => {
          console.log(response)
          const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }))
          const link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          link.setAttribute('download', row.dataset_id)
          document.body.appendChild(link)
          link.click()
        // const resp = response.data
        })
      } else {
        return this.$message.error('未分析完成，不能下载')
      }
    },
    // 删除按钮，删除数据集
    handleDelete (rowId) {
      console.log(rowId)
      this.$confirm('此操作将永久删除该数据集, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        datasetApi.deleteData(rowId).then(response => {
          console.log(12)
          this.$message.success('删除成功')
          this.getDatasetInfo()
        })
      }).catch(error => {
        this.$message.info('已取消删除')
        return error
      })
    },
    // 查看分析任务进度
    taskProgress (rowId) {
      if (rowId) {
        this.queryProgressVisible = true
        datasetApi.searchProgress(rowId).then(response => {
          console.log(response)
          const resp = response.data.data
          this.progressStatus = resp.state
          this.progress = resp.progress
        })
      } else {
        this.$message.error('数据集未进行分析')
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

</style>
