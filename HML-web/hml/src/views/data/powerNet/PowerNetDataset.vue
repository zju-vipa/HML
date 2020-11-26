<template>
  <div>
    <!-- 标题 -->
    <div>
      <el-col :span="2">
        <el-button class="backbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
      </el-col>
      <el-col :span="22">
        <h2>电网数据集</h2>
      </el-col>
    </div>
    <div>
      <!-- 统计任务进度 -->
      <el-card>
        <div><h3>电网数据集生成进度</h3></div>
        <el-row align="middle" style="margin-bottom: 30px" :gutter="20">
          <el-col align="center" :span="10">
            <el-progress type="circle" :percentage="powerNetJobCnt==0 ? 0 : powerNetJobDoneCnt/powerNetJobCnt*100"></el-progress>
          </el-col>
          <el-col :span="10">
            <div><h4>全部：  {{powerNetJobCnt}}</h4></div>
            <div><h4>已完成：{{powerNetJobDoneCnt}}</h4></div>
            <div><h4>未完成：{{powerNetJobUndoneCnt}}</h4></div>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="createPowerNetDataset">创建新任务</el-button>
          </el-col>
        </el-row>
      </el-card>
      <!-- 已有电网拓扑 -->
      <el-card>
        <div><h3>已有电网拓扑</h3></div>
        <el-row align="middle" style="margin-bottom: 30px">
          <!-- 暂时先随便放一下图片 -->
          <img src="@/assets/img/logo.png">
        </el-row>
      </el-card>
      <!-- 任务列表 -->
      <el-card>
        <div><h3>数据生成任务列表</h3></div>
        <el-table :data="powerNetData" border stripe  style="width: 100%">
          <el-table-column  label="序号" type="index"> </el-table-column>
          <el-table-column prop="job_name" label="任务名称"> </el-table-column>
          <el-table-column prop="creator" label="创建者"> </el-table-column>
          <el-table-column prop="start_time" label="开始时间"> </el-table-column>
          <el-table-column prop="is_done" label="状态">
            <template slot-scope="scope">{{scope.row.is_done | applyJobStatusTrans}}</template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button style="width:140px" size="mini" plain type="primary" :disabled="scope.row.is_done==false"
                @click="queryPowerNetResult(scope.row.job_id)" icon="el-icon-search">查看结果</el-button>
              <!-- <el-button size="mini" plain type="danger"
                @click="handleDelete(scope.row.decision_id)" icon="el-icon-delete">删除</el-button> -->
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>
<script>
import queryPowerNetApi from './../../../api/queryPowerNet'
export default {
  filters: {
    // is_done转换成 “已完成” “未完成”
    applyJobStatusTrans (type) {
      return type ? '已完成' : '未完成'
    }
  },
  data () {
    return {
      // 电网数据生成任务列表
      powerNetData: [],
      // 全部任务数，已完成任务数，未完成任务数 (异步)
      powerNetJobCnt: 0,
      powerNetJobDoneCnt: 0,
      powerNetJobUndoneCnt: 0
    }
  },
  created () {
    this.getPowerNetInfo()
  },
  methods: {
    // 获取电网数据生成任务所有信息
    getPowerNetInfo () {
      queryPowerNetApi.query().then(response => {
        console.log(response)
        const resp = response.data
        if (resp.meta.code === 200) {
          this.$message.success('加载电网数据集成功')
          this.powerNetData = resp.data
          // 统计数量
          this.powerNetJobCnt = response.data.list.length
          this.powerNetJobDoneCnt = response.data.list.filter(item => {
            return item.isDone === true
          }).length
          this.powerNetJobUndoneCnt = this.powerNetJobCnt - this.powerNetJobDoneCnt
        }
      })
    },
    createPowerNetDataset () {
      this.$router.push('/data/powerNetDatasetCreate')
    },
    // 查看电网数据生成任务结果
    queryPowerNetResult (rowId) {
      console.log(rowId)
      this.$router.push({ path: '/data/queryPowerNetResult', query: { jobId: rowId } })
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
     margin-left: 20px;
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
  .el-col{
    min-height: 1px;
  }
  .el-form-item{
  margin-bottom: 30px;
  }
</style>
