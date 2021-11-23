<template>
    <div>
      <!-- 统计任务进度 -->
      <el-card>
        <div><h3>学习器进度</h3></div>
        <el-row align="center" style="margin-bottom: 30px" :gutter="20">
          <el-col align="center" :span="6">
            <el-progress :format="format1" type="circle" stroke-width="12" width="200" color="#8e71c7"
            :percentage="1+learnerDoneCnt">
            </el-progress>
          </el-col>
          <el-col align="center" :span="6">
            <el-progress :format="format2" type="circle" stroke-width="12" width="200" color="#f36838"
            :percentage="1+learnerUndoneCnt"></el-progress>
          </el-col>
          <el-col align="center" :span="6">
            <el-progress :format="format3" type="circle" stroke-width="12" width="200" color="#21a675"
            :percentage="learnerCnt==0 ? 0 : parseFloat(learnerDoneCnt/learnerCnt*100).toFixed(1)"></el-progress>
          </el-col>
          <el-col align="center" :span="6">
            <el-button type="primary" @click="inputHumanAction">查看待处理人在回路学习器</el-button>
          </el-col>
        </el-row>
      </el-card>
    <!-- 卡片区域 -->
    <el-card>
      <div class="buttons">
         <el-button @click="queryLearner" class="queryBtn" type="primary">查看学习器</el-button>
      </div>
                <!-- form区域 -->
      <el-form label-position="right" label-width="150px"  :model="chooseDatasetForm" ref="chooseDatasetFormRef">
        <el-form-item prop="dataset_name" label="数据集">
          <el-input clearable  readonly v-model="chooseDatasetForm.dataset_name" style="width: 300px"
                    @click.native="datasetDialogVisible=true" placeholder="请选择数据集"></el-input>
        </el-form-item>
      </el-form>
      <el-form label-position="right" label-width="150px" :model="addLearnerForm" ref="addLearnerFormRef"  class="demo-ruleForm">
        <el-form-item label="学习器名" prop="learner_name">
          <el-input clearable  v-model="addLearnerForm.learner_name" placeholder="请填写学习器名" style="width: 300px"></el-input>
        </el-form-item>
        <el-form-item label="学习器类型" prop="learner_type">
          <el-select  v-model="addLearnerForm.learner_type" placeholder="学习器类型" style="width: 300px">
            <el-option v-for="(option, index) in learnerTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <!-- 学习参数的表单 -->
      <el-form label-position="right" label-width="150px" :model="learnParamsForm" ref="learnParamsFormRef" >
            <el-form-item label="训练方法" prop="train_name">
              <el-select  v-model="learnParamsForm.train_name" placeholder="请选择方法" style="width: 300px"
              @change="handleselectTrainname">
                <el-option
                  v-for="(item,index) in algorithm_name" :key="index"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item class="label" v-for="(params, index) in algorithm_parameters"
                      :label="params.name" :key="index">
              <el-select v-if="params.name==='label'"  :multiple="labelMultible"
                          v-model="params.value" placeholder="请选择标签列">
                <el-option
                  v-for="(item,index) in columnsList" :key="index"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
              <el-input v-else style="width:350px" v-model="params.value"></el-input>
            </el-form-item>
            <!-- <el-form-item  label="n_components" prop="n_estimators">
               <el-input-number  v-model="learnParamsForm.n_estimators"
               :min="1" :max="20" label="请输入n_components"></el-input-number>
            </el-form-item> -->
            <el-button class="submitBtn" type="primary" @click="submitAllForm">开始训练</el-button>
      </el-form>
      <!-- 提交所有表单  -->

    </el-card>
  <!--      选择数据集，弹出的窗口-->
    <el-dialog title="选择数据集" :visible.sync="datasetDialogVisible" @close="getColumns">
      <!-- <dataset :isDialog="true" @dataset-choose = chooseDataset></dataset> -->
      <dataset-hu-fea :isDialog="true" @dataset-choose = chooseDataset></dataset-hu-fea>
    </el-dialog>
    </div>
</template>

<script>
import DatasetHuFea from '../data/HumanFeaDataset'
import featureApi from './../../api/feature'
import learnApi from './../../api/learn'
// 学习器类型
const learnerTypeOptions = [
  { type: 'Manual', name: '人工' },
  { type: 'Auto', name: '自动化' },
  { type: 'HML', name: '人在回路' }
]
export default {
  name: 'Learn',
  components: {
    DatasetHuFea
  },
  data () {
    return {
      // 选择数据集form
      chooseDatasetForm: {
        dataset_name: '',
        dataset_id: ''
      },
      datasetId: '',
      datasetDialogVisible: false,
      addLearnerForm: {
        learner_name: '',
        learner_type: '',
        learner_parameters: {
        },
        dataset_id: ''
      },
      // 用于学习器类型转换的
      learnerTypeOptions,
      columnsList: [],
      // 学习参数的表单
      learnParamsForm: {
        train_name: '',
        label: [],
        n_estimators: 1
      },
      algorithm_name: [],
      // 根据算法类型收到的算法总数据
      algorithm_Options: [],
      // 算法参数
      algorithm_parameters: {},
      algorithm_category: 'Learner_supervised',
      labelMultible: true,
      // 学习器进度统计
      learnerCnt: 0,
      learnerDoneCnt: 0,
      learnerUndoneCnt: 0
    }
  },
  created () {
    this.getAlgorithm()
    this.getLearnerInfo()
  },
  methods: {
    // 接受数据集组件传来的数据
    chooseDataset (currentRow) {
      this.chooseDatasetForm.dataset_name = currentRow.dataset_name
      this.chooseDatasetForm.dataset_id = currentRow.dataset_id
      this.datasetId = currentRow.dataset_id
      this.datasetDialogVisible = false
    },
    // 获取数据集列名
    getColumns () {
      if (this.datasetId !== '') {
        featureApi.getDatasetColumns(this.datasetId).then(response => {
          const resp = response.data
          this.columnsList = resp.data
        })
      }
    },
    // 当选择标签选择框没有先选择方法的时候，
    handleselect () {
      // console.log(12)
      if (this.learnParamsForm.train_name === '') {
        this.$message.error('请先选择方法')
        this.columnsList = []
      }
    },
    // 当训练方法发生改变的时候
    handleselectTrainname () {
      this.getColumns()
      for (let i = 0; i < this.algorithm_Options.length; i++) {
        if (this.algorithm_Options[i].algorithm_name === this.learnParamsForm.train_name) {
          this.algorithm_parameters = JSON.parse(this.algorithm_Options[i].algorithm_parameters)
          this.learnParamsForm.algorithm_parameters = this.algorithm_parameters
          console.log(this.algorithm_parameters)
          for (let i = 0; i < this.algorithm_parameters.length; i++) {
            if (this.algorithm_parameters[i].name === 'label') {
              if (this.algorithm_parameters[i].select === 'single-select') {
                this.labelMultible = false
              } else {
                this.labelMultible = true
              }
              console.log(this.labelMultible)
            }
          }
        }
      }
    },
    // 查看学习器
    queryLearner () {
      this.$router.push('/learn/queryLearner')
    },
    // 处理人在回路学习器
    inputHumanAction () {
      this.$router.push('/learn/queryLearner')
    },
    submitAllForm () {
      console.log(this.addLearnerForm)
      console.log(this.learnParamsForm)
      this.addLearnerForm.dataset_id = this.datasetId
      this.addLearnerForm.learner_parameters = this.learnParamsForm
      // label, n_estimators
      for (let i = 0; i < this.addLearnerForm.learner_parameters.algorithm_parameters.length; i++) {
        if (this.addLearnerForm.learner_parameters.algorithm_parameters[i].name === 'label') {
          this.addLearnerForm.learner_parameters.label = Array(this.addLearnerForm.learner_parameters.algorithm_parameters[i].value)
        } else if (this.addLearnerForm.learner_parameters.algorithm_parameters[i].name === 'n_estimators') {
          this.addLearnerForm.learner_parameters.n_estimators = parseInt(this.addLearnerForm.learner_parameters.algorithm_parameters[i].value, 10)
        }
      }
      learnApi.add(this.addLearnerForm).then(response => {
        console.log(this.addLearnerForm)
        console.log(response)
        const resp = response.data
        if (resp.meta.code === 204) {
          this.$message.success('添加学习器成功')
        } else {
          this.$message.error('添加学习器失败')
        }
      })
    },
    // 通过算法接口动态获取参数
    getAlgorithm () {
      learnApi.queryAlgorithm(this.algorithm_category).then(response => {
        this.algorithm_Options = response.data.data
        this.algorithm_name = response.data.data.map(item => item.algorithm_name)
        console.log(this.algorithm_Options)
      })
    },
    // 学习器学习进度
    getLearnerInfo () {
      learnApi.query().then(response => {
        // console.log(response)
        const resp = response.data
        if (resp.meta.code === 200) {
          this.$message.success('加载学习器成功')
          this.LearnerData = resp.data
          // 统计数量
          this.learnerCnt = resp.data.length
          this.learnerDoneCnt = resp.data.filter(item => {
            return item.train_state === '2'
          }).length
          this.learnerUndoneCnt = this.learnerCnt - this.learnerDoneCnt
        }
      })
    },
    format1 () {
      return `已完成：${this.learnerDoneCnt}`
    },
    format2 () {
      return `未完成：${this.learnerUndoneCnt}`
    },
    format3 (percentage) {
      return `进度：${percentage}%`
    }
  }
}
</script>

<style scoped>
.buttons{
  /* margin-bottom: 15px; */
  float: right;
}
  .el-form {
    margin-top: 80px;
  }
  .submitBtn {
    margin-left: 200px;
  }
</style>
