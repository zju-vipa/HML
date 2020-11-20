<template>
  <div>
    <el-card>
      <!-- 标题 -->
      <h3>电网数据集</h3>
      <div>
        <el-button class="opbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
      </div>
      <div>
        <!-- 统计进度 -->
        <el-row>
          <el-col span="1"></el-col>
          <el-col span="22" style="border-bottom: 3px solid rgb(180, 180, 180); margin-bottom: 10px">
            <el-row><h4>电网数据集生成进度</h4></el-row>
            <el-row align="middle" style="margin-bottom: 30px">
              <el-col align="center" span="12">
                <el-progress type="circle" :percentage="powerNetJobCnt==0 ? 0 : powerNetJobDoneCnt/powerNetJobCnt*100"></el-progress>
              </el-col>
              <el-col span="12">
                <div><h5>全部：  {{powerNetJobCnt}}</h5></div>
                <div><h5>已完成：{{powerNetJobDoneCnt}}</h5></div>
                <div><h5>未完成：{{powerNetJobUndoneCnt}}</h5></div>
              </el-col>
            </el-row>
          </el-col>
          <el-col span="1"></el-col>
        </el-row>
        <!-- 已有电网拓扑 -->
        <el-row>
          <el-col span="1"></el-col>
          <el-col span="22" style="border-bottom: 3px solid rgb(180, 180, 180); margin-bottom: 10px">
            <el-row><h4>已有电网拓扑</h4></el-row>
            <el-row align="middle" style="margin-bottom: 30px">
              <!-- 暂时先随便放一下图片 -->
              <img src="@/assets/logo.png">
            </el-row>
          </el-col>
          <el-col span="1"></el-col>
        </el-row>
        <!-- 任务列表 -->
        <el-row>
          <el-col span="1"></el-col>
          <el-col span="22" style="margin-bottom: 10px">
            <el-row>
              <el-col span="18"><h4>数据生成任务列表</h4></el-col>
              <el-col span="6" style="margin-top: 20px">
                <el-button class="optbtn" size="mini"
                  type="primary" @click="createPowerNetDataset">创建新任务</el-button>
              </el-col>
            </el-row>
          </el-col>
          <el-col span="1"></el-col>
        </el-row>
      </div>
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
/* .queryBtn {
  margin-bottom: 20px;
} */
  /* h3{
    text-align: center;
  } */
  .el-card{
    margin: 10px 20px;
  }
  h3{
    padding-bottom: 10px;
    border-bottom: 3px solid rgb(102, 102, 102)
  }
  h4{
    padding-bottom: 10px;
    /* border-bottom: 2px solid rgb(102, 102, 102) */
  }
  .opbtn{
    margin-bottom: 10px;
  }
  .el-col{
    min-height: 1px;
  }
</style>
