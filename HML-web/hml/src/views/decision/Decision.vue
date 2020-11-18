<template>
  <div>
      <!-- 面包屑区域 -->
      <!-- <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">人在回路</el-breadcrumb-item>
        <el-breadcrumb-item>决策</el-breadcrumb-item>
      </el-breadcrumb> -->
    <!-- 卡片区域 -->
    <el-card>
      <el-button class="queryBtn" @click="gotoQueryDec" type="primary">查询决策</el-button>
      <!-- <el-button class="queryBtn" disabled type="primary">应用决策</el-button>
      <el-button class="queryBtn" @click="gotoDecHumanFea" type="primary">决策特征工程</el-button>
      <el-button class="queryBtn" @click="gotoLearnDec" type="primary">决策学习器</el-button> -->
      <el-form class="choosedataset" label-position="right" label-width="150px" :model="chooseDatasetForm" ref="chooseDatasetFormRef">
        <el-row>
          <el-col :span="10">
            <el-form-item prop="dataset_name" label="选择测试集">
              <el-input clearable  readonly v-model="chooseDatasetForm.dataset_name" style="width: 300px"
                        @click.native="datasetDialogVisible=true" placeholder="请选择测试集"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="10">
            <el-form-item label="决策名" prop="learner_name">
              <el-input clearable  v-model="decideHFAndLeaForm.decision_name" placeholder="请填写决策名" style="width: 300px"></el-input>
            </el-form-item>
          </el-col>
          <!-- <el-col :span="10">
            <el-form-item label="须知">
              <el-input style="width:300px" disabled  placeholder="数据集必须是csv格式"></el-input>
            </el-form-item>
          </el-col> -->
        </el-row>
      </el-form>
      <!-- 决策类型 -->
      <el-form label-position="right" label-width="150px" :model="decideHFAndLeaForm" ref="decideHumanFeaFormRef"  class="demo-ruleForm">
        <el-row>
          <el-col :span="10">
            <el-form-item label="决策类型" prop="learner_type">
              <!-- <el-select disabled  v-model="decideHFAndLeaForm.decision_type" placeholder="决策类型" style="width: 300px">
                <el-option v-for="(option, index) in decisionTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>
              </el-select> -->
              <el-radio-group v-model="decideHFAndLeaForm.decision_type" @change="handleDecideOption">
                <el-radio :label="'Manual_D'">应用决策者</el-radio>
                <el-radio :label="'Manual_FE'">应用特征工程</el-radio>
                <el-radio :label="'Manual_L'">应用学习器</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <el-row>
          <el-col :span="10">
            <el-form class="selectHuFea" label-position="right" label-width="150px"  :model="chooseHumanFeaForm">
              <el-form-item prop="featureEng_name" label="特征工程">
                <el-input disabled="chooseFEDisabled" clearable  readonly v-model="chooseHumanFeaForm.featureEng_name" style="width: 300px"
                          @click.native="humanFeaDialogVisible=true" placeholder="请选择特征工程"></el-input>
              </el-form-item>
            </el-form>
          </el-col>
          <el-col :span="10">
            <el-form label-position="right" label-width="150px"  :model="chooseLearnerForm">
              <el-form-item prop="learner_name" label="学习器">
                <el-input disabled="chooseLearnerDisabled" clearable  readonly v-model="chooseLearnerForm.learner_name" style="width: 300px"
                          @click.native="learnerDialogVisible=true" placeholder="请选择学习器"></el-input>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>
      <!-- 决策应用特征工程加学习器部分 -->
      <!-- <el-form label-position="right" label-width="150px" :model="decideHFAndLeaForm" ref="decideHumanFeaFormRef"  class="demo-ruleForm">
        <el-row>
          <el-col :span="10">
            <el-form-item label="决策名" prop="learner_name">
              <el-input clearable  v-model="decideHFAndLeaForm.decision_name" placeholder="请填写决策名" style="width: 300px"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="10">
            <el-form-item label="决策类型" prop="learner_type">
              <el-select disabled  v-model="decideHFAndLeaForm.decision_type" placeholder="决策类型" style="width: 300px">
                <el-option v-for="(option, index) in decisionTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form> -->
      <!-- 决策应用特征工程决策参数的表单 -->
      <el-form label-position="right" label-width="150px" :model="decideHumanFeaParamForm">
        <el-row>
          <el-col :span="10">
            <el-form-item label="选择标签" prop="label">
              <el-select  v-model="decideHumanFeaParamForm.label" placeholder="选择标签" style="width: 300px">
                <el-option
                  v-for="(item,index) in columnsList" :key="index"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="10">
            <el-form-item>
              <el-button class="submitBtn" type="primary" @click="submitAllDecForm">应用决策</el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <!-- 提交所有表单  -->
    </el-card>
      <!--      选择数据集，弹出的窗口-->
    <el-dialog title="选择数据集" :visible.sync="datasetDialogVisible" @close="getColumns">
      <dataset :isDialog="true" @dataset-choose = chooseDataset></dataset>
    </el-dialog>
      <!--      选择特征工程，弹出的窗口-->
    <el-dialog title="选择特征工程" :visible.sync="humanFeaDialogVisible" @close="getColumns">
      <query-human-feature :isHFeaDialog="true" @choose-HumanFea="chooseHumanFea"></query-human-feature>
    </el-dialog>
      <!--      选择学习器，弹出的窗口-->
    <el-dialog title="选择学习器" :visible.sync="learnerDialogVisible">
      <query-learner :isLearnDialog="true" @learner-choose="chooseLearner"></query-learner>
    </el-dialog>
  </div>
</template>

<script>
import Dataset from '../data/OriginDataset'
import QueryHumanFeature from './../feature/QueryHumanFeature'
import QueryLearner from './../learn/QueryLearner'
import featureApi from './../../api/feature'
import decisionApi from './../../api/decision'
// 学习器类型
const decisionTypeOptions = [
  { type: 'Manual_FE', name: '应用特征工程' },
  { type: 'Manual_L', name: '应用学习器' },
  { type: 'Manual_D', name: '应用决策者' }
]
export default {
  name: 'Decision',
  components: {
    Dataset,
    QueryHumanFeature,
    QueryLearner
  },
  data () {
    return {
      // 选择数据集form
      chooseDatasetForm: {
        dataset_name: '',
        dataset_id: ''
      },
      datasetDialogVisible: false,
      // 决策类型
      decisionTypeOptions,
      // 选择特征工程的
      chooseHumanFeaForm: {
        featureEng_name: '',
        original_dataset_id: '',
        featureEng_id: ''
      },
      // 选择学习器的
      chooseLearnerForm: {
        learner_id: '',
        learner_name: ''
      },
      datasetId: '',
      // 决策于特征的表单
      decideHFAndLeaForm: {
        decision_name: '',
        decision_type: 'Manual_D',
        decision_parameters: {},
        featureEng_id: '',
        dataset_id: ''
      },
      decideHumanFeaParamForm: {
        label: []
      },
      // 特征工程对话框
      humanFeaDialogVisible: false,
      // 学习器对话框
      learnerDialogVisible: false,
      columnsList: [],
      // 是否禁用 选择特征工程 选择学习器
      chooseFEDisabled: false,
      chooseLearnerDisabled: false
    }
  },
  methods: {
    // 接受数据集组件传来的数据
    chooseDataset (currentRow) {
      this.chooseDatasetForm.dataset_name = currentRow.dataset_name
      this.chooseDatasetForm.dataset_id = currentRow.dataset_id
      this.datasetId = currentRow.dataset_id
      this.datasetDialogVisible = false
    },
    // 从人工特征工程传来的选中的特征工程
    chooseHumanFea (currentRow) {
      // console.log(currentRow)
      this.chooseHumanFeaForm.featureEng_name = currentRow.featureEng_name
      // this.chooseHumanFeaForm.original_dataset_id = currentRow.original_dataset_id
      this.chooseHumanFeaForm.featureEng_id = currentRow.featureEng_id
      // this.datasetId = this.chooseHumanFeaForm.original_dataset_id
      this.humanFeaDialogVisible = false
    },
    // 从学习器传来的选中的学习器
    chooseLearner (currentRow) {
      this.chooseLearnerForm.learner_id = currentRow.learner_id
      this.chooseLearnerForm.learner_name = currentRow.learner_name
      this.learnerDialogVisible = false
    },
    // 获取数据集列名
    getColumns () {
      if (this.datasetId !== '') {
        featureApi.getDatasetColumns(this.datasetId).then(response => {
          const resp = response.data
          this.columnsList = resp.data
        // console.log(this.columnsList)
        })
      }
    },
    // 提交决策
    submitAllDecForm () {
      this.decideHFAndLeaForm.dataset_id = this.datasetId
      this.decideHFAndLeaForm.decision_parameters = this.decideHumanFeaParamForm
      this.decideHFAndLeaForm.featureEng_id = this.chooseHumanFeaForm.featureEng_id
      this.decideHFAndLeaForm.learner_id = this.chooseLearnerForm.learner_id
      if (this.decideHFAndLeaForm.decision_type === 'Manual_FE') {
        // 应用特征工程
        decisionApi.addHumanFea(this.decideHFAndLeaForm).then(response => {
          // console.log(response)
          const resp = response.data
          if (resp.meta.code === 204) {
            this.$message.success('添加决策成功')
          } else {
            this.$message.error('添加决策失败')
          }
        })
      } else if (this.decideHFAndLeaForm.decision_type === 'Manual_L') {
        // 应用学习器
        decisionApi.addLearner(this.decideLearnerForm).then(response => {
          // console.log(response)
          const resp = response.data
          if (resp.meta.code === 204) {
            this.$message.success('添加决策成功')
          } else {
            this.$message.error('添加决策失败')
          }
        })
      } else {
        // 应用决策者
        decisionApi.addAllDec(this.decideHFAndLeaForm).then(response => {
          // console.log(response)
          const resp = response.data
          if (resp.meta.code === 204) {
            this.$message.success('添加决策成功')
          } else {
            this.$message.error('添加决策失败')
          }
        })
      }
    },
    handleDecideOption () {
      if (this.decideHFAndLeaForm.decision_type === 'Manual_FE') {
        // 应用特征工程 禁用选择学习器
        this.chooseFEDisabled = false
        this.chooseLearnerDisabled = true
      } else if (this.decideHFAndLeaForm.decision_type === 'Manual_L') {
        // 应用学习器 禁用选择特征工程
        this.chooseFEDisabled = true
        this.chooseLearnerDisabled = false
      } else {
        // 应用决策者
        this.chooseFEDisabled = false
        this.chooseLearnerDisabled = false
      }
    },
    // 点击按钮，跳转到决策特征工程页面
    // gotoDecHumanFea () {
    //   this.$router.push('/decision/decHumanFea')
    // },
    gotoQueryDec () {
      this.$router.push('/decision/queryDecision')
    }
    // gotoLearnDec () {
    //   this.$router.push('/decision/decLearner')
    // }
  }
}
</script>

<style scoped>
/* .selectHuFea {
  margin-top: 20px;
} */
.choosedataset {
  margin-top: 20px;
}
.el-form-item{
  margin-bottom: 30px;
}
.queryBtn {
  margin-bottom: 20px;
}
</style>
