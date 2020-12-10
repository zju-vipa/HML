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
        <el-row align="center" style="margin-bottom: 30px" :gutter="20">
          <el-col align="center" :span="6">
            <el-progress :format="format1" type="circle" stroke-width="12" width="200" color="#8e71c7"
            :percentage="1+powerNetJobDoneCnt">
            </el-progress>
          </el-col>
          <el-col align="center" :span="6">
            <el-progress :format="format2" type="circle" stroke-width="12" width="200" color="#f36838"
            :percentage="1+powerNetJobUndoneCnt"></el-progress>
          </el-col>
          <el-col align="center" :span="6">
            <el-progress :format="format3" type="circle" stroke-width="12" width="200" color="#21a675"
            :percentage="powerNetJobCnt==0 ? 0 : parseFloat(powerNetJobDoneCnt/powerNetJobCnt*100).toFixed(1)"></el-progress>
          </el-col>
          <!-- <el-col :span="5">
            <div><h4>全部：  {{powerNetJobCnt}}</h4></div>
            <div><h4>已完成：{{powerNetJobDoneCnt}}</h4></div>
            <div><h4>未完成：{{powerNetJobUndoneCnt}}</h4></div>
          </el-col> -->
          <el-col align="center" :span="6">
            <el-button type="primary" @click="createPowerNetDataset">创建新任务</el-button>
          </el-col>
        </el-row>
      </el-card>
      <!-- 已有电网拓扑 -->
      <el-card>
        <div><h3>已有电网拓扑</h3></div>
        <el-row align="center" :gutter="20">
          <div v-for="(item, index) in initNetOptions" :key="index" :value="item" style="list-style: none;">
            <li>
              <el-col align="center" :span="6">
                <el-button class="netbtn" plain type="info">{{item}}</el-button>
                <!-- <h4>{{item}}</h4> -->
              </el-col>
            </li>
          </div>
        </el-row>
      </el-card>
      <!-- 任务列表 -->
      <el-card>
        <div><h3>数据生成任务列表</h3></div>
        <el-table :data="powerNetData" border stripe  style="width: 100%">
          <el-table-column  label="序号" type="index"> </el-table-column>
          <el-table-column prop="power_net_dataset_name" label="任务名称"> </el-table-column>
          <el-table-column prop="username" label="创建者"> </el-table-column>
          <el-table-column width="300" prop="start_time" label="开始时间"> </el-table-column>
          <el-table-column prop="generate_state" label="状态">
            <template slot-scope="scope">{{scope.row.generate_state | generateStateTrans}}</template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button  size="mini"  :disabled="scope.row.is_done==false"
                @click="queryPowerNetResult(scope.row.power_net_dataset_id)" icon="el-icon-search">查看结果</el-button>
              <el-button  size="mini" plain type="danger"
                @click="handleDelete(scope.row.power_net_dataset_id)" icon="el-icon-delete">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>
<script>
import queryPowerNetApi from './../../../api/queryPowerNet'
// 任务状态
const generateStateOptions = [
  { type: '0', name: '未开始' },
  { type: '1', name: '正在生成' },
  { type: '2', name: '已完成' },
  { type: '3', name: '生成失败' }
]
// 样例名称
const initNetOptions = ['case5', 'case9', 'case14', 'case30', 'case_ieee30', 'case39', 'case57', 'case118', 'case300']
export default {
  // name: 'Dataset',
  // props: {
  //   // 这里接受父组件传过来的数据，如果isDialog为true，则为弹窗
  //   isDialog: Boolean
  // },
  // computed: {
  // },
  filters: {
    // generate_state转换成文字
    generateStateTrans (type) {
      const obj = generateStateOptions.find(item => item.type === type)
      return obj ? obj.name : null
    }
  },
  data () {
    return {
      // 电网数据生成任务列表
      powerNetData: [],
      // 全部任务数，已完成任务数，未完成任务数 (异步)
      powerNetJobCnt: 0,
      powerNetJobDoneCnt: 0,
      powerNetJobUndoneCnt: 0,
      initNetOptions,
      timer: null
    }
  },
  created () {
    this.getPowerNetInfo()
    this.timer = setInterval(() => {
      this.getPowerNetInfo()
    }, 1000)
  },
  // mounted () {
  //   if (this.timer) {
  //     clearInterval(this.timer)
  //   } else {
  //     this.timer = setInterval(() => {
  //       this.getPowerNetInfo()
  //     }, 5000)
  //   }
  // },
  destroyed () {
    clearInterval(this.timer)
  },
  methods: {
    // 获取电网数据生成任务所有信息
    getPowerNetInfo () {
      queryPowerNetApi.query().then(response => {
        console.log(response)
        const resp = response.data
        if (resp.meta.code === 200) {
          // this.$message.success('加载电网数据集成功')
          this.powerNetData = resp.data
          // 统计数量
          this.powerNetJobCnt = resp.data.length
          this.powerNetJobDoneCnt = resp.data.filter(item => {
            return item.generate_state === '2'
          }).length
          this.powerNetJobUndoneCnt = this.powerNetJobCnt - this.powerNetJobDoneCnt
          // console.log(this.powerNetJobCnt)
          // console.log(this.powerNetJobDoneCnt)
        }
      })
    },
    createPowerNetDataset () {
      this.$router.push('/data/powerNetDatasetCreate')
    },
    // 查看电网数据生成任务结果
    queryPowerNetResult (pnId) {
      console.log(pnId)
      this.$router.push({ path: '/data/queryPowerNetResult', query: { jobId: pnId } })
    },
    // 删除数据集
    handleDelete (pnId) {
      console.log(pnId)
      this.$confirm('此操作将永久删除该电网数据集, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        queryPowerNetApi.deletePowerNetDataset(pnId).then(response => {
          // console.log(12)
          this.$message.success('删除成功')
          this.getPowerNetInfo()
        })
      }).catch(error => {
        this.$message.info('已取消删除')
        return error
      })
    },
    format1 () {
      return `已完成：${this.powerNetJobDoneCnt}`
    },
    format2 () {
      return `未完成：${this.powerNetJobUndoneCnt}`
    },
    format3 (percentage) {
      return `进度：${percentage}%`
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
  .netbtn{
    margin-top: 20px;
    margin-left: 20px;
    width: 200px;
  }
  .progressNum{
    font-size: 20px;
  }
  .progressName{
    font-size: 10px;
  }
</style>
