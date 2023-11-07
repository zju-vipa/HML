<template>
  <div>
    <!-- 标题 -->
    <div>
      <el-col :span="2">
        <el-button class="backbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left" style="font-size: 16px">返回</el-button>
      </el-col>
      <el-col :span="22">
        <h1>待处理学习器</h1>
      </el-col>
    </div>
    <div>
      <el-card>
        <!-- 任务信息 -->
        <div style="font-size: 20px"><h3>学习器信息</h3></div>
        <el-form label-position="right" label-width="150px" :model="learnerInfo">
          <el-row>
            <el-col :span="10">
              <el-form-item prop="learner_name">
              <template slot="label"><div class="label" style="font-size: 20px">学习器名称</div></template>
                <el-input disabled  v-model="learnerInfo.learner_name" style="width: 200px"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item prop="learner_type">
              <template slot="label"><div class="label" style="font-size: 20px">学习器类型</div></template>
                <el-select disabled v-model="learnerInfo.learner_type" placeholder="学习器类型" style="width: 200px">
                  <el-option v-for="(option, index) in learnerTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>
                </el-select>
                <!-- <el-input disabled  v-model="learnerInfo.learner_type" style="width: 200px"></el-input> -->
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <el-form-item prop="pn_job_name">
              <template slot="label"><div class="label" style="font-size: 20px">输入动作</div></template>
                <!-- <el-input v-model="learnerInfo.learner_action" style="width: 200px"></el-input> -->
                <el-select  v-model="learnerInfo.learner_action" style="width: 200px">
                  <el-option v-for="(option, index) in netDetailInfo.action_str" :key="index" :label="option" :value="netDetailInfo.action_idx[index]"></el-option>
                  <!-- <el-option v-for="count in 106" :key="count-1" :label="count-1">{{((count-1)/2)}}号发电机调至{{((count-1)%2)? '0.5':'1.4'}}</el-option> -->
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-button class="dealBtn" type="primary" @click="submitAction" style="font-size: 20px">提交动作</el-button>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
      <el-card>
        <!-- 任务信息 -->
        <el-row style="font-size: 28px; margin-bottom: 30px">
          <el-col :span="3" align="right">
            <div class="currerntTask"> 当前任务： </div>
          </el-col>
          <el-col :span="20" align="center">
            <div class="currerntTaskRange"> 在满足安全约束的情况下调整目标断面功率到指定范围内 </div>
          </el-col>
        </el-row>
        <el-row style="font-size: 22px; margin-bottom: 30px">
          <el-col class = "Power" :span="8" align="center">
            <el-row class = "sectionPower">目标断面当前功率为：{{ formatValues(netDetailInfo.target_sec_pair[0][1]) }}</el-row>
            <el-row class = "sectionPower">目标断面目标功率为：{{ formatValues(netDetailInfo.target_sec_pair[0][2]) }}</el-row>
            <el-row class = "sectionPower">约束断面功率下界为：{{ formatValues(netDetailInfo.sec_pair[0][2]) }}</el-row>
            <el-row class = "sectionPower">约束断面功率上界为：{{ formatValues(netDetailInfo.sec_pair[0][3]) }}</el-row>
          </el-col>
          <el-col class = "Power" :span="6" align="center">
            <el-row class = "basicGenPower">平衡机Gen1A-4当前功率为：{{ formatValues(netDetailInfo.balance_pair[0][1]) }}</el-row>
            <el-row class = "basicGenPower">平衡机Gen1A-4功率下界为：{{ formatValues(netDetailInfo.balance_pair[0][2]) }}</el-row>
            <el-row class = "basicGenPower">平衡机Gen1A-4功率上界为：{{ formatValues(netDetailInfo.balance_pair[0][3]) }}</el-row>
          </el-col>
          <el-col class = "Power" :span="6" align="center">
            <el-row class = "basicGenPower">平衡机Gen2E-7当前功率为：{{ formatValues(netDetailInfo.balance_pair[1][1]) }}</el-row>
            <el-row class = "basicGenPower">平衡机Gen2E-7功率下界为：{{ formatValues(netDetailInfo.balance_pair[1][2]) }}</el-row>
            <el-row class = "basicGenPower">平衡机Gen2E-7功率上界为：{{ formatValues(netDetailInfo.balance_pair[1][3]) }}</el-row>
          </el-col>
        </el-row>
        <el-row style="font-size: 28px; margin-bottom: 30px">
          危险预警：
        </el-row>
        <el-row style="font-size: 28px; margin-bottom: 30px">
          <el-row style="height:200px; border: 2px solid black; text-align: center; list-style: none; overflow-y: auto; z-index: 999;">
            <el-row v-if="netDangerWarnInfo.length!=0" >
              <el-col :span="8" v-for="(item,id) in netDangerWarnInfo" :key="id">{{ item }}</el-col>
            </el-row>
            <el-row v-else>
              无危险信息
            </el-row>
          </el-row>
        </el-row>
        <el-row style="font-size: 28px; margin-bottom: 30px">
          <div @click="previewBig" style="width: 100%; height: 100%;">
            <pdf ref="pdf" :src= "pdfurl"> </pdf>
          </div>
        </el-row>
      </el-card>
      <el-card>
        <el-row style="margin-bottom: 30px">
          <el-col :span="12" align="center">
            <el-row class="fakeTableLabel">母线电压</el-row>
            <el-row style="font-size: 18px; margin: 0 10px;">
              <el-row style="height:500px; border:1px solid #ebeef5; overflow-y: auto; z-index: 10;">
                <el-col :span="6" align="center" v-for="(item,id) in netDetailInfo.v_pair" :key="id" style="list-style: none; min-width: 180px;">
                  <li>
                    <div class="box" :style="cellStyleV(item)">
                      <el-row style="height: 30px; line-height: 30px"> {{ item[0] }} </el-row>
                      <el-row style="height: 30px; line-height: 30px"> {{ formatValues(item[1]) }} </el-row>
                    </div>
                  </li>
                </el-col>
              </el-row>
            </el-row>
          </el-col>
          <el-col :span="12" align="center">
            <el-row class="fakeTableLabel">线路功率</el-row>
            <el-row style="font-size: 18px; margin: 0 10px;">
              <el-row style="height:500px; border:1px solid #ebeef5; overflow-y: auto; z-index: 10;">
                <el-col :span="6" align="center" v-for="(item,id) in netDetailInfo.line_pair" :key="id" style="list-style: none; min-width: 180px;">
                  <li>
                    <div class="box" :style="cellStyleLine(item)">
                      <el-row style="height: 30px; line-height: 30px"> {{ item[0] }} </el-row>
                      <el-row style="height: 30px; line-height: 30px"> {{ formatValues(item[1]) }} </el-row>
                    </div>
                  </li>
                </el-col>
              </el-row>
            </el-row>
          </el-col>
        </el-row>
        <el-row style="margin-bottom: 30px">
          <el-col align="center">
            <el-row class="fakeTableLabel">发电机功率</el-row>
            <el-row style="font-size: 18px; margin: 0 10px;">
              <el-row style="height:500px; border:1px solid #ebeef5; overflow-y: auto; z-index: 10;">
                <el-col :span="4" align="center" v-for="(item,id) in netDetailInfo.gen_pair" :key="id" style="list-style: none; min-width: 180px;">
                  <li>
                    <div class="box" :style="cellStyleGen(item)">
                      <el-row style="height: 30px; line-height: 30px"> {{ item[0] }} </el-row>
                      <el-row style="height: 30px; line-height: 30px"> {{ formatValues(item[1]) }} </el-row>
                    </div>
                  </li>
                </el-col>
              </el-row>
            </el-row>
          </el-col>
        </el-row>
      </el-card>

      <el-dialog :visible.sync="pdfDialogVisible" width="200%" custom-class="magnifer-dialog">
        <div ref="printContent" class="magnifer">
          <pdf ref="pdf" :src= "pdfurl"> </pdf>
        </div>
        <!-- <span slot="footer" class="dialog-footer">
          <el-button @click="">取消</el-button>
        </span> -->
      </el-dialog>
    </div>
  </div>
</template>
<script>
import learnApi from './../../api/learn'
// 学习器类型
import pdf from 'vue-pdf'
// import CMapReaderFactory from 'vue-pdf/src/CMapReaderFactory.js'

const learnerTypeOptions = [
  { type: 'Manual', name: '人工' },
  { type: 'Machine', name: '自动化' },
  { type: 'HumanInLoop', name: '人在回路' }
]

// netDetailInfo有哪些列
const netDetailInfoColumns = {
  action_idx: ['index'],
  action_str: ['actionInfo'],

  v_pair: ['name', 'voltage', 'voltageLowerLimit', 'voltageHighLimit', 'voltageInfo'],
  v_str: ['dangerInfo'],

  balance_pair: ['name', 'power', 'powerLowerLimit', 'powerHighLimit', 'powerInfo'],
  balance_str: ['dangerInfo'],

  line_pair: ['name', 'power'],
  line_str: ['dangerInfo'],

  gen_pair: ['name', 'power', 'powerLowerLimit', 'powerHighLimit', 'powerInfo'],
  gen_str: ['dangerInfo'],

  sec_pair: ['name', 'power', 'powerLowerLimit', 'powerHighLimit', 'powerInfo'],
  sec_str: ['dangerInfo'],

  target_sec_pair: ['name'],
  target_sec_str: ['dangerInfo']
}
export default {
  components: {
    pdf
  },
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
      netDetailInfo: {
        action_idx: '',
        action_str: '',
        balance_pair: '',
        balance_str: '',
        gen_pair: '',
        gen_str: '',
        line_pair: '',
        line_str: '',
        sec_pair: '',
        sec_str: '',
        target_sec_pair: '',
        target_sec_str: '',
        v_pair: '',
        v_str: ''
      },
      gen_min: 0,
      gen_max: 0,
      line_min: 0,
      line_max: 0,
      v_min: 0,
      v_max: 0,
      netDangerWarnInfo: '',
      netDetailInfoColumns,
      submitActionForm: {},
      learnerTypeOptions,
      actionOptions: [],
      pdfurl: '',
      // pdfurl: 'http://10.82.29.169:8080/case300.pdf',
      // pdfurl: require('@/assets/case300.pdf'),
      // pdfurl: 'http://10.82.29.169:8080/case300.pdf',
      // pdfurl: 'http://10.82.29.169:8030/case300.pdf',
      // pdfurl: `${window.location.origin}/case300.pdf`,
      // pdfurl: './case300.pdf',
      // pdfurl: './../../assets/img/case300.pdf',
      // pdfSrc: '',
      pdfDialogVisible: false
    }
  },
  created () {
    console.log(`${window.location.origin}`)
    this.pdfurl = 'http://' + document.location.host + '/case300.pdf'
    // this.getTitlePdf()
    this.setActionOptions()
    this.getDangerWarnInfo(this.$route.query.learnerId)
    this.getLearnerInfo(this.$route.query.learnerId)
  },
  methods: {
    // getTitlePdf () {
    //   console.log('getTitlePdf')
    //   this.pdfSrc = pdf.createLoadingTask(this.pdfurl)
    //   console.log('this.pdfSrc: ', this.pdfSrc)
    //   // this.pdfSrc.promise.then(pdf => {
    //   //   this.numPages = pdf.numPages
    //   // })
    // },
    // 弹出大pdf对话框
    previewBig () {
      console.log('previewBig')
      this.pdfDialogVisible = true
    },
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
    // 获得危险警告信息
    getDangerWarnInfo (learnerId) {
      console.log('getDangerWarnInfo')
      learnApi.queryDangerWarnInfo(learnerId).then(response => {
        const resp = response.data
        if (resp.meta.code === 200) {
          this.netDangerWarnInfo = resp.data.dangerInfo
        }
      })
    },
    getLearnerInfo (learnerId) {
      console.log('getLearnerInfo:', learnerId)
      learnApi.queryActionDetail(learnerId).then(response => {
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
          // this.netDetailInfo = resp.data.detail
          this.netDetailInfo.action_idx = resp.data.detail.action_idx
          this.netDetailInfo.action_str = resp.data.detail.action_str
          this.netDetailInfo.balance_pair = resp.data.detail.balance_pair
          this.netDetailInfo.balance_str = resp.data.detail.balance_str
          this.netDetailInfo.gen_pair = resp.data.detail.gen_pair
          this.netDetailInfo.gen_str = resp.data.detail.gen_str
          this.netDetailInfo.line_pair = resp.data.detail.line_pair
          this.netDetailInfo.line_str = resp.data.detail.line_str
          this.netDetailInfo.sec_pair = resp.data.detail.sec_pair
          this.netDetailInfo.sec_str = resp.data.detail.sec_str
          this.netDetailInfo.target_sec_pair = resp.data.detail.target_sec_pair
          this.netDetailInfo.target_sec_str = resp.data.detail.target_sec_str
          this.netDetailInfo.v_pair = resp.data.detail.v_pair
          this.netDetailInfo.v_str = resp.data.detail.v_str
          console.log('this.netDetailInfo:', this.netDetailInfo)
          // console.log(this.netDetailInfo)
          console.log(this.netDetailInfo.target_sec_pair)
          console.log(typeof this.netDetailInfo.target_sec_pair)
          console.log(this.netDetailInfo.target_sec_pair[0])
          console.log(this.netDetailInfo.target_sec_pair[0][1])
          console.log(this.netDetailInfo.target_sec_pair[0][2])
          let genMin = 999
          let lineMin = 999
          let vMin = 999
          let genMax = -999
          let lineMax = -999
          let vMax = -999
          this.netDetailInfo.v_pair.forEach(item => {
            if (item[1] < vMin) {
              vMin = item[1]
            }
            if (item[1] > vMax) {
              vMax = item[1]
            }
          })
          this.netDetailInfo.line_pair.forEach(item => {
            if (item[1] < lineMin) {
              lineMin = item[1]
            }
            if (item[1] > lineMax) {
              lineMax = item[1]
            }
          })
          this.netDetailInfo.gen_pair.forEach(item => {
            if (item[1] < vMin) {
              genMin = item[1]
            }
            if (item[1] > vMax) {
              genMax = item[1]
            }
          })
          this.gen_min = genMin
          this.gen_max = genMax
          this.line_min = lineMin
          this.line_max = lineMax
          this.v_min = vMin
          this.v_max = vMax
        }
      })
    },
    // 提交动作
    submitAction () {
      this.submitActionForm = {
        learner_id: this.learnerInfo.learner_id,
        learner_action: parseInt(this.learnerInfo.learner_action)
      }
      console.log('learner_action: ', this.submitActionForm.learner_action)
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
    formatValues (cellValue) {
      if (cellValue === null) {
        return 'null'
      }
      return parseFloat(cellValue).toFixed(3)
    },
    // 根据级别显示颜色
    cellStyleLine (item) {
      console.log(item)
      const v = 255 - Math.floor((item[1] - this.line_min) * 200 / (this.line_max - this.line_min))
      const color = 0xff0000 + (v << 8) + v
      return `background:#${color.toString(16)}`
    },
    cellStyleV (item) {
      const v = 255 - Math.floor((item[1] - this.v_min) * 200 / (this.v_max - this.v_min))
      const color = 0xff0000 + (v << 8) + v
      return `background:#${color.toString(16)}`
    },
    cellStyleGen (item) {
      const v = 255 - Math.floor((item[1] - this.gen_min) * 200 / (this.gen_max - this.gen_min))
      const color = 0xff0000 + (v << 8) + v
      return `background:#${color.toString(16)}`
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
  h1{
     text-align: center;
  }
  h2{
     text-align: center;
  }
  h3{
    padding-bottom: 10px;
    border-bottom: 3px solid rgb(180, 180, 180);
  }
  h4{
    padding-bottom: 10px;
    /* border-bottom: 2px solid rgb(102, 102, 102) */
  }
  .currerntTask{
    height: 60px;
    line-height: 60px;
  }
  .currerntTaskRange{
    width: 1000px;
    height: 60px;
    line-height: 60px;
    border: 2px solid black;
  }
  .Power{
    margin: 0 20px 0 20px;
    height: 160px;
    border: 2px solid black;
  }
  .sectionPower{
    height: 30px;
    margin: 8px 0 8px 0;
  }
  .basicGenPower{
    height: 40px;
    margin: 10px 0 10px 0;
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
  .box{
    height:60px;
    border-right: 1px solid #ebeef5;
    border-bottom: 1px solid #EBEEF5;
    text-align: center;
    padding: 12px 0;
  }
  .fakeTableLabel{
    font-size: 28px;
    border: 1px solid #ebeef5;
    height:60px;
    line-height: 60px ;
    margin: 0 10px;
  }
</style>
