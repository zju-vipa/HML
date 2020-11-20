<template>
  <div>
    <el-card>
      <!-- 标题 -->
      <h3>电网数据生成任务结果</h3>
      <div>
        <el-button class="opbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
      </div>
      <div>
        <!-- 任务信息 -->
        <el-form label-position="right" label-width="150px" :model="powerNetJobInfo">
          <el-row>
            <el-col :span="10">
              <el-form-item label="任务名称" prop="pn_job_name">
                <el-input disabled  v-model="powerNetJobInfo.pn_job_name" style="width: 300px"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item label="生成方式" prop="pn_job_type">
                <el-select disabled v-model="powerNetJobInfo.pn_job_type" style="width: 300px">
                  <el-option v-for="(option, index) in generateTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
              <el-col :span="20">
              <el-form-item label="任务描述" prop="pn_job_description">
                <el-input disabled  v-model="powerNetJobInfo.pn_job_description" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <!-- 初始电网信息 -->
        <el-form label-position="right" label-width="150px" :model="initPowerNetInfo">
          <el-row>
            <el-col :span="10">
              <el-form-item label="样例名称" prop="init_net_name">
                <el-select disabled v-model="initPowerNetInfo.init_net_name" style="width: 300px">
                  <el-option v-for="(option, index) in initNetOptions" :key="index" :label="option.name" :value="option.type"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
              <el-col :span="20">
              <el-form-item label="样例描述" prop="init_net_description">
                <el-input disabled v-model="initPowerNetInfo.init_net_description" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <!-- 初始电网统计信息 -->
        <el-table border stripe style="width: 100%">
          <el-col :span="6">
              <el-row>母线数量</el-row>
              <el-row>0</el-row>
          </el-col>
          <el-col :span="6">
              <el-row>负荷数量</el-row>
              <el-row>0</el-row>
          </el-col>
          <el-col :span="6">
              <el-row>电机数量</el-row>
              <el-row>0</el-row>
          </el-col>
          <el-col :span="6">
              <el-row>线路数量</el-row>
              <el-row>0</el-row>
          </el-col>
        </el-table>
      </div>
      <h4>潮流计算结果</h4>
      <el-table :data="powerFlowResultData" border stripe  style="width: 100%">
        <el-table-column  label="序号" type="index"> </el-table-column>
        <el-table-column prop="position" label="扰动位置"> </el-table-column>
        <el-table-column prop="value_before" label="扰动前"> </el-table-column>
        <el-table-column prop="value_after" label="扰动后"> </el-table-column>
        <el-table-column prop="convergence" label="收敛情况"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>
<script>
import queryPowerNetApi from './../../../api/queryPowerNet'
// 生成方式类型
const generateTypeOptions = [
  { type: 'A', name: '方式A' },
  { type: 'B', name: '方式B' },
  { type: 'C', name: '方式C' }
]
// 样例名称
const initNetOptions = [
  { type: 'c18', name: 'c18' },
  { type: 'c39', name: 'c39' },
  { type: 'c54', name: 'c54' }
]
export default {
  filters: {
    // is_done转换成 “已完成” “未完成”
    applyJobStatusTrans (type) {
      return type ? '已完成' : '未完成'
    }
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
      powerNetJobInfo: {
        pn_job_id: '',
        pn_job_name: '',
        pn_job_type: 'A',
        pn_job_description: '略'
      },
      // 初始电网样例名称，描述，网络结构，拓扑图
      initPowerNetInfo: {
        init_net_name: '',
        init_net_description: '',
        init_net_data: [],
        init_net_topo_url: ''
      },
      // 调整参数
      // to do
      // 潮流计算结果
      powerFlowResultData: [],
      generateTypeOptions,
      initNetOptions
    }
  },
  created () {
    this.getPowerNetJobInfo(this.$route.query.jobId)
  },
  methods: {
    // 根据id获取电网数据生成任务信息
    getPowerNetJobInfo (jobId) {
      queryPowerNetApi.queryJob(jobId).then(response => {
        console.log(response)
        const resp = response.data
        if (resp.meta.code === 200) {
          this.$message.success('加载任务信息成功')
          // to do
        //   this.powerNetData = resp.data
        //   // 统计数量
        //   this.powerNetJobCnt = response.data.list.length
        //   this.powerNetJobDoneCnt = response.data.list.filter(item => {
        //     return item.isDone === true
        //   }).length
        //   this.powerNetJobUndoneCnt = this.powerNetJobCnt - this.powerNetJobDoneCnt
        }
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
  .el-form-item{
  margin-bottom: 30px;
  }
</style>
