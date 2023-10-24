<template>
  <div>
      <!-- 面包屑区域 -->
      <!-- <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">人在回路</el-breadcrumb-item>
        <el-breadcrumb-item>决策</el-breadcrumb-item>
      </el-breadcrumb> -->
    <!-- 卡片区域 -->
    <el-card>
      <el-row>
        <el-col :span="24" >
          <el-button class="buttons" @click="gotoQueryDec" type="primary">查询决策</el-button>
        </el-col>
      </el-row>
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
          <el-col :span="20">
            <el-form-item label="决策类型" prop="learner_type">
              <!-- <el-select disabled  v-model="decideHFAndLeaForm.decision_type" placeholder="决策类型" style="width: 300px">
                <el-option v-for="(option, index) in decisionTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>
              </el-select> -->
              <el-radio-group v-model="decideHFAndLeaForm.decision_type" @change="handleDecideOption">
                <el-radio :label="'Manual_D'">应用决策者</el-radio>
                <el-radio :label="'Manual_FE'">应用特征工程</el-radio>
                <el-radio :label="'Manual_L'">应用学习器</el-radio>
                <!--断面算法-->
                <el-radio :label="'Section_Algorithm'">断面算法</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <el-row>
          <el-col :span="10">
            <el-form class="selectHuFea" label-position="right" label-width="150px"  :model="chooseHumanFeaForm">
              <el-form-item prop="featureEng_name" label="特征工程">
                <el-input :disabled="chooseFEDisabled" clearable  readonly v-model="chooseHumanFeaForm.featureEng_name" style="width: 300px"
                          @click.native="humanFeaDialogVisible=true" placeholder="请选择特征工程"></el-input>
              </el-form-item>
            </el-form>
          </el-col>
          <el-col :span="10">
            <el-form label-position="right" label-width="150px"  :model="chooseLearnerForm">
              <el-form-item prop="learner_name" label="学习器">
                <el-input :disabled="chooseLearnerDisabled" clearable  readonly v-model="chooseLearnerForm.learner_name" style="width: 300px"
                          @click.native="learnerDialogVisible=true" placeholder="请选择学习器"></el-input>
              </el-form-item>
            </el-form>
          </el-col>
      </el-row>
      <!--断面算法：task与case选择栏-->
      <el-row v-if="decideHFAndLeaForm.decision_type === 'Section_Algorithm'">
        <el-col :span="10">
          <el-form class="selectTask" label-position="right" label-width="150px" :model="decideHFAndLeaForm">
            <el-form-item label="选择Task" prop="task">
              <el-input clearable readonly v-model="decideHFAndLeaForm.task" @click.native="taskDialogVisible=true" style="width: 300px" placeholder="请选择Task"></el-input>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="10">
          <el-form class="selectCase" label-position="right" label-width="150px" :model="decideHFAndLeaForm">
            <el-form-item label="选择Case" prop="case">
              <el-input clearable readonly v-model="decideHFAndLeaForm.case" @click.native="caseDialogVisible=true" style="width: 300px" placeholder="请选择Case"></el-input>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
      <el-dialog title="选择Task" :visible.sync="taskDialogVisible">
        <el-select v-model="decideHFAndLeaForm.task" placeholder="选择Task">
          <el-option label="M5" value="M5"></el-option>
          <el-option label="S4" value="S4"></el-option>
          <el-option label="S10" value="S10"></el-option>
        </el-select>
      </el-dialog>
      <el-dialog title="选择Case" :visible.sync="caseDialogVisible">
        <el-select v-model="decideHFAndLeaForm.case" placeholder="选择Case">
          <el-option label="118" value="case118"></el-option>
          <el-option label="300" value="case300"></el-option>
          <el-option label="9241" value="case9241"></el-option>
        </el-select>
      </el-dialog>
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
    </el-card>
    <el-card v-if="decideHFAndLeaForm.decision_type === 'Section_Algorithm'">
      <!-- 断面算法：新建卡片显示断面算法调整结果、图像、表格数据，下载结果、图像、表格数据 -->
      <!-- 提交所有表单  -->
      <h3 >断面调整算法数据查看模块</h3>
      <h4 v-if="imageUrl">Q-table：</h4>
      <img :src="imageUrl" alt="Q Table" v-if="imageUrl" width="500px" height="500px">
      <el-input v-model="searchQuery.state" placeholder="输入状态" style="width: 200px; margin-right: 10px;"></el-input>
      <el-input v-model="searchQuery.action" placeholder="输入动作" style="width: 200px; margin-right: 10px;"></el-input>
      <el-button type="primary" @click="searchQTable">检索</el-button>
      <el-button type="primary" @click="toggleSearchForm">{{ isSearchFormVisible ? '隐藏搜索表单' : '显示搜索表单' }}</el-button>
      <el-button @click="exportTable" type="primary">导出表格</el-button>
      <el-table :data="filteredQTableData.length > 0 ? filteredQTableData : qTableData" style="width: 100%" v-if="isSearchFormVisible" >
        <el-table-column prop="state" label="状态" width="180"></el-table-column>
        <el-table-column prop="action" label="动作" width="180"></el-table-column>
        <el-table-column prop="qValue" label="Q值"></el-table-column>
      </el-table>
      <el-button type="primary" @click="toggleQTable">{{ showQTable ? '隐藏表格' : '显示表格' }}</el-button>
      <el-table :data="qTableData" style="width: 100%" v-if="showQTable">
        <el-table-column prop="state" label="状态" width="180"></el-table-column>
        <el-table-column prop="action" label="动作" width="180"></el-table-column>
        <el-table-column prop="qValue" label="Q值"></el-table-column>
      </el-table>
      <h4 v-if="imageUrl">下载结果：</h4>
      <a :href="imageUrl" v-if="imageUrl" download style="margin-right: 10px;">
        <el-button type="primary">下载图像结果</el-button>
      </a>
      <a :href="textUrl" v-if="textUrl" download="q_table_evenly_spaced_states.txt" style="margin-right: 10px;">
        <el-button type="primary">下载文本结果</el-button>
      </a>
      <!-- 下载图片按钮 -->
      <!-- <a :href="imageUrl" v-if="imageUrl" style="margin-right: 10px;">
        <el-button type="primary" @click="downloadImage">下载图片</el-button>
      </a> -->
      <!-- 下载TXT文件按钮 -->
      <!-- <a :href="imageUrl" v-if="imageUrl" style="margin-right: 10px;">
        <el-button type="primary" @click="downloadTxt">下载TXT文件</el-button>
      </a> -->
    </el-card>
    <el-card v-if="decideHFAndLeaForm.decision_type === 'Section_Algorithm'">
    <!-- 断面算法：新建卡片显示人机交互结果，保存几人交互state、action记录，下载state、action记录 -->
    <!-- <h3 v-if="imageUrl">断面算法人机交互模块</h3>-->
    <h3 >断面调整算法人机交互模块</h3>
    <el-form>
      <el-form-item label="选择State">
        <div style="display: flex; align-items: center;">
          <el-select v-model="selectedState" placeholder="请选择State" @change="findTopActions" style="margin-right: 10px;">
            <el-option
              v-for="(state, index) in qTableData.map(item => item.state).filter((value, index, self) => self.indexOf(value) === index)"
              :key="index"
              :label="state"
              :value="state">
            </el-option>
          </el-select>
          <!-- 选择 action -->
          <el-select v-model="selectedAction" placeholder="请选择Action" @change="updateSelectedQValue" style="margin-right: 10px;">
            <el-option
              v-for="(action, index) in topActions"
              :key="index"
              :label="`${action.action} (Q值: ${action.qValue}) - ${generateDescription(index)}`"
              :value="action.action">
            </el-option>
  <!--          &lt;!&ndash; 显示 q 值 &ndash;&gt;-->
  <!--          <el-input v-model="selectedQValue" readonly placeholder="Q 值"></el-input>-->
            <!-- 继续按钮 -->
  <!--          <el-button @click="continueInteraction">继续</el-button>-->
            <!-- 下载交互结果按钮 -->
  <!--          <el-button @click="downloadInteractions">下载交互结果</el-button>-->
          </el-select>
          <div v-if="selectedDescription">
            所选动作的描述：{{ selectedDescription }}
          </div>
          <!-- 显示 q 值 -->
          <el-input v-model="selectedQValue" readonly placeholder="Q 值" style="margin-right: 10px; width: 400px;"></el-input>
        </div>
        <!-- 继续按钮 -->
        <el-button @click="continueInteraction">继续</el-button>
        <!-- 下载交互结果按钮 -->
        <el-button @click="downloadInteractions">下载交互结果</el-button>
      </el-form-item>
      <el-form-item v-if="topActions.length > 0" label="Top 3 Actions">
        <el-select v-model="selectedAction" placeholder="请选择一个Action">
          <el-option v-for="(action, index) in topActions" :key="index" :label="'Action: ' + action.action + ', Q-value: ' + action.qValue" :value="action.action"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item v-if="selectedAction !== ''" label="Selected Action">
        <el-input v-model="selectedAction" readonly></el-input>
      </el-form-item>
      <!-- 断面算法1019：决策树 -->
      <el-button @click="generateAndDownloadDecisionTree">下载决策树</el-button>
      <div id="decisionTree"></div>
    </el-form>
  </el-card>
  <el-card >
    <h3 >决策规则抽取模块</h3>
      <el-button @click="fetchDecisionTree11">查看决策树渲染结果1</el-button>
      <el-button @click="fetchDecisionTree22">查看决策树渲染结果2</el-button>
<!--      <img v-if="tree1ImageUrl" :src="tree1ImageUrl" alt="决策树1" />-->
<!--      <img v-if="tree2ImageUrl" :src="tree2ImageUrl" alt="决策树2" />-->
  </el-card>
    <!-- 决策树1的弹窗 -->
    <el-dialog title="决策树1" :visible.sync="tree1DialogVisible" width="auto">
      <img v-if="tree1ImageUrl" :src="tree1ImageUrl" alt="决策树1" :width="imgWidth1 + 'px'" height="auto" @wheel="handleWheel($event, 'tree1')" @load="setInitialSize('tree1')" />
    </el-dialog>
    <!-- 决策树2的弹窗 -->
    <el-dialog title="决策树2" :visible.sync="tree2DialogVisible" width="auto">
      <img v-if="tree2ImageUrl" :src="tree2ImageUrl" alt="决策树2" :width="imgWidth2 + 'px'" height="auto" @wheel="handleWheel($event, 'tree2')" @load="setInitialSize('tree2')" />
    </el-dialog>
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
import axios from 'axios'
import * as d3 from 'd3'
// 学习器类型
const decisionTypeOptions = [
  { type: 'Manual_FE', name: '应用特征工程' },
  { type: 'Manual_L', name: '应用学习器' },
  { type: 'Manual_D', name: '应用决策者' },
  { type: 'Section_Algorithm', name: '应用断面算法' }
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
      imgWidth1: null, // 1024：决策树1的图片宽度
      imgWidth2: null, // 1024：决策树2的图片宽度
      tree1DialogVisible: false, // 1024：控制决策树1的弹窗可见性
      tree2DialogVisible: false, // 1024：控制决策树2的弹窗可见性
      tree1ImageUrl: '', // 1024：决策树图像url
      tree2ImageUrl: '', // 1024：决策树图像url
      selectedDescription: '',
      nGen: 53,
      nAdjustStep: 2,
      adjustRatios: [0.8, 1.2],
      allActions: [],
      interactionsHistory: [],
      interactions: [], // 新增属性，用于存储用户的交互
      selectedState: '', // 用于存储选中的state
      topActions: [], // 用于存储给定state的top 3 actions
      selectedAction: '', // 用于存储选中的action
      selectedQValue: '', // 用于存储选定的Q值
      isSearchFormVisible: false,
      taskDialogVisible: false,
      caseDialogVisible: false,
      qTableData: [],
      showQTable: false,
      searchQuery: {
        state: '',
        action: ''
      },
      filteredQTableData: [],
      imageUrl: '',
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
        dataset_id: '',
        task: '',
        case: ''
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
  computed: {
    enrichedTopActions () {
      return this.topActions.map((action, index) => {
        const genIdx = Math.floor(index / this.nAdjustStep)
        const ratioIdx = index % this.nAdjustStep
        const description = `对第 ${genIdx + 1} 个电力生成单元进行${this.adjustRatios[ratioIdx] === 0.8 ? '减少到' : '增加到'} ${this.adjustRatios[ratioIdx] * 100}% 的输出电量`
        return {
          ...action,
          description
        }
      })
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
      if (this.decideHFAndLeaForm.decision_type === 'Section_Algorithm') {
        // 应用特征工程
        decisionApi.addMam(this.decideHFAndLeaForm).then(response => {
          // console.log(response)
          const resp = response.data
          if (resp.meta.code === 204) {
            this.$message.success('添加决策成功')
            if (resp.data && resp.data.imageData) {
              this.imageUrl = resp.data.imageData
              // 解析文本数据
              const decodedText = atob(resp.data.textData.split('base64,')[1])
              const lines = decodedText.split('\n')
              let currentState = ''
              lines.forEach(line => {
                if (line.startsWith('State')) {
                  currentState = line
                } else if (line.startsWith('Action')) {
                  const actionDetails = line.split(': Q-value = ')
                  this.qTableData.push({
                    state: currentState,
                    action: actionDetails[0],
                    qValue: actionDetails[1]
                  })
                }
              })
            }
            if (resp.data && resp.data.textData) {
              this.textUrl = resp.data.textData
            } else {
              this.$message.error('添加决策失败')
            }
          }
        })
      } else if (this.decideHFAndLeaForm.decision_type === 'Manual_FE') {
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
    // 断面算法：优化选择界面
    handleDecideOption () {
      if (this.decideHFAndLeaForm.decision_type === 'Section_Algorithm') {
        // 禁用"特征工程"和"学习器"当选择"断面算法"
        this.chooseFEDisabled = true
        this.chooseLearnerDisabled = true
      } else if (this.decideHFAndLeaForm.decision_type === 'Manual_FE') {
        // 应用特征工程 禁用选择学习器
        console.log('handleDecideOption: Manual_FE')
        this.chooseFEDisabled = false
        this.chooseLearnerDisabled = true
      } else if (this.decideHFAndLeaForm.decision_type === 'Manual_L') {
        // 应用学习器 禁用选择特征工程
        console.log('handleDecideOption: Manual_L')
        this.chooseFEDisabled = true
        this.chooseLearnerDisabled = false
      } else {
        // 应用决策者
        console.log('handleDecideOption: Manual_D')
        this.chooseFEDisabled = false
        this.chooseLearnerDisabled = false
      }
    },
    gotoQueryDec () {
      this.$router.push('/decision/queryDecision')
    },
    toggleQTable () {
      this.showQTable = !this.showQTable
    },
    searchQTable () {
      this.filteredQTableData = this.qTableData.filter(item => {
        return (this.searchQuery.state === '' || item.state.includes(this.searchQuery.state)) && (this.searchQuery.action === '' || item.action.includes(this.searchQuery.action))
      })
    },
    // 断面算法：下载结果图片
    downloadImage () {
      // axios.get('/download/image', { responseType: 'blob' })
      axios.get('/download/image', { responseType: 'arraybuffer' })
        .then(response => {
          // 使用blob创建一个URL，并使用a标签来下载
          console.log('响应数据:', response)
          const blob = new Blob([response.data], { type: 'image/png' })
          const url = window.URL.createObjectURL(blob)
          // const url = window.URL.createObjectURL(new Blob([response.data]))
          const link = document.createElement('a')
          link.href = url
          link.setAttribute('download', 'q_table.png')
          document.body.appendChild(link)
          link.click()
        })
        .catch(error => {
          // 错误处理，例如提示用户登录
          console.error('下载失败:', error)
        })
    },
    // 断面算法：下载结果数据文件
    downloadTxt () {
      // 调用后端端点下载TXT文件
      window.location.href = '/download/txt'
    },
    toggleSearchForm () {
      this.isSearchFormVisible = !this.isSearchFormVisible
    },
    // 断面算法：寻找最优action
    findTopActions () {
      if (this.selectedState !== '') {
        const actions = this.qTableData.filter(item => item.state === this.selectedState)
        // actions.sort((a, b) => b.qValue - a.qValue)
        // this.topActions = actions.slice(0, 3)
        this.topActions = actions
      }
    },
    // 断面算法：选择action
    selectAction (action) {
      this.selectedAction = action
    },
    // 断面算法：保存交互结果并继续
    continueInteraction () {
      if (this.selectedState && this.selectedAction && this.selectedQValue) {
        this.interactions.push({
          state: this.selectedState,
          action: this.selectedAction,
          qValue: this.selectedQValue
        })
        // 将当前交互添加到历史数组中
        this.interactionsHistory.push({
          state: this.selectedState,
          action: this.selectedAction,
          qValue: this.selectedQValue,
          timestamp: new Date().toISOString() // 记录交互的时间戳
        })
        // 清除当前选择
        this.selectedState = ''
        this.selectedAction = ''
        this.selectedQValue = ''
      }
    },
    // 断面算法：下载当前交互记录
    downloadInteractions () {
      const lines = this.interactions.map((item, index) => {
        let description = ''
        if (item.action !== '') {
          const selectedActionDetails = this.topActions.find(actionItem => actionItem.action === item.action)
          if (selectedActionDetails) {
            const selectedIndex = this.topActions.findIndex(action => action.action === item.action)
            if (selectedIndex !== -1) {
              const genIdx = Math.floor(selectedIndex / this.nAdjustStep)
              const ratioIdx = selectedIndex % this.nAdjustStep
              description = `对第 ${genIdx + 1} 个电力生成单元进行${this.adjustRatios[ratioIdx] === 0.8 ? '减少到' : '增加到'} ${this.adjustRatios[ratioIdx] * 100}% 的输出电量`
            }
          }
        }
        return `${item.state},${item.action},${item.qValue},${description}` // 添加描述到每一行
      })
      const blob = new Blob([lines.join('\n')], { type: 'text/plain' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = '断面调整人机交互记录.txt'
      document.body.appendChild(link)
      link.click()
    },
    // 断面算法：更新q值
    updateSelectedQValue () {
      // if (this.selectedAction !== '') {
      //   const selectedActionDetails = this.topActions.find(item => item.action === this.selectedAction)
      //   if (selectedActionDetails) {
      //     this.selectedQValue = selectedActionDetails.qValue
      //   }
      // }
      // if (this.selectedAction !== '') {
      //   const selectedActionDetails = this.topActions.find(item => item.action === this.selectedAction)
      //   if (selectedActionDetails) {
      //     // 更新 selectedQValue
      //     this.selectedQValue = selectedActionDetails.qValue
      //     // 计算该动作的索引
      //     const selectedIndex = this.topActions.findIndex(action => action.action === this.selectedAction)
      //     // 根据索引计算动作描述
      //     if (selectedIndex !== -1) {
      //       const genIdx = Math.floor(selectedIndex / this.nAdjustStep)
      //       const ratioIdx = selectedIndex % this.nAdjustStep
      //       const description = `对第 ${genIdx + 1} 个电力生成单元进行${this.adjustRatios[ratioIdx] === 0.8 ? '减少到' : '增加到'} ${this.adjustRatios[ratioIdx] * 100}% 的输出电量`
      //       // 更新动作的描述
      //       selectedActionDetails.description = description
      //     }
      //   }
      // }
      if (this.selectedAction !== '') {
        const selectedActionDetails = this.topActions.find(item => item.action === this.selectedAction)
        if (selectedActionDetails) {
          this.selectedQValue = selectedActionDetails.qValue
          const selectedIndex = this.topActions.findIndex(action => action.action === this.selectedAction)
          if (selectedIndex !== -1) {
            const genIdx = Math.floor(selectedIndex / this.nAdjustStep)
            const ratioIdx = selectedIndex % this.nAdjustStep
            const description = `对第 ${genIdx + 1} 个电力生成单元进行${this.adjustRatios[ratioIdx] === 0.8 ? '减少到' : '增加到'} ${this.adjustRatios[ratioIdx] * 100}% 的输出电量`
            this.selectedDescription = description
          }
        }
      }
    },
    // 断面算法：添加action描述
    generateDescription (index) {
      const genIdx = Math.floor(index / this.nAdjustStep)
      const ratioIdx = index % this.nAdjustStep
      return `对第 ${genIdx + 1} 个电力生成单元进行${this.adjustRatios[ratioIdx] === 0.8 ? '减少到' : '增加到'} ${this.adjustRatios[ratioIdx] * 100}% 的输出电量`
    },
    // downloadInteractionsHistory () {
    //   if (this.selectedState !== '') {
    //     const actions = this.qTableData.filter(item => item.state === this.selectedState)
    //     this.allActions = actions.map(action => ({
    //       action: action.action,
    //       qValue: action.qValue
    //     }))
    //     const existingHistoryIndex = this.interactionsHistory.findIndex(item => item.state === this.selectedState)
    //     if (existingHistoryIndex !== -1) {
    //       this.interactionsHistory[existingHistoryIndex].actions = this.allActions
    //       this.interactionsHistory[existingHistoryIndex].timestamp = new Date().toISOString()
    //     } else {
    //       this.interactionsHistory.push({
    //         state: this.selectedState,
    //         actions: this.allActions,
    //         timestamp: new Date().toISOString()
    //       })
    //     }
    //     const jsonBlob = new Blob([JSON.stringify(this.interactionsHistory, null, 2)], { type: 'application/json' })
    //     const jsonLink = document.createElement('a')
    //     jsonLink.href = URL.createObjectURL(jsonBlob)
    //     jsonLink.download = 'interactions_history.json'
    //     document.body.appendChild(jsonLink)
    //     jsonLink.click()
    //     const txtBlob = new Blob([this.interactionsHistory.map(item => `${item.timestamp}, ${item.state}, ${JSON.stringify(item.actions)}`).join('\n')], { type: 'text/plain' })
    //     const txtLink = document.createElement('a')
    //     txtLink.href = URL.createObjectURL(txtBlob)
    //     txtLink.download = 'interactions_history.txt'
    //     document.body.appendChild(txtLink)
    //     txtLink.click()
    //   }
    // }
    // 断面算法：下载历史记录（json格式）
    downloadInteractionsHistory () {
      if (this.selectedState !== '') {
        const actions = this.qTableData.filter(item => item.state === this.selectedState)
        this.allActions = actions.map(action => `${action.action}, Q-value: ${action.qValue}`).join('; ')
        const existingHistoryIndex = this.interactionsHistory.findIndex(item => item.state === this.selectedState)
        if (existingHistoryIndex !== -1) {
          this.interactionsHistory[existingHistoryIndex].actions = this.allActions
          this.interactionsHistory[existingHistoryIndex].timestamp = new Date().toISOString()
        } else {
          this.interactionsHistory.push({
            state: this.selectedState,
            actions: this.allActions,
            timestamp: new Date().toISOString()
          })
        }
        const jsonBlob = new Blob([JSON.stringify(this.interactionsHistory, null, 2)], { type: 'application/json' })
        const jsonLink = document.createElement('a')
        jsonLink.href = URL.createObjectURL(jsonBlob)
        jsonLink.download = 'interactions_history.json'
        document.body.appendChild(jsonLink)
        jsonLink.click()
        const txtBlob = new Blob([this.interactionsHistory.map(item => `${item.timestamp}, State ${item.state}:, ${item.actions}`).join('\n')], { type: 'text/plain' })
        const txtLink = document.createElement('a')
        txtLink.href = URL.createObjectURL(txtBlob)
        txtLink.download = 'interactions_history.txt'
        document.body.appendChild(txtLink)
        txtLink.click()
      }
    },
    // 断面算法：1019生成并下载决策树
    generateAndDownloadDecisionTree () {
      // 清除之前的 SVG 元素
      d3.select('#decisionTree svg').remove()
      const interactions = this.interactionsHistory
      const treeData = this.convertInteractionsToTree(interactions)
      this.renderDecisionTree(treeData)
      this.downloadSVGAsPNG()
    },
    // 断面算法：1019将交互记录转换为决策树数据
    // convertInteractionsToTree (interactions) {
    //   const root = { name: 'Root', children: [] }
    //   interactions.forEach(interaction => {
    //     let existingStateNode = root.children.find(child => child.name === interaction.state)
    //     if (!existingStateNode) {
    //       existingStateNode = { name: interaction.state, children: [] }
    //       root.children.push(existingStateNode)
    //     }
    //     const color = interaction.qValue > 0.5 ? 'red' : 'blue' // 基于 qValue 确定颜色
    //     existingStateNode.children.push({ name: interaction.action, color })
    //   })
    //   return root
    // },
    // 断面算法：1019将交互记录转换为决策树数据,有蓝色节点，有注释，但是红色节点位置全部在末尾这一点要改
    convertInteractionsToTree (interactions) {
      const root = { name: 'Root', children: [] }
      let currentNode = root
      interactions.forEach(interaction => {
        const actionNode = { name: interaction.action, color: 'red', children: [], state: interaction.state }
        const stateNodes = [] // 添加多个蓝色节点
        // 添加与当前action关联的所有可能的state
        // for (let i = 0; i < this.totalActions; i++) {
        for (let i = 0; i < 106; i++) {
          const stateNode = { name: `action${i}`, color: 'blue', children: [] }
          stateNodes.push(stateNode)
        }
        actionNode.children = stateNodes
        // 将当前action添加为新的节点，并将其设置为当前节点
        currentNode.children.push(actionNode)
        currentNode = actionNode // 将选中的action设置为当前节点
      })
      return root
    },
    // 断面算法：1019使用 D3.js 渲染决策树
    // 修改后的使用 D3.js 渲染决策树
    renderDecisionTree (treeData) {
      d3.select('#decisionTree svg').remove()
      const svg = d3.select('#decisionTree').append('svg')
        .attr('width', 1000) // 调整为较小的尺寸
        .attr('height', 1000) // 调整为较小的尺寸
      const root = d3.hierarchy(treeData)
      const treeLayout = d3.tree().size([900, 900])
      const treeRoot = treeLayout(root)
      // 添加节点
      const nodes = svg.selectAll('.node')
        .data(treeRoot.descendants())
        .enter()
        .append('g')
        .attr('transform', d => `translate(${d.x}, ${d.y})`)
      nodes.append('circle')
        .attr('class', 'node')
        .attr('r', 5) // 缩小节点大小
        .attr('fill', d => d.data.color)
      // 添加连线
      svg.selectAll('.link')
        .data(treeRoot.links())
        .enter()
        .append('line')
        .attr('class', 'link')
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)
        .attr('stroke', 'black')
      // 添加备注到红色节点
      nodes.filter(d => d.data.color === 'red')
        .append('text')
        .attr('dx', -10)
        .attr('dy', -10)
        .attr('font-size', '10px')
        .text(d => `state: ${d.data.state || ''}, action: ${d.data.name}`)
    },
    // 断面算法：1019下载 SVG 为 PNG
    downloadSVGAsPNG () {
      const svg = document.querySelector('#decisionTree svg')
      const canvas = document.createElement('canvas')
      canvas.width = svg.width.baseVal.value
      canvas.height = svg.height.baseVal.value
      const ctx = canvas.getContext('2d')
      const data = (new XMLSerializer()).serializeToString(svg)
      const blob = new Blob([data], { type: 'image/svg+xml;charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const img = new Image()
      img.onload = function () {
        ctx.drawImage(img, 0, 0)
        window.URL.revokeObjectURL(url)
        // 保存为 PNG 图片
        const imgURL = canvas.toDataURL('image/png')
        const link = document.createElement('a')
        link.href = imgURL
        link.download = '决策树.png'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      }
      img.src = url
    },
    // 1024：查看渲染决策树
    fetchDecisionTree11 () {
      this.tree1ImageUrl = ''
      this.tree2ImageUrl = ''
      decisionApi.fetchDecisionTree1({ treeType: 'tree1' }).then(response => {
        const resp = response.data
        if (resp.meta.code === 204) {
          this.$message.success('获取决策树1成功')
          if (resp.data && resp.data.imageData) {
            this.tree1ImageUrl = ''
            this.tree1ImageUrl = resp.data.imageData
            // 集成的下载图片代码
            const link = document.createElement('a')
            link.href = resp.data.imageData
            this.tree1DialogVisible = true // 显示决策树1的弹窗
            link.download = '决策树1.png'
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
          }
        } else {
          this.$message.error('获取决策树1失败')
        }
      }).catch(error => {
        console.error('Fetch Decision Tree 1 failed:', error)
        this.$message.error('获取决策树1失败')
      })
    },
    // 1024：查看渲染决策树
    fetchDecisionTree22 () {
      this.tree1ImageUrl = ''
      this.tree2ImageUrl = ''
      decisionApi.fetchDecisionTree2({ treeType: 'tree2' }).then(response => {
        const resp = response.data
        if (resp.meta.code === 204) {
          this.$message.success('获取决策树2成功')
          if (resp.data && resp.data.imageData) {
            this.tree2ImageUrl = ''
            this.tree2ImageUrl = resp.data.imageData
            // 集成的下载图片代码
            const link = document.createElement('a')
            link.href = resp.data.imageData
            this.tree2DialogVisible = true // 显示决策树2的弹窗
            link.download = '决策树2.png'
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
          }
        } else {
          this.$message.error('获取决策树2失败')
        }
      }).catch(error => {
        console.error('Fetch Decision Tree 2 failed:', error)
        this.$message.error('获取决策树2失败')
      })
    },
    // 1024：决策树弹窗
    showTree1Dialog () {
      this.fetchDecisionTree1() // 获取决策树1的数据
      this.tree1DialogVisible = true // 显示决策树1的弹窗
    },
    // 1024：决策树弹窗
    showTree2Dialog () {
      this.fetchDecisionTree2() // 获取决策树2的数据
      this.tree2DialogVisible = true // 显示决策树2的弹窗
    },
    // 1024：鼠标滚轮调整决策树图像大小
    handleWheel (event, treeType) {
      const delta = event.deltaY > 0 ? 200 : -200
      if (treeType === 'tree1') {
        this.imgWidth1 = Math.max(1000, this.imgWidth1 + delta)
      } else if (treeType === 'tree2') {
        this.imgWidth2 = Math.max(1000, this.imgWidth2 + delta)
      }
    },
    // 1024：鼠标滚轮调整决策树图像大小
    setInitialSize (treeType) {
      if (treeType === 'tree1') {
        this.imgWidth1 = 1000
      } else if (treeType === 'tree2') {
        this.imgWidth2 = 800
      }
    }
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
.buttons{
    float: right;
}
/* .queryBtn{
    width: 120px;
}
.queryBtn {
  margin-bottom: 20px;
  float: left;
} */
/* .buttons{
  /* margin-bottom: 15px; */
  /* float: right;
} */
  /* .el-form {
    margin-top: 80px;
  } */
</style>
