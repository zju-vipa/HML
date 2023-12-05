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
                <el-option v-for="(option, index) in runModeOptions" :key="index" :label="option.label" :value="option.value">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item class="label" label="特征工程类型" prop="featureEng_type">
              <el-radio-group v-model="addFeatureForm.featureEng_type" style="width:610px">
                <el-radio v-for="(option, index) in featureEngTypeOptions" :key="index" :label="option.value" :value="option.value" @change="handleFeatureEngType">{{option.label}}</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item v-if="addFeatureForm.featureEng_type === 'HumanInLoop'" class="label" label="功能模块选择" prop="featureEng_modules">
              <el-checkbox-group v-model="addFeatureForm.checkedModules" @change="handleCheckedChange">
                <el-checkbox v-for="(item, index) in moduleOptions" :label="item.value" :key="index" :value="item.value">{{item.label}}</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item class="label" label="技术方法配置" prop="featureEng_processes">
<!--              <div v-if="addFeatureForm.featureEng_type==''">-->
<!--                <span style="color: darkgray">请先选择特征工程类型</span>-->
<!--              </div>-->
<!--              <div v-else-if="addFeatureForm.featureEng_type=='HumanInLoop'">-->
              <div v-if="addFeatureForm.featureEng_type === 'HumanInLoop'">
                <el-row>
                  <el-col span="12">
                    <el-card class="card-form">
                      <el-col span="4">
                        <span>特征解耦</span>
                      </el-col>
                      <el-col span="14">
                        <el-select v-model="processDecouplingForm.operate_name" placeholder="请选择方法" @change="handleselectTrainname" :disabled="!addFeatureForm.checkedModules.includes('1')">
                          <el-option
                            v-for="(item,index) in algorithm_Options1" :key="index"
                            :label="item.introduction"
                            :value="item.algorithm_name">
                          </el-option>
                         </el-select>
                      </el-col>
                      <el-col span="6">
                        <el-button type="mini" :disabled="!addFeatureForm.checkedModules.includes('1')" @click="showDecouplingSetting">参数配置</el-button>
                      </el-col>
                  </el-card>
                  </el-col>
                  <el-col span="12">
                    <el-card class="card-form">
                      <el-col span="4">
                        <span>特征学习</span>
                      </el-col>
                      <el-col span="14">
                        <el-select v-model="processLearningForm.operate_name" placeholder="请选择方法" @change="handleselectTrainname2" :disabled="!addFeatureForm.checkedModules.includes('2')">
                          <el-option
                            v-for="(item,index) in algorithm_Options2" :key="index"
                            :label="item.introduction"
                            :value="item.algorithm_name">
                          </el-option>
                        </el-select>
                      </el-col>
                      <el-col span="6">
                        <el-button type="mini" :disabled="!addFeatureForm.checkedModules.includes('2')" @click="showLearningSetting">参数配置</el-button>
                      </el-col>
                    </el-card>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col span="12">
                    <el-card class="card-form">
                      <el-col span="4">
                        <span>特征衍生</span>
                      </el-col>
                      <el-col span="14">
                        <el-select v-model="processDeriveForm.operate_name" placeholder="请选择方法" @change="handleselectTrainname3" :disabled="!addFeatureForm.checkedModules.includes('3')">
                          <el-option
                            v-for="(item,index) in algorithm_Options3" :key="index"
                            :label="item.introduction"
                            :value="item.algorithm_name">
                          </el-option>
                        </el-select>
                      </el-col>
                      <el-col span="6">
                        <el-button type="mini" :disabled="!addFeatureForm.checkedModules.includes('3')" @click="showDeriveSetting">参数配置</el-button>
                      </el-col>
                    </el-card>
                  </el-col>
                  <el-col span="12">
                    <el-card class="card-form">
                      <el-col span="4">
                        <span>特征选择</span>
                      </el-col>
                      <el-col span="14">
                        <el-select v-model="processSelectionForm.operate_name" placeholder="请选择方法" @change="handleselectTrainname4" :disabled="!addFeatureForm.checkedModules.includes('4')">
                          <el-option
                            v-for="(item,index) in algorithm_Options4" :key="index"
                            :label="item.introduction"
                            :value="item.algorithm_name">
                          </el-option>
                        </el-select>
                      </el-col>
                      <el-col span="6">
                        <el-button type="mini" :disabled="!addFeatureForm.checkedModules.includes('4')" @click="showSelectionSetting">参数配置</el-button>
                      </el-col>
                    </el-card>
                  </el-col>
                </el-row>
              </div>
              <div v-if="addFeatureForm.featureEng_type === 'Manual'">
                <el-row style="width: 600px">
                  <el-card class="card-form">
                    <el-col span="4">
                      <span>特征构建</span>
                    </el-col>
                    <el-col span="14">
                      <el-select v-model="processConstructForm.operate_name" placeholder="请选择方法" @change="handleselectTrainname5">
                        <el-option
                          v-for="(item,index) in algorithm_Options5" :key="index"
                          :label="item.introduction"
                          :value="item.algorithm_name">
                        </el-option>
                      </el-select>
                    </el-col>
                    <el-col span="6">
                      <el-button type="mini" @click="showConstructSetting">参数配置</el-button>
                    </el-col>
                  </el-card>
                </el-row>
<!--                <el-row style="width: 600px">-->
<!--                  <el-card class="card-form">-->
<!--                    <el-col span="4">-->
<!--                      <span>特征提取</span>-->
<!--                    </el-col>-->
<!--                    <el-col span="14">-->
<!--                      <el-select v-model="processExtractForm.operate_name" placeholder="请选择方法" @change="handleselectTrainname6">-->
<!--                        <el-option-->
<!--                          v-for="(item,index) in algorithm_Options6" :key="index"-->
<!--                          :label="item.introduction"-->
<!--                          :value="item.algorithm_name">-->
<!--                        </el-option>-->
<!--                      </el-select>-->
<!--                    </el-col>-->
<!--                    <el-col span="6">-->
<!--                      <el-button type="mini" @click="showExtractSetting">参数配置</el-button>-->
<!--                    </el-col>-->
<!--                  </el-card>-->
<!--                </el-row>-->
              </div>
              <div v-if="addFeatureForm.featureEng_type === 'Machine'">
                <el-row style="width: 600px">
                  <el-card class="card-form">
                    <el-col span="4">
                      <span>特征生成</span>
                    </el-col>
                    <el-col span="14">
                      <el-select v-model="processGenerationForm.operate_name" placeholder="请选择方法" @change="handleselectTrainname7">
                        <el-option
                          v-for="(item,index) in algorithm_Options7" :key="index"
                          :label="item.introduction"
                          :value="item.algorithm_name">
                        </el-option>
                      </el-select>
                    </el-col>
                    <el-col span="6">
                      <el-button type="mini" @click="showGenerationSetting">参数配置</el-button>
                    </el-col>
                  </el-card>
                </el-row>
              </div>
<!--              <div v-else>-->
<!--                <el-card class="card-form">-->
<!--                  <el-form label-width="150px" label-position="left" :model="processConstructForm">-->
<!--                    <el-form-item  label="特征构建">-->
<!--                      <el-select style="width:360px" v-model="processConstructForm.operate_name" placeholder="请选择特征"-->
<!--                                 @change="handleselectTrainname">-->
<!--                        <el-option-->
<!--                          v-for="(item,index) in algorithm_Options" :key="index"-->
<!--                          :label="item.introduction"-->
<!--                          :value="item.algorithm_name">-->
<!--                        </el-option>-->
<!--                      </el-select>-->
<!--                    </el-form-item >-->
<!--                    <el-form-item class="label" v-for="(params, index) in algorithm_parameters"-->
<!--                                  :label="params.introduction" :key="index">-->
<!--                      <el-select v-if="params.name==='col_retain'" style="width:360px" :multiple="labelMultible"-->
<!--                                 v-model="params.value" placeholder="请选择保留列">-->
<!--                        <el-option-->
<!--                          v-for="(item,index) in columnsList" :key="index"-->
<!--                          :label="item"-->
<!--                          :value="item">-->
<!--                        </el-option>-->
<!--                      </el-select>-->
<!--                      <el-checkbox-group v-else-if="params.name==='machine_operators'" style="width:360px"-->
<!--                                         v-model="machine_operators_list">-->
<!--                        <el-checkbox :label="'sum'">sum</el-checkbox>-->
<!--                        <el-checkbox :label="'log'">log</el-checkbox>-->
<!--                        <el-checkbox :label="'mean'">mean</el-checkbox>-->
<!--                      </el-checkbox-group>-->
<!--                      &lt;!&ndash; 基于算子 人在回路特征工程的参数 &ndash;&gt;-->
<!--                    </el-form-item>-->
<!--                  </el-form>-->
<!--                </el-card>-->
<!--                <el-card class="card-form">-->
<!--                  <el-form label-width="150px" label-position="left"  :model="processExtractForm">-->
<!--                    <el-form-item  label="特征提取">-->
<!--                      <el-select style="width:360px" @change="handleselectTrainname2"-->
<!--                                 v-model="processExtractForm.operate_name" placeholder="请选择特征">-->
<!--                        <el-option-->
<!--                          v-for="(item,index) in algorithm_Options2" :key="index"-->
<!--                          :label="item.introduction"-->
<!--                          :value="item.algorithm_name">-->
<!--                        </el-option>-->
<!--                      </el-select>-->
<!--                    </el-form-item>-->
<!--                    <el-form-item class="label" v-for="(params, index) in algorithm_parameters2"-->
<!--                                  :label="params.introduction" :key="index">-->
<!--                      <el-select v-if="params.name==='col_retain'" style="width:360px"  :multiple="labelMultible2"-->
<!--                                 v-model="params.value" placeholder="请选择保留列">-->
<!--                        <el-option-->
<!--                          v-for="(item,index) in columnsList" :key="index"-->
<!--                          :label="item"-->
<!--                          :value="item">-->
<!--                        </el-option>-->
<!--                      </el-select>-->
<!--                      <el-input v-else style="width:360px" v-model.number="params.value"></el-input>-->
<!--                    </el-form-item>-->
<!--                  </el-form>-->
<!--                </el-card>-->
<!--              </div>-->
            </el-form-item>
            <el-form-item class="label" label="新数据集名称" prop="new_dataset_name" >
              <el-input style="width:610px" clearable  v-model="addFeatureForm.new_dataset_name" placeholder="请填写新数据集名称"></el-input>
            </el-form-item>
            <el-form-item>
              <el-row>
                <el-button type="primary" @click="submitHumanForm">立即创建</el-button>
                <el-button type="success" @click="showExistedFeatureEng"><i class="el-icon-upload el-icon--right"></i>导入已有特征工程</el-button>
              </el-row>

              <!-- <el-button>取消</el-button> -->
            </el-form-item>
      </el-form>
    </el-card>
    <!--特征解耦参数配置，弹出的窗口-->
    <el-dialog
      title="特征解耦参数配置"
      :visible.sync="featureDecouplingDialog"
      width="30%">
      <el-form label-width="150px" label-position="left" :model="processDecouplingForm">
        <el-form-item class="label" v-for="(params, index) in algorithm_parameters1" :label="params.introduction" :key="index">
          <el-select v-if="params.name==='col_retain'" style="width:100%"  :multiple="labelMultible1"
                     v-model="params.value" placeholder="请选择保留列">
            <el-option
              v-for="(item,index) in columnsList" :key="index"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
          <el-input v-else style="width:100%" v-model.number="params.value"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="featureDecouplingDialog = false">取 消</el-button>
        <el-button type="primary" @click="submitDecouplingParams">确 定</el-button>
      </div>
    </el-dialog>
    <!--特征学习参数配置，弹出的窗口-->
    <el-dialog
      title="特征学习参数配置"
      :visible.sync="featureLearningDialog"
      width="30%">
      <el-form label-width="150px" label-position="left" :model="processLearningForm">
        <el-form-item class="label" v-for="(params, index) in algorithm_parameters2" :label="params.introduction" :key="index">
          <el-select v-if="params.name==='col_retain'" style="width:100%"  :multiple="labelMultible2"
                     v-model="params.value" placeholder="请选择保留列">
            <el-option
              v-for="(item,index) in columnsList" :key="index"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
          <el-input v-else style="width:100%" v-model.number="params.value"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="featureLearningDialog = false">取 消</el-button>
        <el-button type="primary" @click="submitLearningParams">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      title="已有特征工程"
      :visible.sync="existedFeatureEng"
      width="70%">
      <el-table
        :data="HumanFeaData"
        border stripe
        ref="featureEng_list_table"
        height="550"
        style="font-size: 15px"
        @row-click="importFeatureEng"
        solt="append">
        <el-table-column  label="序号" type="index" style="font-weight: bolder"> </el-table-column>
        <el-table-column prop="featureEng_name" label="特征工程名" style="font-weight: bolder"> </el-table-column>
        <el-table-column prop="featureEng_type" label="特征工程类型" style="font-weight: bolder"> </el-table-column>
        <el-table-column prop="featureEng_result" label="任务效果" style="font-weight: bolder">
          <template slot-scope="scope">
            <el-progress
              v-if="scope.row.featureEng_accuracy!=null"
              type="line"
              :stroke-width="10"
              :percentage="scope.row.featureEng_accuracy"
              color="green">
            </el-progress>
            <span v-else>
              暂无数据
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="featureEng_efficiency" label="特征有效率">
          <template slot-scope="scope">
            <el-progress
              v-if="scope.row.featureEng_efficiency!=null"
              type="line"
              :stroke-width="10"
              :percentage="scope.row.featureEng_efficiency"
              :color="blue">
            </el-progress>
            <span v-else>
              暂无数据
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="operate_state" label="状态">
          <template slot-scope="scope">
            <span v-if="scope.row.operate_state==='已完成'" style="color: green">已完成</span>
            <span v-else-if="scope.row.operate_state==='交互中'"  style="color: orange">交互中</span>
            <span v-else-if="scope.row.operate_state==='已停止'"  style="color: orange">交互中</span>
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="existedFeatureEng = false">取 消</el-button>
      </div>
    </el-dialog>
    <!--特征解耦参数配置，弹出的窗口-->
    <el-dialog
      title="特征构建参数配置"
      :visible.sync="featureConstructDialog"
      width="30%">
      <el-form label-width="150px" label-position="left" :model="processConstructForm">
        <el-form-item class="label" v-for="(params, index) in algorithm_parameters5" :label="params.introduction" :key="index">
          <el-select v-if="params.name==='col_retain'" style="width:100%"  :multiple="labelMultible5"
                     v-model="params.value" placeholder="请选择保留列">
            <el-option
              v-for="(item,index) in columnsList" :key="index"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
          <el-input v-else style="width:100%" v-model.number="params.value"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="featureConstructDialog = false">取 消</el-button>
        <el-button type="primary" @click="submitConstructParams">确 定</el-button>
      </div>
    </el-dialog>
    <!--特征提取参数配置，弹出的窗口-->
    <el-dialog
      title="特征提取参数配置"
      :visible.sync="featureExtractDialog"
      width="30%">
      <el-form label-width="150px" label-position="left" :model="processExtractForm">
        <el-form-item class="label" v-for="(params, index) in algorithm_parameters6" :label="params.introduction" :key="index">
          <el-select v-if="params.name==='col_retain'" style="width:100%"  :multiple="labelMultible6"
                     v-model="params.value" placeholder="请选择保留列">
            <el-option
              v-for="(item,index) in columnsList" :key="index"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
          <el-input v-else style="width:100%" v-model="params.value"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="featureExtractDialog = false">取 消</el-button>
        <el-button type="primary" @click="submitExtractParams">确 定</el-button>
      </div>
    </el-dialog>
    <!--机器学习--参数配置，弹出的窗口-->
    <el-dialog
      title="特征提取参数配置"
      :visible.sync="featureGenerationDialog"
      width="30%">
      <el-form label-width="150px" label-position="left" :model="processGenerationForm">
        <el-form-item class="label" v-for="(params, index) in algorithm_parameters7" :label="params.introduction" :key="index">
          <el-input style="width:100%" v-model="params.value"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="featureGenerationDialog = false">取 消</el-button>
        <el-button type="primary" @click="submitGenerationParams">确 定</el-button>
      </div>
    </el-dialog>
    <!--特征衍生参数配置-->
    <el-dialog
      title="特征衍生参数配置"
      :visible.sync="featureDeriveDialog"
      width="30%">
<!--      <el-form label-width="150px" label-position="left" :model="processDeriveForm">-->
<!--        <el-form-item class="label" v-for="(params, index) in algorithm_parameters3" :label="params.introduction" :key="index">-->
<!--          <el-select v-if="params.name==='col_retain'" style="width:100%"  :multiple="labelMultible6"-->
<!--                     v-model="params.value" placeholder="请选择保留列">-->
<!--            <el-option-->
<!--              v-for="(item,index) in columnsList" :key="index"-->
<!--              :label="item"-->
<!--              :value="item">-->
<!--            </el-option>-->
<!--          </el-select>-->
<!--          <el-input v-else style="width:100%" v-model="params.value"></el-input>-->
<!--        </el-form-item>-->
<!--      </el-form>-->
<!--      <div slot="footer" class="dialog-footer">-->
<!--        <el-button @click="featureExtractDialog = false">取 消</el-button>-->
<!--        <el-button type="primary" @click="submitExtractParams">确 定</el-button>-->
<!--      </div>-->
      <span>暂无内容</span>
      <div slot="footer" class="dialog-footer">
        <el-button @click="featureDeriveDialog = false">确定</el-button>
      </div>
    </el-dialog>
    <!--特征选择参数配置-->
    <el-dialog
      title="特征选择参数配置"
      :visible.sync="featureSelectionDialog"
      width="30%">
      <!--      <el-form label-width="150px" label-position="left" :model="processDeriveForm">-->
      <!--        <el-form-item class="label" v-for="(params, index) in algorithm_parameters3" :label="params.introduction" :key="index">-->
      <!--          <el-select v-if="params.name==='col_retain'" style="width:100%"  :multiple="labelMultible6"-->
      <!--                     v-model="params.value" placeholder="请选择保留列">-->
      <!--            <el-option-->
      <!--              v-for="(item,index) in columnsList" :key="index"-->
      <!--              :label="item"-->
      <!--              :value="item">-->
      <!--            </el-option>-->
      <!--          </el-select>-->
      <!--          <el-input v-else style="width:100%" v-model="params.value"></el-input>-->
      <!--        </el-form-item>-->
      <!--      </el-form>-->
      <!--      <div slot="footer" class="dialog-footer">-->
      <!--        <el-button @click="featureExtractDialog = false">取 消</el-button>-->
      <!--        <el-button type="primary" @click="submitExtractParams">确 定</el-button>-->
      <!--      </div>-->
      <span>暂无内容</span>
      <div slot="footer" class="dialog-footer">
        <el-button @click="featureSelectionDialog = false">确定</el-button>
      </div>
    </el-dialog>
    <!--查看特征工程进度-->
    <el-dialog title="特征工程进度" :visible.sync="featureEngDialogVisible">
      <el-progress
        type="line"
        :stroke-width="10"
        :percentage="percentage"
        color="green">
      </el-progress>
      <span>{{taskMessage}}</span>
      <div slot="footer" class="dialog-footer">
        <el-button @click="clear">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import featureApi from './../../api/feature'
import humanFeaApi from './../../api/HumanFea'
import featureEngApi from './../../api/queryFea'
// 所属运行方式
const runModeOptions = [
  { value: '1', label: '001夏平初始' }
]
// 生成方式类型
const featureEngTypeOptions = [
  { value: 'Manual', label: '纯人工方法' },
  { value: 'Machine', label: '纯机器方法' },
  { value: 'HumanInLoop', label: '人机协同特征学习与衍生技术' }
]
// 余娜 基于算子的特征构建 人在回路 算子类型
const operatorTypes = [
  { value: 'sum', label: '求和' },
  { value: 'log', label: '对数' },
  { value: 'mean', label: '均值' }
]
const moduleOptions = [
  { value: '1', label: '特征解耦' },
  { value: '2', label: '特征学习' },
  { value: '3', label: '特征衍生' },
  { value: '4', label: '特征选择' }
]

export default {
  name: 'HumanFea',
  data () {
    return {
      percentage: 0,
      taskMessage: 'test',
      activeIndex: '0',
      featureEngDialogVisible: false,
      // 表单
      addFeatureForm: {
        // 特征工程名
        featureEng_name: '',
        // 特征工程类型
        featureEng_type: 'HumanInLoop',
        featureEng_processes: [],
        original_dataset_id: '',
        original_dataset_name: '',
        new_dataset_name: '',
        // 运行方式
        run_mode: '1',
        checkedModules: ['1', '2', '3', '4']
      },
      featureEngTypeOptions,
      runModeOptions,
      moduleOptions,
      operate_columnsValue1: [],
      operate_columnsValue2: [],
      operate_columnsValue3: [],
      operate_columnsValue4: [],
      operate_nameValue1: '',
      operate_nameValue2: '',
      operate_nameValue3: '',
      operate_nameValue4: '',
      n_componentsValue: 1,
      algorithm_name1: [],
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
      pagination_featureEngList: {
        page: 1,
        pageSize: 20,
        total: 0
      },
      // 在特征首页选择的数据集及其列名
      OriginDatasetId: '',
      OriginDatasetName: '',
      columnsList: [],
      algorithm_category: 'FeatureEng_construct',
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
      algorithm_category2: 'FeatureEng_extract',
      // 三种特征工程类型，根据算法类型收到的算法总数据
      algorithm_originalOptions1: [],
      algorithm_originalOptions2: [],
      algorithm_originalOptions3: [],
      // 四个模块，选择的算法
      algorithm_Options1: [{ algorithm_name: 'FactorGNN', introduction: '基于因子图的特征解耦' }],
      algorithm_Options2: [{ algorithm_name: 'GNN', introduction: '基于GNN的特征提取' }],
      algorithm_Options3: [{ algorithm_name: 'HumanMachineCooperation', introduction: '人机协同特征生成' }],
      algorithm_Options4: [{ algorithm_name: 'ModelBased', introduction: '基于模型的特征选择' }],
      algorithm_Options5: [{ algorithm_name: 'OperatorBased-Manual', introduction: '基于专家经验的特征构建' }],
      algorithm_Options6: [{ algorithm_name: 'PCA', introduction: 'PCA主成分分析' }],
      algorithm_Options7: [{ algorithm_name: 'FETCH', introduction: 'FETCH自动化特征工程' }],
      // 算法参数
      // algorithm_parameters2: [{ introduction: '保留列', name: 'col_retain', value: '' }, { introduction: '维度', name: 'dimension', value: '' }, { introduction: '迭代数', name: 'iteration', value: '' }],
      // 算法参数
      algorithm_parameters1: [{ introduction: '解耦层维度', name: 'latent_dims', select: 'single-select', type: 'int', value: 32 }, { introduction: '迭代数', name: 'epoch', select: 'single-select', type: 'int', value: 100 }, { introduction: '学习率', name: 'lr', select: 'single-select', type: 'float', value: 0.01 }],
      algorithm_parameters2: [{ introduction: '维度', name: 'n_components', select: 'single-select', type: 'int', value: 10 }, { introduction: '迭代数', name: 'epoch', select: 'single-select', type: 'int', value: 100 }, { introduction: '模型层数', name: 'num_layers', select: 'single-select', type: 'int', value: 5 }],
      algorithm_parameters3: [],
      algorithm_parameters4: [],
      algorithm_parameters5: [{ introduction: '保留列', name: 'col_retain', select: 'multi-select', type: 'column', value: '' }],
      algorithm_parameters6: [{ introduction: '维度', name: 'n_components', select: 'single-select', type: 'int', value: 5 }],
      algorithm_parameters7: [{ introduction: '步数', name: 'steps_num', select: 'single-select', type: 'int', value: 3 }, { introduction: '迭代数', name: 'epoch', select: 'single-select', type: 'int', value: 100 }, { introduction: 'worker个数', name: 'worker', select: 'single-select', type: 'int', value: 12 }],
      labelMultible1: false,
      labelMultible2: false,
      labelMultible3: false,
      labelMultible4: false,
      labelMultible5: true,
      labelMultible6: false,
      processConstructForm: {
        operate_name: 'OperatorBased-Manual'
      },
      processExtractForm: {
        operate_name: 'PCA'
      },
      processDecouplingForm: {
        operate_name: 'FactorGNN'
      },
      processLearningForm: {
        operate_name: 'GNN'
      },
      processDeriveForm: {
        operate_name: 'HumanMachineCooperation'
      },
      processSelectionForm: {
        operate_name: 'ModelBased'
      },
      processGenerationForm: {
        operate_name: 'FETCH'
      },
      featureDecouplingDialog: false,
      featureLearningDialog: false,
      featureDeriveDialog: false,
      featureSelectionDialog: false,
      featureConstructDialog: false,
      featureExtractDialog: false,
      featureGenerationDialog: false,
      existedFeatureEng: false,
      HumanFeaData: [],
      totalPage_featureEngList: 5,
      countTotal_featureEngList: 15,
      percentageListen: null
    }
  },
  mounted () {
    // this.lazyLoading_featureEngList()
  },
  created () {
    this.getOriginDatasetId()
  },
  methods: {
    showDeriveSetting () {
      this.featureDeriveDialog = true
      // this.featureEngDialogVisible = true
      // this.percentageListen = setInterval(() => {
      //   this.percentage = this.percentage + 1
      //   console.log(this.percentage)
      // }, 1000 * 1)
    },
    showGenerationSetting () {
      this.featureGenerationDialog = true
      // this.featureEngDialogVisible = true
      // this.percentageListen = setInterval(() => {
      //   this.percentage = this.percentage + 1
      //   console.log(this.percentage)
      // }, 1000 * 1)
    },
    showSelectionSetting () {
      this.featureSelectionDialog = true
    },
    clear () {
      this.featureEngDialogVisible = false
      clearInterval(this.percentageListen)
      this.$router.push('/feature')
    },
    handleCheckedChange () {
    },
    showDecouplingSetting () {
      if (this.algorithm_parameters1.length === 0) {
        humanFeaApi.queryAlgorithmParas(this.processDecouplingForm.operate_name).then(response => {
          const resp = response.data
          console.log(resp.data)
          if (typeof JSON.parse(resp.data.algorithm_parameters) === 'string') {
            const algorithmParametersList = JSON.parse(JSON.parse(resp.data.algorithm_parameters))
            for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
              this.algorithm_parameters1.push(algorithmParametersList[i])
            }
          } else {
            const algorithmParametersList = JSON.parse(resp.data.algorithm_parameters)
            for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
              this.algorithm_parameters1.push(algorithmParametersList[i])
            }
          }
          for (let i = 0; i < this.algorithm_parameters1.length; i = i + 1) {
            if (this.algorithm_parameters1[i].name === 'col_retain') {
              if (this.algorithm_parameters1[i].select === 'single-select') {
                this.labelMultible1 = false
              } else {
                this.labelMultible1 = true
              }
            }
          }
        })
      }
      this.featureDecouplingDialog = true
    },
    showLearningSetting () {
      if (this.algorithm_parameters2.length === 0) {
        humanFeaApi.queryAlgorithmParas(this.processLearningForm.operate_name).then(response => {
          const resp = response.data
          console.log(resp.data)
          if (typeof JSON.parse(resp.data.algorithm_parameters) === 'string') {
            const algorithmParametersList = JSON.parse(JSON.parse(resp.data.algorithm_parameters))
            for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
              this.algorithm_parameters2.push(algorithmParametersList[i])
            }
          } else {
            const algorithmParametersList = JSON.parse(resp.data.algorithm_parameters)
            for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
              this.algorithm_parameters2.push(algorithmParametersList[i])
            }
          }
          for (let i = 0; i < this.algorithm_parameters2.length; i = i + 1) {
            if (this.algorithm_parameters2[i].name === 'col_retain') {
              if (this.algorithm_parameters2[i].select === 'single-select') {
                this.labelMultible2 = false
              } else {
                this.labelMultible2 = true
              }
            }
          }
        })
      }
      this.featureLearningDialog = true
    },
    showConstructSetting () {
      if (this.algorithm_parameters5.length === 0) {
        humanFeaApi.queryAlgorithmParas(this.processConstructForm.operate_name).then(response => {
          const resp = response.data
          console.log(resp.data)
          if (typeof JSON.parse(resp.data.algorithm_parameters) === 'string') {
            const algorithmParametersList = JSON.parse(JSON.parse(resp.data.algorithm_parameters))
            for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
              this.algorithm_parameters5.push(algorithmParametersList[i])
            }
          } else {
            const algorithmParametersList = JSON.parse(resp.data.algorithm_parameters)
            for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
              this.algorithm_parameters5.push(algorithmParametersList[i])
            }
          }
          for (let i = 0; i < this.algorithm_parameters5.length; i = i + 1) {
            if (this.algorithm_parameters5[i].name === 'col_retain') {
              if (this.algorithm_parameters5[i].select === 'single-select') {
                this.labelMultible5 = false
              } else {
                this.labelMultible5 = true
              }
            }
          }
        })
      }
      this.featureConstructDialog = true
    },
    showExtractSetting () {
      if (this.algorithm_parameters6.length === 0) {
        humanFeaApi.queryAlgorithmParas(this.processExtractForm.operate_name).then(response => {
          const resp = response.data
          console.log(resp.data)
          if (typeof JSON.parse(resp.data.algorithm_parameters) === 'string') {
            const algorithmParametersList = JSON.parse(JSON.parse(resp.data.algorithm_parameters))
            for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
              this.algorithm_parameters6.push(algorithmParametersList[i])
            }
          } else {
            const algorithmParametersList = JSON.parse(resp.data.algorithm_parameters)
            for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
              this.algorithm_parameters6.push(algorithmParametersList[i])
            }
          }
          for (let i = 0; i < this.algorithm_parameters6.length; i = i + 1) {
            if (this.algorithm_parameters6[i].name === 'col_retain') {
              if (this.algorithm_parameters6[i].select === 'single-select') {
                this.labelMultible6 = false
              } else {
                this.labelMultible6 = true
              }
            }
          }
        })
      }
      this.featureExtractDialog = true
    },
    backPage () {
      this.$router.back()
    },
    showExistedFeatureEng () {
      console.log(this.HumanFeaData)
      // 导入已有特征工程
      this.HumanFeaData = []
      // 已有特征工程
      featureEngApi.query().then(response => {
        const resp = response.data
        console.log(resp.data)
        const upper = resp.data.length
        let state = ''
        let type = ''
        for (let i = 0; i < upper; i = i + 1) {
          if (resp.data[i].operate_state === '1') {
            state = '交互中'
          } else if (resp.data[i].operate_state === '2') {
            state = '已完成'
          } else if (resp.data[i].operate_state === '3') {
            state = '已停止'
          }
          if (resp.data[i].featureEng_type === 'HumanInLoop') {
            type = '人机协同特征学习与衍生技术'
          } else if (resp.data[i].featureEng_type === 'Machine') {
            type = '纯机器方法'
          } else {
            type = '纯人工方法'
          }
          this.existedFeatureEng = true
          this.HumanFeaData.push({ featureEng_id: resp.data[i].featureEng_id, featureEng_name: resp.data[i].featureEng_name, featureEng_type: type, featureEng_accuracy: resp.data[i].FeatureEng_accuracy, featureEng_efficiency: resp.data[i].FeatureEng_efficiency, operate_state: state })
        }
      })
    },
    // 点击确定按钮，提交上传数据表单
    submitHumanForm () {
      console.log(this.algorithm_parameters1)
      console.log(this.algorithm_parameters2)
      if (this.addFeatureForm.featureEng_type === 'HumanInLoop') {
        this.addFeatureForm.featureEng_processes = []
        if (this.addFeatureForm.checkedModules.includes('1')) {
          var process1 = {}
          this.processDecouplingForm.process_name = 'Feature_Decoupling'
          process1.process_name = 'Feature_Decoupling'
          process1.operate_name = this.processDecouplingForm.operate_name
          for (let i = 0; i < this.algorithm_parameters1.length; i = i + 1) {
            process1[this.algorithm_parameters1[i].name] = this.algorithm_parameters1[i].value
          }
          this.addFeatureForm.featureEng_processes.push(process1)
        }
        if (this.addFeatureForm.checkedModules.includes('2')) {
          var process2 = {}
          this.processDecouplingForm.process_name = 'Feature_Learning'
          process2.process_name = 'Feature_Learning'
          process2.operate_name = this.processLearningForm.operate_name
          for (let i = 0; i < this.algorithm_parameters2.length; i = i + 1) {
            process2[this.algorithm_parameters2[i].name] = this.algorithm_parameters2[i].value
          }
          this.addFeatureForm.featureEng_processes.push(process2)
        }
        if (this.addFeatureForm.checkedModules.includes('3')) {
          var process3 = {}
          this.processDeriveForm.process_name = 'Feature_Derive'
          process3.process_name = 'Feature_Derive'
          process3.operate_name = this.processDeriveForm.operate_name
          for (let i = 0; i < this.algorithm_parameters3.length; i = i + 1) {
            process3[this.algorithm_parameters3[i].name] = this.algorithm_parameters3[i].value
          }
          this.addFeatureForm.featureEng_processes.push(process3)
        }
        if (this.addFeatureForm.checkedModules.includes('4')) {
          var process4 = {}
          this.processSelectionForm.process_name = 'Feature_Selection'
          process4.process_name = 'Feature_Selection'
          process4.operate_name = this.processSelectionForm.operate_name
          for (let i = 0; i < this.algorithm_parameters4.length; i = i + 1) {
            process4[this.algorithm_parameters4[i].name] = this.algorithm_parameters4[i].value
          }
          this.addFeatureForm.featureEng_processes.push(process4)
        }
        console.log(this.addFeatureForm)
        if (this.addFeatureForm.checkedModules.length === 0) {
          this.$message.error('请选择功能模块！')
        } else {
          humanFeaApi.submitFeatureEngForm(this.addFeatureForm).then(response => {
            console.log(response.data.data)
            this.featureEngDialogVisible = true
            this.percentageListen = setInterval(() => {
              this.getTaskStatues(response.data.data.task_id)
            }, 1000 * 0.2)
          })
        }
      } else if (this.addFeatureForm.featureEng_type === 'Manual') {
        this.addFeatureForm.featureEng_processes = []
        this.addFeatureForm.checkedModules = ['1']
        var process5 = {}
        this.processConstructForm.process_name = 'FeatureEng_construct'
        process5.process_name = 'FeatureEng_construct'
        process5.operate_name = this.processConstructForm.operate_name
        for (let i = 0; i < this.algorithm_parameters5.length; i = i + 1) {
          process5[this.algorithm_parameters5[i].name] = this.algorithm_parameters5[i].value
        }
        this.addFeatureForm.featureEng_processes.push(process5)
        var process6 = {}
        this.processExtractForm.process_name = 'FeatureEng_extract'
        process6.process_name = 'FeatureEng_extract'
        process6.operate_name = this.processExtractForm.operate_name
        for (let i = 0; i < this.algorithm_parameters6.length; i = i + 1) {
          process6[this.algorithm_parameters6[i].name] = this.algorithm_parameters6[i].value
        }
        console.log(this.algorithm_parameters6)
        this.addFeatureForm.featureEng_processes.push(process6)
        console.log(this.addFeatureForm)
        humanFeaApi.submitFeatureEngForm(this.addFeatureForm).then(response => {
          console.log(response.data.data)
          this.featureEngDialogVisible = true
          this.percentageListen = setInterval(() => {
            this.getTaskStatues(response.data.data.task_id)
          }, 1000 * 0.2)
        })
      } else {
        this.addFeatureForm.featureEng_processes = []
        this.addFeatureForm.checkedModules = ['1']
        var process7 = {}
        this.processConstructForm.process_name = 'Feature_Generation'
        process7.process_name = 'Feature_Generation'
        process7.operate_name = this.processGenerationForm.operate_name
        for (let i = 0; i < this.algorithm_parameters7.length; i = i + 1) {
          process7[this.algorithm_parameters7[i].name] = this.algorithm_parameters7[i].value
        }
        this.addFeatureForm.featureEng_processes.push(process7)
        console.log(this.addFeatureForm)
        humanFeaApi.submitFeatureEngForm(this.addFeatureForm).then(response => {
          console.log(response.data.data)
          this.featureEngDialogVisible = true
          this.percentageListen = setInterval(() => {
            this.getTaskStatues(response.data.data.task_id)
          }, 1000 * 0.2)
        })
      }

      // // 调整了一下位置
      // // 处理一下特征构建的参数
      // if (this.processConstructForm.algorithm_parameters !== undefined) {
      //   for (let i = 0; i < this.processConstructForm.algorithm_parameters.length; i++) {
      //     if (this.processConstructForm.algorithm_parameters[i].name === 'human_operators') {
      //       // 基于算子 人在回路
      //       this.processConstructForm.algorithm_parameters[i].value = this.human_operators_list
      //     }
      //     if (this.processConstructForm.algorithm_parameters[i].name === 'machine_operators') {
      //       // 基于算子 自动化（机器）
      //       this.processConstructForm.algorithm_parameters[i].value = this.machine_operators_list
      //     }
      //     this.processConstructForm[this.processConstructForm.algorithm_parameters[i].name] = this.processConstructForm.algorithm_parameters[i].value
      //   }
      //   this.addFeatureForm.featureEng_processes.push(this.processConstructForm)
      // }
      // // 处理一下特征提取的参数
      // if (this.processExtractForm.algorithm_parameters !== undefined) {
      //   for (let i = 0; i < this.processExtractForm.algorithm_parameters.length; i++) {
      //     this.processExtractForm[this.processExtractForm.algorithm_parameters[i].name] = this.processExtractForm.algorithm_parameters[i].value
      //   }
      //   this.addFeatureForm.featureEng_processes.push(this.processExtractForm)
      // }
      //
      // this.addFeatureForm.original_dataset_id = this.OriginDatasetId
      // this.$refs.addFeatureFormRef.validate(valid => {
      //   if (valid) {
      //     console.log(this.addFeatureForm)
      //     humanFeaApi.add(this.addFeatureForm).then(response => {
      //       const resp = response.data
      //       console.log(response)
      //       if (resp.meta.code === 204) {
      //         this.$message.success('添加特征工程成功')
      //       } else {
      //         this.$message.error('添加特征工程失败')
      //       }
      //     })
      //   }
      // })
    },
    getTaskStatues (id) {
      humanFeaApi.queryTaskProgress(id).then(response => {
        const resp = JSON.parse(response.data.data)
        console.log(resp)
        this.percentage = Math.ceil(resp.progress * 100)
        this.taskMessage = resp.message
      })
    },
    // 获取数据集列名
    getColumns () {
      console.log('this.addFeatureForm.original_dataset_id')
      console.log(this.addFeatureForm.original_dataset_id)
      featureApi.getDatasetColumns(this.addFeatureForm.original_dataset_id.toString()).then(response => {
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
      this.addFeatureForm.original_dataset_id = this.OriginDatasetId
      this.addFeatureForm.original_dataset_name = this.OriginDatasetName
      // console.log(this.OriginDatasetId)
      // this.getColumns()
      // console.log(db)
    },
    // 点击查看特征工程按钮
    queryFeatureEng () {
      this.$router.push('/feature/queryFea')
    },
    // 通过算法接口动态获取参数
    getAlgorithm () {
      // learnApi.queryAlgorithm(this.algorithm_category).then(response => {
      //   this.algorithm_originalOptions1 = response.data.data
      //   this.algorithm_name1 = response.data.data.map(item => item.algorithm_name)
      // })
      // learnApi.queryAlgorithm(this.algorithm_category2).then(response => {
      //   this.algorithm_originalOptions2 = response.data.data
      //   this.algorithm_name2 = response.data.data.map(item => item.algorithm_name)
      // })
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
      this.algorithm_originalOptions1 = []
      console.log(this.addFeatureForm.featureEng_type)
      if (this.addFeatureForm.featureEng_type === 'HumanInLoop') {
        console.log('this.addFeatureForm', this.addFeatureForm)
        humanFeaApi.queryAlgorithmByType(this.addFeatureForm.featureEng_type).then(response => {
          const resp = response.data
          if (resp.meta.code === 200) {
            this.$message.success('获取数据集成功')
          }
          this.algorithm_originalOptions1 = resp.data
          if (this.algorithm_originalOptions1.length > 0) {
            console.log('algorithm_originalOptions1', this.algorithm_originalOptions1)
            this.algorithm_Options1 = this.algorithm_originalOptions1.filter((p) => {
              return p.algorithm_category === 'Feature_Decoupling'
            })
            this.algorithm_Options2 = this.algorithm_originalOptions1.filter((p) => {
              return p.algorithm_category === 'Feature_Learning'
            })
            this.algorithm_Options3 = this.algorithm_originalOptions1.filter((p) => {
              return p.algorithm_category === 'Feature_Derive'
            })
            this.algorithm_Options4 = this.algorithm_originalOptions1.filter((p) => {
              return p.algorithm_category === 'Feature_Selection'
            })
          }
        })
      } else if (this.addFeatureForm.featureEng_type === 'Manual') {
        this.algorithm_originalOptions1 = []
        humanFeaApi.queryAlgorithmByType(this.addFeatureForm.featureEng_type).then(response => {
          const resp = response.data
          if (resp.meta.code === 200) {
            this.$message.success('获取数据集成功')
          }
          this.algorithm_originalOptions1 = resp.data
          console.log('testtest')
          console.log(this.algorithm_originalOptions1)
          if (this.algorithm_originalOptions1.length > 0) {
            this.algorithm_Options5 = this.algorithm_originalOptions1.filter((p) => {
              return p.algorithm_category === 'FeatureEng_construct'
            })
            this.algorithm_Options6 = this.algorithm_originalOptions1.filter((p) => {
              return p.algorithm_category === 'FeatureEng_extract'
            })

            this.getColumns()
          }
        })
      } else if (this.addFeatureForm.featureEng_type === 'Machine') {
        this.algorithm_originalOptions1 = []
        humanFeaApi.queryAlgorithmByType(this.addFeatureForm.featureEng_type).then(response => {
          const resp = response.data
          if (resp.meta.code === 200) {
            this.$message.success('获取数据集成功')
          }
          this.algorithm_originalOptions1 = resp.data
          if (this.algorithm_originalOptions1.length > 0) {
            this.algorithm_Options7 = this.algorithm_originalOptions1.filter((p) => {
              return p.algorithm_category === 'Feature_Generation'
            })
          }
        })
      }
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
    // 当特征解耦方法发生改变的时候
    handleselectTrainname () {
      this.algorithm_parameters1 = []
      humanFeaApi.queryAlgorithmParas(this.processDecouplingForm.operate_name).then(response => {
        const resp = response.data
        console.log(resp.data)
        if (typeof JSON.parse(resp.data.algorithm_parameters) === 'string') {
          const algorithmParametersList = JSON.parse(JSON.parse(resp.data.algorithm_parameters))
          for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
            this.algorithm_parameters1.push(algorithmParametersList[i])
          }
        } else {
          const algorithmParametersList = JSON.parse(resp.data.algorithm_parameters)
          for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
            this.algorithm_parameters1.push(algorithmParametersList[i])
          }
        }
        for (let i = 0; i < this.algorithm_parameters1.length; i = i + 1) {
          if (this.algorithm_parameters1[i].name === 'col_retain') {
            if (this.algorithm_parameters1[i].select === 'single-select') {
              this.labelMultible1 = false
            } else {
              this.labelMultible1 = true
            }
          }
        }
      })
    },
    handleselectTrainname2 () {
      this.algorithm_parameters2 = []
      humanFeaApi.queryAlgorithmParas(this.processLearningForm.operate_name).then(response => {
        const resp = response.data
        console.log(resp.data)
        if (typeof JSON.parse(resp.data.algorithm_parameters) === 'string') {
          const algorithmParametersList = JSON.parse(JSON.parse(resp.data.algorithm_parameters))
          for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
            this.algorithm_parameters2.push(algorithmParametersList[i])
          }
        } else {
          const algorithmParametersList = JSON.parse(resp.data.algorithm_parameters)
          for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
            this.algorithm_parameters2.push(algorithmParametersList[i])
          }
        }
        for (let i = 0; i < this.algorithm_parameters2.length; i = i + 1) {
          if (this.algorithm_parameters2[i].name === 'col_retain') {
            if (this.algorithm_parameters2[i].select === 'single-select') {
              this.labelMultible2 = false
            } else {
              this.labelMultible2 = true
            }
          }
        }
      })
    },
    handleselectTrainname3 () {

    },
    handleselectTrainname4 () {

    },
    handleselectTrainname5 () {
      this.algorithm_parameters5 = []
      humanFeaApi.queryAlgorithmParas(this.processConstructForm.operate_name).then(response => {
        const resp = response.data
        console.log(resp.data)
        if (typeof JSON.parse(resp.data.algorithm_parameters) === 'string') {
          const algorithmParametersList = JSON.parse(JSON.parse(resp.data.algorithm_parameters))
          for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
            this.algorithm_parameters5.push(algorithmParametersList[i])
          }
        } else {
          const algorithmParametersList = JSON.parse(resp.data.algorithm_parameters)
          for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
            this.algorithm_parameters5.push(algorithmParametersList[i])
          }
        }
        for (let i = 0; i < this.algorithm_parameters5.length; i = i + 1) {
          if (this.algorithm_parameters5[i].name === 'col_retain') {
            if (this.algorithm_parameters5[i].select === 'single-select') {
              this.labelMultible5 = false
            } else {
              this.labelMultible5 = true
            }
          }
        }
      })
    },
    handleselectTrainname6 () {
      this.algorithm_parameters6 = []
      humanFeaApi.queryAlgorithmParas(this.processExtractForm.operate_name).then(response => {
        const resp = response.data
        console.log(resp.data)
        if (typeof JSON.parse(resp.data.algorithm_parameters) === 'string') {
          const algorithmParametersList = JSON.parse(JSON.parse(resp.data.algorithm_parameters))
          for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
            this.algorithm_parameters6.push(algorithmParametersList[i])
          }
        } else {
          const algorithmParametersList = JSON.parse(resp.data.algorithm_parameters)
          for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
            this.algorithm_parameters6.push(algorithmParametersList[i])
          }
        }
        for (let i = 0; i < this.algorithm_parameters6.length; i = i + 1) {
          if (this.algorithm_parameters6[i].name === 'col_retain') {
            if (this.algorithm_parameters6[i].select === 'single-select') {
              this.labelMultible6 = false
            } else {
              this.labelMultible6 = true
            }
          }
        }
      })
    },
    handleselectTrainname7 () {
      this.algorithm_parameters7 = []
      humanFeaApi.queryAlgorithmParas(this.processGenerationForm.operate_name).then(response => {
        const resp = response.data
        console.log(resp.data)
        if (typeof JSON.parse(resp.data.algorithm_parameters) === 'string') {
          const algorithmParametersList = JSON.parse(JSON.parse(resp.data.algorithm_parameters))
          for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
            this.algorithm_parameters7.push(algorithmParametersList[i])
          }
        } else {
          const algorithmParametersList = JSON.parse(resp.data.algorithm_parameters)
          for (let i = 0; i < algorithmParametersList.length; i = i + 1) {
            this.algorithm_parameters7.push(algorithmParametersList[i])
          }
        }
      })
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
    // // 当训练方法发生改变的时候
    // handleselectTrainname2 () {
    //   // this.getColumns()
    //   for (let i = 0; i < this.algorithm_Options2.length; i++) {
    //     if (this.algorithm_Options2[i].algorithm_name === this.processExtractForm.operate_name) {
    //       // this.algorithm_parameters2 = JSON.parse(this.algorithm_Options2[i].algorithm_parameters
    //       // 暂时用假数据
    //       this.algorithm_parameters2 = [{ introduction: '保留列', name: 'col_retain', value: '' }, { introduction: '维度', name: 'dimension', value: '' }, { introduction: '迭代数', name: 'iteration', value: '' }]
    //       this.processExtractForm.algorithm_parameters = this.algorithm_parameters2
    //       console.log(this.algorithm_parameters2)
    //       for (let i = 0; i < this.algorithm_parameters2.length; i++) {
    //         if (this.algorithm_parameters2[i].name === 'col_retain') {
    //           if (this.algorithm_parameters2[i].select === 'single-select') {
    //             this.labelMultible2 = false
    //           } else {
    //             this.labelMultible2 = true
    //           }
    //         }
    //       }
    //     }
    //   }
    // },
    // 特征解耦参数配置
    submitDecouplingParams () {
      console.log(this.processDecouplingForm)
      this.featureDecouplingDialog = false
    },
    // 特征学习参数配置
    submitLearningParams () {
      console.log(this.processLearningForm)
      this.featureLearningDialog = false
    },
    // 特征构建参数配置
    submitConstructParams () {
      console.log(this.processConstructForm)
      this.featureConstructDialog = false
    },
    // 特征提取参数配置
    submitExtractParams () {
      console.log(this.processExtractForm)
      this.featureExtractDialog = false
    },
    // 机器学习-特征生成参数配置
    submitGenerationParams () {
      console.log(this.processExtractForm)
      this.featureGenerationDialog = false
    },
    // 导入特征工程
    importFeatureEng (row) {
      const id = row.featureEng_id
      featureEngApi.importFeatureEng(id).then(response => {
        const resp = response.data.data
        this.addFeatureForm.featureEng_type = resp.featureEng_type
        this.addFeatureForm.featureEng_name = resp.featureEng_name
        this.addFeatureForm.original_dataset_id = resp.dataset_id
        this.addFeatureForm.original_dataset_name = resp.dataset_name
        this.addFeatureForm.new_dataset_name = resp.new_dataset_name
        this.addFeatureForm.run_mode = resp.featureEng_operationMode
        this.addFeatureForm.checkedModules = []
        const modules = resp.checkedModules.split(',')
        for (let i = 0; i < modules.length; i = i + 1) {
          this.addFeatureForm.checkedModules.push(modules[i])
        }
        const process = resp.featureEng_processes
        for (let i = 0; i < process.length; i = i + 1) {
          if (process[i].process_name === 'Feature_Decoupling') {
            this.processDecouplingForm.operate_name = process[i].operate_name
          }
          if (process[i].process_name === 'Feature_Learning') {
            this.processLearningForm.operate_name = process[i].operate_name
          }
          if (process[i].process_name === 'Feature_Derive') {
            this.processDeriveForm.operate_name = process[i].operate_name
          }
          if (process[i].process_name === 'Feature_Selection') {
            this.processSelectionForm.operate_name = process[i].operate_name
          }
          if (process[i].process_name === 'FeatureEng_construct') {
            this.processConstructForm.operate_name = process[i].operate_name
          }
          if (process[i].process_name === 'FeatureEng_extract') {
            this.processExtractForm.operate_name = process[i].operate_name
          }
        }
        console.log(this.addFeatureForm)
      })
      this.existedFeatureEng = false
    }
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
    height: 80px;
    box-shadow: none;
  }
</style>
