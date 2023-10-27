<template>
  <div>
    <div>
      <!-- 功能模块 -->
      <el-row align="center" style="margin-bottom: 30px" :gutter="5">
        <el-col align="center" :span="6">
          <el-card style="height: 600px;">
            <div><h3>功能模块</h3></div>
            <el-row align="center" style="margin-top:60px;margin-bottom: 60px" :gutter="20">
              <el-button @click="gotoDatasetUpload" type="primary" circle>数据导入与上传</el-button>
            </el-row>
            <el-row align="center" style="margin-top:60px;margin-bottom: 30px" :gutter="20">
              <el-button @click="gotoPowerNetDataset" type="primary" circle>电网数据生成</el-button>
            </el-row>
            <el-row align="center" style="margin-top:60px;margin-bottom: 30px" :gutter="20">
              <el-button @click="gotoDatasetList" type="primary" circle>数据查看</el-button>
            </el-row>
          </el-card>
        </el-col>
        <el-col align="center" :span="18">
          <!-- 信息汇总 -->
          <el-card style="height: 600px;">
            <div><h3>信息汇总</h3></div>
            <el-row align="center" style="margin-top:20px;margin-bottom:30px; height:220px;" :gutter="20">
              <el-col align="center" :span="8">
                <el-card shadow="hover" :body-style="{padding:'0'}" style="border: 0px; min-height:200px; background-color: rgb(234, 235, 235);">
                  <el-row style="margin-top: 30px;margin-bottom: 0px; height: 100px;" :gutter="2">
                    <el-col :span="5"></el-col>
                    <el-col align="center" :span="10" style="margin-top: 10px;font-size: 50px;">100</el-col>
                    <el-col align="start" :span="9" style="margin-top: 40px;font-size: 20px;">个</el-col>
                  </el-row>
                  <el-row align="center" style="height: 50px;">
                    <el-col align="center" :span="24" style="margin-top: 0px;font-size: 20px;">数据集总数</el-col>
                  </el-row>
                </el-card>
              </el-col>
              <el-col align="center" :span="8">
                <el-card shadow="hover" :body-style="{padding:'0'}" style="border: 0px; min-height:200px; background-color: rgb(234, 235, 235);">
                  <el-row style="margin-top: 30px;margin-bottom: 0px; height: 100px;" :gutter="2">
                    <el-col :span="5"></el-col>
                    <el-col align="center" :span="10" style="margin-top: 10px;font-size: 50px;">60</el-col>
                    <el-col align="start" :span="9" style="margin-top: 40px;font-size: 20px;">个</el-col>
                  </el-row>
                  <el-row align="center" style="height: 50px;">
                    <el-col align="center" :span="24" style="margin-top: 0px;font-size: 20px;">原始数据集</el-col>
                  </el-row>
                </el-card>
              </el-col>
              <el-col align="center" :span="8">
                <el-card shadow="hover" :body-style="{padding:'0'}" style="border: 0px; min-height:200px; background-color: rgb(234, 235, 235);">
                  <el-row style="margin-top: 30px;margin-bottom: 0px; height: 100px;" :gutter="2">
                    <el-col :span="5"></el-col>
                    <el-col align="center" :span="10" style="margin-top: 10px;font-size: 50px;">40</el-col>
                    <el-col align="start" :span="9" style="margin-top: 40px;font-size: 20px;">个</el-col>
                  </el-row>
                  <el-row align="center" style="height: 50px;">
                    <el-col align="center" :span="24" style="margin-top: 0px;font-size: 20px;">特征工程数据集</el-col>
                  </el-row>
                </el-card>
              </el-col>
            </el-row>
            <el-row align="center" style="margin-top:20px;margin-bottom:30px; height:220px;" :gutter="20">
              <el-col align="center" :span="8">
                <el-card shadow="hover" :body-style="{padding:'0'}" style="border: 0px; min-height:200px; background-color: rgb(234, 235, 235);">
                  <el-row style="margin-top: 30px;margin-bottom: 0px; height: 100px;" :gutter="2">
                    <el-col :span="5"></el-col>
                    <el-col align="center" :span="10" style="margin-top: 10px;font-size: 50px;">9</el-col>
                    <el-col align="start" :span="9" style="margin-top: 40px;font-size: 20px;">个</el-col>
                  </el-row>
                  <el-row align="center" style="height: 50px;">
                    <el-col align="center" :span="24" style="margin-top: 0px;font-size: 20px;">电网拓扑数</el-col>
                  </el-row>
                </el-card>
              </el-col>
              <el-col align="center" :span="8">
                <el-card shadow="hover" :body-style="{padding:'0'}" style="border: 0px; min-height:200px; background-color: rgb(234, 235, 235);">
                  <el-row style="margin-top: 30px;margin-bottom: 0px; height: 100px;" :gutter="2">
                    <el-col :span="5"></el-col>
                    <el-col align="center" :span="10" style="margin-top: 10px;font-size: 50px;">0</el-col>
                    <el-col align="start" :span="9" style="margin-top: 40px;font-size: 20px;">个</el-col>
                  </el-row>
                  <el-row align="center" style="height: 50px;">
                    <el-col align="center" :span="24" style="margin-top: 0px;font-size: 20px;">未完成任务</el-col>
                  </el-row>
                </el-card>
              </el-col>
              <el-col align="center" :span="8">
                <el-card shadow="hover" :body-style="{padding:'0'}" style="border: 0px; min-height:200px; background-color: rgb(234, 235, 235);">
                  <el-row style="margin-top: 30px;margin-bottom: 0px; height: 100px;" :gutter="2">
                    <el-col :span="5"></el-col>
                    <el-col align="center" :span="10" style="margin-top: 10px;font-size: 50px;">80</el-col>
                    <el-col align="start" :span="9" style="margin-top: 40px;font-size: 20px;">%</el-col>
                  </el-row>
                  <el-row align="center" style="height: 50px;">
                    <el-col align="center" :span="24" style="margin-top: 0px;font-size: 20px;">上次任务<br/>失稳样本有效率</el-col>
                  </el-row>
                </el-card>
              </el-col>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
import queryPowerNetApi from './../../api/queryPowerNet'
// 任务状态
const generateStateOptions = [
  { type: '0', name: '未开始' },
  { type: '1', name: '正在生成' },
  { type: '2', name: '已完成' },
  { type: '3', name: '生成失败' }
]

export default {
  name: 'DataManage',
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
      value1: 5,
      powerNetData: [],
      // 全部任务数，已完成任务数，未完成任务数 (异步)
      powerNetJobCnt: 0,
      powerNetJobDoneCnt: 0,
      powerNetJobUndoneCnt: 0,
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
    // createPowerNetTransientStabilityDataset () {
    //   this.$router.push('/data/powerNetTransientStabilityDatasetCreate')
    // },
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
    // 前往电网数据生成
    gotoPowerNetDataset () {
      this.$router.push('/data/powerNet')
    },
    // 前往数据导入与上传
    gotoDatasetUpload () {
      this.$router.push('/data/uploadDataset')
    },
    // 前往数据集页面
    gotoDatasetList () {
      this.$router.push('/data/originDataset')
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
    margin: 20px 20px;
  }
  .el-button {
    height: 100px;
    width: 200px;
    padding:30px;
    /* display: flex; */
    justify-content: center;
    align-items: center;
    font-size: 20px;

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

  /* .el-slider {
    .el-slider__input {
      margin-top: 0;
    }
    .el-slider__runway {
      height: 32px;
      margin-top: 0;
      margin-bottom: 0 !important;
      background-color: #FFFFFF;
      border: 1px solid #DCDFE6;
      .el-slider__bar {
        height: 31px;
      }
      .el-slider__button-wrapper {
        top: 0;
        height: 32px;
        .el-slider__button {
          width: 4px;
          height: 31px;
          border-radius: 0;
          background: #FFFFFF;
          border: solid 2px #0068A5;
        }
      }
      .el-slider__stop {
        width: 1px;
        height: 31px;
        border-radius: 0;
        background-color: #DCDFE6;
      }
      .el-slider__marks-text {
        color: #717171;
        margin-top: 0;
        transform: translateX(-115%);
      }
    }
  } */
</style>
