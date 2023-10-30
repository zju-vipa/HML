<template>
  <div>
    <!-- 卡片区域 -->
    <el-card>
<!--      <el-button class="queryBtn" @click="queryFeatureEng" type="primary">查看特征工程</el-button>-->
           <!-- 表单区域 -->
      <el-button class="opbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
      <el-form label-position="right" label-width="250px" :model="addFeatureForm" :rules="addFeatureFormRules" ref="addFeatureFormRef" class="demo-ruleForm">
            <el-form-item class="label" label="原始数据集" prop="original_dataset_name">
              <el-input clearable disabled="" style="width:610px" v-model="addFeatureForm.original_dataset_name" placeholder="返回选择原始数据集"></el-input>
            </el-form-item>
            <el-form-item class="label" label="特征工程名" prop="featureEng_name">
              <el-input clearable style="width:610px" v-model="addFeatureForm.featureEng_name" placeholder="请填写特征工程名"></el-input>
            </el-form-item>
            <el-form-item class="label" label="所属运行方式" prop="featureEng_name" style="width:610px">
              <el-select v-model="addFeatureForm.run_mode" placeholder="请选择">
                <el-option v-for="(option, index) in runModeOptions" :key="index" :label="option.type" :value="option.name">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item class="label" label="特征工程类型" prop="featureEng_type">
              <!-- <el-input style="width:410px" v-model="addFeatureForm.featureEng_type"></el-input> -->
              <!-- <el-select v-model="addFeatureForm.featureEng_type" style="width:610px" @change="handleFeatureEngType">
                <el-option v-for="(option, index) in featureEngTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>
              </el-select> -->
              <el-radio-group v-model="addFeatureForm.featureEng_type" style="width:610px" @change="handleFeatureEngType">
                <el-radio v-for="(option, index) in featureEngTypeOptions" :key="index" :label="option.type" >{{option.name}}</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item class="label" label="技术方法配置" prop="featureEng_processes">
              <div v-if="addFeatureForm.featureEng_type==''">
                <span style="color: darkgray">请先选择特征工程类型</span>
              </div>
              <div v-else-if="addFeatureForm.featureEng_type=='HumanInLoop'">
                <el-row>
                  <el-col span="12">
                    <el-card class="card-form">
                    <el-form label-width="150px" label-position="left" :model="processConstructForm">
                      <el-form-item  label="特征解耦">
                          <el-select style="width:360px" v-model="processConstructForm.operate_name" placeholder="请选择方法" @change="handleselectTrainname">
                          <el-option
                            v-for="(item,index) in algorithm_Options" :key="index"
                            :label="item.introduction"
                            :value="item.algorithm_name">
                          </el-option>
                        </el-select>
                      </el-form-item >
                      <el-form-item class="label" v-for="(params, index) in algorithm_parameters"
                        :label="params.introduction" :key="index">
                        <el-select v-if="params.name==='col_retain'" style="width:360px" :multiple="labelMultible"
                          v-model="params.value" placeholder="请选择保留列">
                          <el-option
                            v-for="(item,index) in columnsList" :key="index"
                            :label="item"
                            :value="item">
                          </el-option>
                        </el-select>
                        <el-checkbox-group v-else-if="params.name==='machine_operators'" style="width:360px"
                          v-model="machine_operators_list">
                          <el-checkbox :label="'sum'">sum</el-checkbox>
                          <el-checkbox :label="'log'">log</el-checkbox>
                          <el-checkbox :label="'mean'">mean</el-checkbox>
                        </el-checkbox-group>
                        <!-- 基于算子 人在回路特征工程的参数 -->
                        <div v-else-if="params.name==='human_operators'" style="width:360px">
                          <!-- <el-button @click="handleAddSumOperator">sum</el-button>
                          <el-button @click="handleAddLogOperator">log</el-button>
                          <el-button @click="handleAddMeanOperator">mean</el-button> -->
                          <el-button class="addBtn" type="primary" @click="dialogSumVisible = true">设置</el-button>
                          <!-- sum算子弹框 -->
                          <el-dialog
                            title="请添加特征求和（sum）算子"
                            :visible.sync="dialogSumVisible"
                            :close-on-click-modal="false">
                            <el-table border :data="human_operators_sum_list" style="width: 100%" >
                                <el-table-column min-width="40%" prop="columns" label="求和运算列">
                                  <template scope="scope">
                                    <el-select :multiple="true" v-model="scope.row.columns" placeholder="请选择运算列">
                                      <el-option
                                        v-for="(item,index) in columnsList" :key="index"
                                        :label="item"
                                        :value="item">
                                      </el-option>
                                    </el-select>
                                  </template>
                                </el-table-column>
                                <el-table-column min-width="20%" fixed="right" label="操作">
                                  <template slot-scope="scope">
                                    <!-- 删除 新增 -->
                                    <el-button @click.native.prevent="deleteRow(scope.$index, human_operators_sum_list)"
                                    icon="el-icon-minus" size="medium" circle></el-button>
                                    <el-button @click.native.prevent="addRowSimple(human_operators_sum_list)"
                                    icon="el-icon-plus" size="medium" circle></el-button>
                                  </template>
                                </el-table-column>
                              </el-table>
                              <el-button class="addBtn" @click="addRowSimple(human_operators_sum_list)" > 新增 </el-button>
                              <el-button class="addBtn" @click="handleSumNextStep" > 下一步 </el-button>
                          </el-dialog>
                          <!-- log算子弹框 -->
                          <el-dialog
                            title="请添加特征对数（log）算子"
                            :visible.sync="dialogLogVisible"
                            :close-on-click-modal="false">
                            <el-table border :data="human_operators_log_list" style="width: 100%" >
                                <el-table-column min-width="40%" prop="columns" label="对数运算列">
                                  <template scope="scope">
                                    <el-select :multiple="false" v-model="scope.row.columns" placeholder="请选择运算列">
                                      <el-option
                                        v-for="(item,index) in columnsList" :key="index"
                                        :label="item"
                                        :value="item">
                                      </el-option>
                                    </el-select>
                                  </template>
                                </el-table-column>
                                <el-table-column min-width="20%" fixed="right" label="操作">
                                  <template slot-scope="scope">
                                    <!-- 删除 新增 -->
                                    <el-button @click.native.prevent="deleteRow(scope.$index, human_operators_log_list)"
                                    icon="el-icon-minus" size="medium" circle></el-button>
                                    <el-button @click.native.prevent="addRowSimple(human_operators_log_list)"
                                    icon="el-icon-plus" size="medium" circle></el-button>
                                  </template>
                                </el-table-column>
                              </el-table>
                              <el-button class="addBtn" @click="addRowSimple(human_operators_log_list)" > 新增 </el-button>
                              <el-button class="addBtn" @click="handleLogNextStep" > 下一步 </el-button>
                          </el-dialog>
                          <!-- mean算子弹框 -->
                          <el-dialog
                            title="请添加特征均值（mean）算子"
                            @close="clearHumanOperators3list"
                            :visible.sync="dialogMeanVisible"
                            :close-on-click-modal="false">
                            <el-table border :data="human_operators_mean_list" style="width: 100%" >
                                <el-table-column min-width="40%" prop="columns" label="均值运算列">
                                  <template scope="scope">
                                    <el-select :multiple="true" v-model="scope.row.columns" placeholder="请选择运算列">
                                      <el-option
                                        v-for="(item,index) in columnsList" :key="index"
                                        :label="item"
                                        :value="item">
                                      </el-option>
                                    </el-select>
                                  </template>
                                </el-table-column>
                                <el-table-column min-width="20%" fixed="right" label="操作">
                                  <template slot-scope="scope">
                                    <!-- 删除 新增 -->
                                    <el-button @click.native.prevent="deleteRow(scope.$index, human_operators_mean_list)"
                                    icon="el-icon-minus" size="medium" circle></el-button>
                                    <el-button @click.native.prevent="addRowSimple(human_operators_mean_list)"
                                    icon="el-icon-plus" size="medium" circle></el-button>
                                  </template>
                                </el-table-column>
                              </el-table>
                              <el-button class="addBtn" @click="addRowSimple(human_operators_mean_list)" > 新增 </el-button>
                              <el-button class="addBtn" @click="handleMeanNextStep" > 完成 </el-button>
                          </el-dialog>
                          <!-- 直接通过表格增删 human_operators -->
                          <!-- <el-button class="addBtn" type="primary" @click="addRow(human_operators_list)">新增</el-button> -->
                            <template>
                              <el-table border :data="human_operators_list" v-model="params.value" style="width: 100%" >
                                <el-table-column min-width="30%" prop="operateType" label="算子类型">
                                  <template scope="scope">
                                    <!-- <el-input disabled="true" v-model="scope.row.operatorType"></el-input> -->
                                    <el-select disabled="true" v-model="scope.row.operatorType" clearable>
                                      <el-option v-for="(item, index) in operatorTypes"
                                      :key="index" :label="item.name" :value="item.type">
                                      </el-option>
                                    </el-select>
                                  </template>
                                </el-table-column>
                                <el-table-column min-width="40%" prop="columns" label="运算列">
                                  <template scope="scope">
                                    <el-input disabled="true" v-model="scope.row.columns"></el-input>
                                    <!-- <el-select :multiple="scope.row.operatorType==='sum' || scope.row.operatorType==='mean'"
                                    v-model="scope.row.columns" placeholder="请选择运算列">
                                      <el-option
                                        v-for="(item,index) in columnsList" :key="index"
                                        :label="item"
                                        :value="item">
                                      </el-option>
                                    </el-select> -->
                                  </template>
                                </el-table-column>
                                <!-- <el-table-column min-width="20%" fixed="right" label="操作">
                                  <template slot-scope="scope">
                                    <el-button @click.native.prevent="deleteRow(scope.$index, human_operators_list)"
                                    size="small"> 删除 </el-button>
                                  </template>
                                </el-table-column> -->
                              </el-table>
                            </template>
                        </div>
                        <el-input v-else style="width:360px" v-model="params.value"></el-input>
                      </el-form-item>
                    </el-form>
                  </el-card>
                  </el-col>
                  <el-col span="12">
                    <el-card class="card-form">
                        <el-form label-width="150px" label-position="left"  :model="processExtractForm">
                          <el-form-item  label="特征学习">
                              <el-select style="width:360px" @change="handleselectTrainname2"
                              v-model="processExtractForm.operate_name" placeholder="请选择方法">
                                <el-option
                                v-for="(item,index) in algorithm_Options2" :key="index"
                                :label="item.introduction"
                                :value="item.algorithm_name">
                                </el-option>
                            </el-select>
                          </el-form-item>
                          <el-form-item class="label" v-for="(params, index) in algorithm_parameters2" :label="params.introduction" :key="index">
                              <el-select v-if="params.name==='col_retain'" style="width:360px"  :multiple="labelMultible2"
                                v-model="params.value" placeholder="请选择保留列">
                                  <el-option
                                    v-for="(item,index) in columnsList" :key="index"
                                    :label="item"
                                    :value="item">
                                  </el-option>
                              </el-select>
                              <el-input v-else style="width:360px" v-model.number="params.value"></el-input>
                          </el-form-item>
                      </el-form>
                    </el-card>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col span="12">
                    <el-card class="card-form">
                      <el-form label-width="150px" label-position="left"  :model="processDeriveForm">
                        <el-form-item  label="特征衍生">
                          <el-select style="width:360px" @change="handleselectTrainname3"
                                     v-model="processDeriveForm.operate_name" placeholder="请选择方法">
                            <el-option
                              v-for="(item,index) in algorithm_Options3" :key="index"
                              :label="item.introduction"
                              :value="item.algorithm_name">
                            </el-option>
                          </el-select>
                        </el-form-item>
                        <el-form-item class="label" v-for="(params, index) in algorithm_parameters3"
                                      :label="params.introduction" :key="index">
                          <el-select v-if="params.name==='col_retain'" style="width:360px"  :multiple="labelMultible3"
                                     v-model="params.value" placeholder="请选择保留列">
                            <el-option
                              v-for="(item,index) in columnsList" :key="index"
                              :label="item"
                              :value="item">
                            </el-option>
                          </el-select>
                          <el-input v-else style="width:360px" v-model.number="params.value"></el-input>
                        </el-form-item>
                      </el-form>
                    </el-card>
                  </el-col>
                  <el-col span="12">
                    <el-card class="card-form">
                      <el-form label-width="150px" label-position="left"  :model="processSelectionForm">
                        <el-form-item  label="特征选择">
                          <el-select style="width:360px" @change="handleselectTrainname4"
                                     v-model="processSelectionForm.operate_name" placeholder="请选择方法">
                            <el-option
                              v-for="(item,index) in algorithm_Options4" :key="index"
                              :label="item.introduction"
                              :value="item.algorithm_name">
                            </el-option>
                          </el-select>
                        </el-form-item>
                        <el-form-item class="label" v-for="(params, index) in algorithm_parameters4"
                                      :label="params.introduction" :key="index">
                          <el-select v-if="params.name==='col_retain'" style="width:360px"  :multiple="labelMultible4"
                                     v-model="params.value" placeholder="请选择保留列">
                            <el-option
                              v-for="(item,index) in columnsList" :key="index"
                              :label="item"
                              :value="item">
                            </el-option>
                          </el-select>
                          <el-input v-else style="width:360px" v-model.number="params.value"></el-input>
                        </el-form-item>
                      </el-form>
                    </el-card>
                  </el-col>
                </el-row>
              </div>
              <div v-else>
                <el-card class="card-form">
                  <el-form label-width="150px" label-position="left" :model="processConstructForm">
                    <el-form-item  label="特征构建">
                      <el-select style="width:360px" v-model="processConstructForm.operate_name" placeholder="请选择特征"
                                 @change="handleselectTrainname">
                        <el-option
                          v-for="(item,index) in algorithm_Options" :key="index"
                          :label="item.introduction"
                          :value="item.algorithm_name">
                        </el-option>
                      </el-select>
                    </el-form-item >
                    <el-form-item class="label" v-for="(params, index) in algorithm_parameters"
                                  :label="params.introduction" :key="index">
                      <el-select v-if="params.name==='col_retain'" style="width:360px" :multiple="labelMultible"
                                 v-model="params.value" placeholder="请选择保留列">
                        <el-option
                          v-for="(item,index) in columnsList" :key="index"
                          :label="item"
                          :value="item">
                        </el-option>
                      </el-select>
                      <el-checkbox-group v-else-if="params.name==='machine_operators'" style="width:360px"
                                         v-model="machine_operators_list">
                        <el-checkbox :label="'sum'">sum</el-checkbox>
                        <el-checkbox :label="'log'">log</el-checkbox>
                        <el-checkbox :label="'mean'">mean</el-checkbox>
                      </el-checkbox-group>
                      <!-- 基于算子 人在回路特征工程的参数 -->
                    </el-form-item>
                  </el-form>
                </el-card>
                <el-card class="card-form">
                  <el-form label-width="150px" label-position="left"  :model="processExtractForm">
                    <el-form-item  label="特征提取">
                      <el-select style="width:360px" @change="handleselectTrainname2"
                                 v-model="processExtractForm.operate_name" placeholder="请选择特征">
                        <el-option
                          v-for="(item,index) in algorithm_Options2" :key="index"
                          :label="item.introduction"
                          :value="item.algorithm_name">
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item class="label" v-for="(params, index) in algorithm_parameters2"
                                  :label="params.introduction" :key="index">
                      <el-select v-if="params.name==='col_retain'" style="width:360px"  :multiple="labelMultible2"
                                 v-model="params.value" placeholder="请选择保留列">
                        <el-option
                          v-for="(item,index) in columnsList" :key="index"
                          :label="item"
                          :value="item">
                        </el-option>
                      </el-select>
                      <el-input v-else style="width:360px" v-model.number="params.value"></el-input>
                    </el-form-item>
                  </el-form>
                </el-card>
              </div>
            </el-form-item>
            <el-form-item class="label" label="新数据集名称" prop="new_dataset_name" >
              <el-input style="width:610px" clearable  v-model="addFeatureForm.new_dataset_name" placeholder="请填写新数据集名称"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitHumanForm">立即创建</el-button>
              <!-- <el-button>取消</el-button> -->
            </el-form-item>
      </el-form>
    </el-card>
    <!--      选择数据集，弹出的窗口-->
  </div>
</template>
<script>
import featureApi from './../../api/feature'
// import learnApi from './../../api/learn'
import humanApi from './../../api/HumanFea'
import learnApi from './../../api/learn'
// 所属运行方式
const runModeOptions = [
  { type: '1', name: '1' }
]
// 生成方式类型
const featureEngTypeOptions = [
  { type: 'Manual', name: '人工特征工程' },
  { type: 'Machine', name: '自动化特征工程' },
  { type: 'HumanInLoop', name: '人机协同特征学习与衍生技术' }
]
// 余娜 基于算子的特征构建 人在回路 算子类型
const operatorTypes = [
  { type: 'sum', name: '求和' },
  { type: 'log', name: '对数' },
  { type: 'mean', name: '均值' }
]

export default {
  name: 'HumanFea',

  data () {
    return {
      activeIndex: '0',
      // 表单
      addFeatureForm: {
        // 特征工程名
        featureEng_name: '',
        // 特征工程类型
        featureEng_type: '',
        featureEng_processes: [
        ],
        original_dataset_id: '',
        original_dataset_name: '',
        new_dataset_name: '',
        // 运行方式
        run_mode: ''
      },
      featureEngTypeOptions,
      runModeOptions,
      operate_nameValue1: '',
      operate_columnsValue1: [],
      operate_columnsValue2: [],
      operate_columnsValue3: [],
      operate_columnsValue4: [],
      operate_nameValue2: '',
      operate_nameValue3: '',
      operate_nameValue4: '',
      n_componentsValue: 1,
      algorithm_name: [],
      algorithm_name2: [],
      algorithm_name3: [],
      algorithm_name4: [],
      addFeatureFormRules: {
        featureEng_name: [
          { required: true, message: '请填写特征工程名', trigger: 'blur' }
        ],
        featureEng_type: [
          { required: true, message: '请选择特征工程类型', trigger: 'blur' }
        ]
      },
      // 在特征首页选择的数据集及其列名
      OriginDatasetId: '',
      OriginDatasetName: '',
      columnsList: [],
      algorithm_category: 'FeatureEng_construct',
      // 根据算法类型收到的算法总数据
      algorithm_originalOptions: [],
      algorithm_Options: [{ algorithm_name: 'FactorGraph', introduction: '基于因子图的特征解耦' }],
      // 算法参数
      algorithm_parameters: {},
      // 余娜 基于算子的特征构建方法 人在回路特征工程的参数
      machine_operators_list: ['sum'],
      human_operators_list: [],
      human_operators_sum_list: [{ columns: [] }],
      human_operators_log_list: [{ columns: [] }],
      human_operators_mean_list: [{ columns: [] }],
      // sum, log, mean算子弹窗
      dialogSumVisible: false,
      dialogLogVisible: false,
      dialogMeanVisible: false,
      operatorTypes,
      labelMultible: false,
      algorithm_category2: 'FeatureEng_extract',
      // 根据算法类型收到的算法总数据
      algorithm_originalOptions2: [],
      algorithm_originalOptions4: [],
      algorithm_Options2: [{ algorithm_name: 'FactorGraph', introduction: '基于GNN的特征提取' }],
      algorithm_Options3: [],
      algorithm_Options4: [],
      // 算法参数
      // algorithm_parameters2: [{ introduction: '保留列', name: 'col_retain', value: '' }, { introduction: '维度', name: 'dimension', value: '' }, { introduction: '迭代数', name: 'iteration', value: '' }],
      algorithm_parameters2: [],
      algorithm_parameters3: [],
      algorithm_parameters4: [],
      labelMultible2: false,
      labelMultible3: false,
      labelMultible4: false,
      processConstructForm: {
        operate_name: ''
      },
      processExtractForm: {
        operate_name: ''
      },
      processDeriveForm: {
        operate_name: ''
      },
      processSelectionForm: {
        operate_name: ''
      }
    }
  },
  created () {
    this.getOriginDatasetId()
    this.getAlgorithm()
  },
  methods: {
    backPage () {
      this.$router.back()
    },
    // 点击确定按钮，提交上传数据表单
    submitHumanForm () {
      console.log(this.processExtractForm.algorithm_parameters2)
      console.log(this.processConstructForm.algorithm_parameters)
      // 调整了一下位置
      // 处理一下特征构建的参数
      if (this.processConstructForm.algorithm_parameters !== undefined) {
        for (let i = 0; i < this.processConstructForm.algorithm_parameters.length; i++) {
          if (this.processConstructForm.algorithm_parameters[i].name === 'human_operators') {
            // 基于算子 人在回路
            this.processConstructForm.algorithm_parameters[i].value = this.human_operators_list
          }
          if (this.processConstructForm.algorithm_parameters[i].name === 'machine_operators') {
            // 基于算子 自动化（机器）
            this.processConstructForm.algorithm_parameters[i].value = this.machine_operators_list
          }
          this.processConstructForm[this.processConstructForm.algorithm_parameters[i].name] = this.processConstructForm.algorithm_parameters[i].value
        }
        this.addFeatureForm.featureEng_processes.push(this.processConstructForm)
      }
      // 处理一下特征提取的参数
      if (this.processExtractForm.algorithm_parameters2 !== undefined) {
        for (let i = 0; i < this.processExtractForm.algorithm_parameters2.length; i++) {
          this.processExtractForm[this.processExtractForm.algorithm_parameters2[i].name] = this.processExtractForm.algorithm_parameters2[i].value
        }
        this.addFeatureForm.featureEng_processes.push(this.processExtractForm)
      }

      this.addFeatureForm.original_dataset_id = this.OriginDatasetId
      this.$refs.addFeatureFormRef.validate(valid => {
        if (valid) {
          console.log(this.addFeatureForm)
          humanApi.add(this.addFeatureForm).then(response => {
            const resp = response.data
            console.log(response)
            if (resp.meta.code === 204) {
              this.$message.success('添加特征工程成功')
            } else {
              this.$message.error('添加特征工程失败')
            }
          })
        }
      })
    },
    // 获取数据集列名
    getColumns () {
      featureApi.getDatasetColumns(this.OriginDatasetId).then(response => {
        // console.log(response)
        const resp = response.data
        if (resp.meta.code === 200) {
          this.$message.success('获取数据集成功')
        }
        this.columnsList = resp.data
      })
    },
    // 获取原始数据集id
    getOriginDatasetId () {
      this.OriginDatasetId = localStorage.getItem('datasetId')
      this.OriginDatasetName = localStorage.getItem('datasetName')
      this.addFeatureForm.original_dataset_name = this.OriginDatasetName
      // console.log(this.OriginDatasetId)
      this.getColumns()
      // console.log(db)
    },
    // 点击查看特征工程按钮
    queryFeatureEng () {
      this.$router.push('/feature/queryFea')
    },
    // 通过算法接口动态获取参数
    getAlgorithm () {
      learnApi.queryAlgorithm(this.algorithm_category).then(response => {
        this.algorithm_originalOptions = response.data.data
        this.algorithm_name = response.data.data.map(item => item.algorithm_name)
        // console.log(this.algorithm_Options)
      })
      learnApi.queryAlgorithm(this.algorithm_category2).then(response => {
        this.algorithm_originalOptions2 = response.data.data
        this.algorithm_name2 = response.data.data.map(item => item.algorithm_name)
        // console.log(this.algorithm_name2)
      })
      // learnApi.queryAlgorithm(this.algorithm_category2).then(response => {
      //   this.algorithm_Options3 = response.data.data
      //   for (let i = 0; i < this.algorithm_Options3.length; i++) {
      //     this.algorithm_name3.push({
      //       algorithm_name: this.algorithm_Options3[i].algorithm_name,
      //       algorithm_id: this.algorithm_Options3[i].algorithm_id
      //     })
      //   }
      //   // this.algorithm_name2 = response.data.data.map(item => item.algorithm_name)
      //   console.log(this.algorithm_name3)
      // })
    },
    handleFeatureEngType () {
      // this.processConstructForm.operate_name = ''
      // this.processExtractForm.operate_name = ''
      // this.processConstructForm.algorithm_parameters = {}
      // this.processExtractForm.algorithm_parameters2 = {}
      // this.algorithm_parameters = {}
      // this.algorithm_parameters2 = {}
      // this.algorithm_Options = this.algorithm_originalOptions.filter((p) => {
      //   return p.algorithm_type === this.addFeatureForm.featureEng_type
      // })
      // console.log(this.addFeatureForm.featureEng_type)
      // console.log(this.algorithm_originalOptions)
      // console.log(this.algorithm_Options)
      // this.algorithm_Options2 = this.algorithm_originalOptions2.filter((p) => {
      //   return p.algorithm_type === this.addFeatureForm.featureEng_type
      // })
      // console.log(this.addFeatureForm.featureEng_type)
      // console.log(this.algorithm_originalOptions2)
      // console.log(this.algorithm_Options2)
    },
    // 当选择标签选择框没有先选择方法的时候，
    handleselect () {
      if (this.operate_nameValue1 === '') {
        this.$message.error('请先选择方法')
        this.columnsList = []
      }
    },
    // 当选择标签选择框没有先选择方法的时候，
    handleselect2 () {
      if (this.operate_nameValue2 === '') {
        this.$message.error('请先选择方法')
        this.columnsList = []
      }
    },
    // 当训练方法发生改变的时候
    handleselectTrainname () {
      // this.getColumns()
      for (let i = 0; i < this.algorithm_Options.length; i++) {
        if (this.algorithm_Options[i].algorithm_name === this.processConstructForm.operate_name) {
          // 首先，将返回的json格式转换一下
          // this.algorithm_parameters = JSON.parse(this.algorithm_Options[i].algorithm_parameters)
          // 暂时用假数据
          this.algorithm_parameters = [{ introduction: '保留列', name: 'col_retain', value: '' }, { introduction: '维度', name: 'dimension', value: '' }, { introduction: '迭代数', name: 'iteration', value: '' }]
          // 然后，将他放到表单中，防止表单没有这个，最后在提交的时候，将里面的列取出来就好了
          this.processConstructForm.algorithm_parameters = this.algorithm_parameters
          console.log(this.algorithm_parameters)
          // 如果是保留列，就是下拉选择，就要判断单选和多选
          for (let i = 0; i < this.algorithm_parameters.length; i++) {
            if (this.algorithm_parameters[i].name === 'col_retain') {
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

    handleselectTrainname3 () {

    },
    handleselectTrainname4 () {

    },
    // 删除行
    deleteRow (index, rows) {
      rows.splice(index, 1)
    },
    // 新增行
    addRow (tableData, event) {
      tableData.push({ operatorType: 'sum', columns: [] })
    },
    // 新增行,sum,log,mean
    addRowSimple (tableData, event) {
      tableData.push({ columns: [] })
    },
    clearHumanOperators3list () {
      this.human_operators_sum_list = [{ columns: [] }]
      this.human_operators_log_list = [{ columns: [] }]
      this.human_operators_mean_list = [{ columns: [] }]
    },
    handleSumNextStep () {
      this.dialogSumVisible = false
      this.dialogLogVisible = true
    },
    handleLogNextStep () {
      this.dialogLogVisible = false
      this.dialogMeanVisible = true
    },
    handleMeanNextStep () {
      // 完成
      this.dialogMeanVisible = false
      // 数据转换
      this.human_operators_list = []
      for (let i = 0; i < this.human_operators_sum_list.length; i++) {
        this.human_operators_list.push({ operatorType: 'sum', columns: this.human_operators_sum_list[i].columns })
      }
      for (let i = 0; i < this.human_operators_log_list.length; i++) {
        this.human_operators_list.push({ operatorType: 'log', columns: this.human_operators_log_list[i].columns })
      }
      for (let i = 0; i < this.human_operators_mean_list.length; i++) {
        this.human_operators_list.push({ operatorType: 'mean', columns: this.human_operators_mean_list[i].columns })
      }
    },
    // 当训练方法发生改变的时候
    handleselectTrainname2 () {
      // this.getColumns()
      for (let i = 0; i < this.algorithm_Options2.length; i++) {
        if (this.algorithm_Options2[i].algorithm_name === this.processExtractForm.operate_name) {
          // this.algorithm_parameters2 = JSON.parse(this.algorithm_Options2[i].algorithm_parameters
          // 暂时用假数据
          this.algorithm_parameters2 = [{ introduction: '保留列', name: 'col_retain', value: '' }, { introduction: '维度', name: 'dimension', value: '' }, { introduction: '迭代数', name: 'iteration', value: '' }]
          this.processExtractForm.algorithm_parameters2 = this.algorithm_parameters2
          console.log(this.algorithm_parameters2)
          for (let i = 0; i < this.algorithm_parameters2.length; i++) {
            if (this.algorithm_parameters2[i].name === 'col_retain') {
              if (this.algorithm_parameters2[i].select === 'single-select') {
                this.labelMultible2 = false
              } else {
                this.labelMultible2 = true
              }
            }
          }
        }
      }
    }
    // // 当训练方法发生改变的时候
    // handleselectTrainname2 () {
    //   this.getColumns()
    //   for (let i = 0; i < this.algorithm_Options2.length; i++) {
    //     // console.log(this.algorithm_Options2[i].algorithm_name)
    //     if (this.algorithm_Options2[i].algorithm_name === this.processExtractForm.operate_name) {
    //       // this.algorithm_parameters2 = [
    //       //   {
    //       //     name: 'col1',
    //       //     value: ''
    //       //   },
    //       //   {
    //       //     name: 'col2',
    //       //     value: ''
    //       //   }
    //       // ]

    //       this.algorithm_parameters2 = JSON.parse(this.algorithm_Options2[i].algorithm_parameters)
    //       // for (let i = 0; i < this.algorithm_parameters2.length; i++) {
    //       //   // console.log(this.algorithm_parameters2[i])
    //       //   this.processExtractForm[this.algorithm_parameters2[i].name] = this.algorithm_parameters2[i].value
    //       // }

    //       this.processExtractForm.algorithm_parameters2 = this.algorithm_parameters2

    //       // this.paramsKeys = Object.keys(this.algorithm_parameters2)
    //       // this.paramsKeys.forEach(item => {
    //       //   this.processExtractForm[item] = ''
    //       // })
    //       // console.log(this.paramsKeys)
    //       console.log(this.algorithm_parameters2)
    //       // if (this.algorithm_parameters2.col_retain.select === 'single-select') {
    //       //   this.labelMultible2 = false
    //       // } else {
    //       //   this.labelMultible2 = true
    //       // }
    //     }
    //   }
    // }
  }
}
</script>
<style scoped>
.queryBtn{
  float: right;
  width: 120px;
  margin-bottom: 20px;
}
.addBtn{
  margin-top: 10px;
  margin-bottom: 10px;
  margin-left: 10px;
  margin-right: 10px;
}
  .el-form-item{
    margin-top: 20px;
  }
  h3{
    padding-bottom: 10px;
    border-bottom: 2px solid rgb(57, 65, 167);
    width: 450px;
  }
  .card-form {
    width:610px;
    box-shadow: none;
  }
</style>
