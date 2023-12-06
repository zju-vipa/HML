<template>
    <div>
      <!-- 卡片区域 -->
      <el-card >
        <!-- form区域 -->
          <el-row type="flex" align="middle">
            <el-col :span="2"><h3>创建特征工程</h3></el-col>
            <el-col :span="4">
<!--              <el-form label-width="0px" label-position="right" :model="chooseDatasetForm" ref="chooseDatasetFormRef" id="chooseDatasetFormID">-->
<!--                <el-form-item prop="dataset_name">-->
                  <el-input clearable readonly v-model="chooseDatasetForm.dataset_name"
                  @click.native="datasetDialogVisible=true" placeholder="请选择数据集" style="width: 90%"></el-input>
<!--                </el-form-item>-->
<!--              </el-form>-->
            </el-col>
            <el-col :span="4">
              <el-button type="primary" @click="goHumanFea">创建</el-button>
            </el-col>
          </el-row>
            <!-- <el-form-item prop="dataset_name" label="数据集">
              <el-input clearable  readonly v-model="chooseDatasetForm.dataset_name" style="width: 300px"
                        @click.native="datasetDialogVisible=true" placeholder="请选择数据集"></el-input>
            </el-form-item> -->
            <!-- <el-form-item label="特征工程">
              <el-row>
                <el-col :span="5">
                  <el-button type="primary" @click="goHumanFea">人工特征工程</el-button>
                </el-col>
                <el-col :span="5">
                  <el-button type="primary" >自动化特征工程</el-button>
                </el-col>
                <el-col :span="5">
                  <el-button type="primary" >人在回路的特征工程</el-button>
                </el-col>
              </el-row>
            </el-form-item> -->
      </el-card>

<!--          <el-table :data="datasetDetailList" border stripe  style="width: 100%">-->
<!--          &lt;!&ndash; <el-table-column  label="序号" type="index" width="120"> </el-table-column> &ndash;&gt;-->
<!--          <el-table-column width="120" v-for="(item,id) in columnsList" :key="id" :prop="item" :label="item"></el-table-column>-->
<!--          &lt;!&ndash; <el-table-column prop="age" label="数据集类型"> </el-table-column>-->
<!--          <el-table-column prop="checking_status" label="数据集介绍"> </el-table-column> &ndash;&gt;-->
<!--        </el-table>-->
      <div style="padding: 1%">
        <el-tabs type="border-card">
        <el-tab-pane label="最新结果">
          <div v-if="checkedAll">
            <el-row v-if="newResultForm.isNewResult==false">
              <div style="text-align: center">
                <el-row>
                  <img src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px">
                </el-row>
                <el-row><span style="color: darkgray">暂无记录</span></el-row>
              </div>
            </el-row>
            <el-row v-if="newResultForm.isNewResult==true">
              <el-col span="16">
              <el-row>
                <el-col span="13">
                  <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }">
                    <div slot="header" class="header">
                      <el-row type="flex" align="middle">
                        <el-col span="12">
                          <span class="header-label" style="font-size: 18px; font-weight: bolder">当前任务概况</span>
                        </el-col>
  <!--                      <el-col span="12" style="text-align: right">-->
  <!--                        <el-link type="success">查看详情</el-link>-->
  <!--                      </el-col>-->
                      </el-row>
                    </div>
                    <div style="margin: 15px; text-align: center">
                        <el-row  v-for="item in newResultForm.taskDetails" :key="item.type" style="line-height: 5px">
                          <el-col span="6">
                            <h3 style="text-align: left">{{item.label}}</h3>
                          </el-col>
                          <el-col span="18" style="text-align: left">
                            <h4 style="font-weight: lighter">{{item.value}}</h4>
                          </el-col>
                        </el-row>
                        <el-row style="line-height: 5px" type="flex" align="middle">
                          <el-col span="6">
                           <h3 style="text-align: left">已选功能模块</h3>
                          </el-col>
                          <el-col span="18" style="text-align: left">
                            <el-checkbox-group v-model="newResultForm.checkedModules" v-if="displayType == 0">
                              <el-checkbox v-for="(item, index) in moduleOptions" :label="item.value" :key="index" :value="item.value" disabled>{{item.label}}</el-checkbox>
                            </el-checkbox-group>
                            <el-checkbox-group v-model="newResultForm.checkedModules" v-else-if="displayType == 1">
                              <el-checkbox v-for="(item, index) in moduleOptions2" :label="item.value" :key="index" :value="item.value" disabled>{{item.label}}</el-checkbox>
                            </el-checkbox-group>
                            <el-checkbox-group v-model="newResultForm.checkedModules" v-else>
                              <el-checkbox v-for="(item, index) in moduleOptions3" :label="item.value" :key="index" :value="item.value" disabled>{{item.label}}</el-checkbox>
                            </el-checkbox-group>
                          </el-col>
                        </el-row>
                    </div>
                  </el-card>
                </el-col>
                <el-col span="11">
                  <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }">
                    <div slot="header" class="header">
                      <el-row type="flex" align="middle">
                        <el-col span="12">
                          <span class="header-label" style="font-size: 18px; font-weight: bolder">当前效果</span>
                        </el-col>
                      </el-row>
                    </div>
                    <div style="margin: 15px; text-align: center; height: 300px">
                      <el-row v-if="newResultForm.efficiency != null">
                        <el-col span="12">
                          <el-row>
                            <el-progress type="dashboard" :percentage="newResultForm.efficiency" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">
                            </el-progress>
                          </el-row>
                          <span style="color: steelblue; font-size: 18px;">特征有效率</span>
                        </el-col>
                        <el-col span="12">
                          <el-row>
                            <el-progress type="dashboard" :percentage="newResultForm.accuracy" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">
                            </el-progress>
                          </el-row>
                          <span style="color: steelblue; font-size: 18px;">任务准确率</span>
                        </el-col>
                      </el-row>
                      <el-row v-else>
                        <div style="text-align: center">
                          <el-row>
                            <img src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px">
                          </el-row>
                          <el-row><span style="color: darkgray">暂无记录</span></el-row>
                        </div>
                      </el-row>
                    </div>
                  </el-card>
                </el-col>
              </el-row>
              <el-row>
                <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 370px">
                  <div slot="header" class="header">
                    <el-row type="flex" align="middle">
                      <el-col span="12">
                        <span class="header-label" style="font-size: 18px; font-weight: bolder">当前任务生成特征</span>
                      </el-col>
                    </el-row>
                  </div>
                  <div style="margin: 15px; text-align: center">
                    <el-table
                      border stripe
                      ref="task_feature_table"
                      height="250"
                      solt="append"
                      style="font-size: 15px"
                      :data="taskFeatureList">
                      <el-table-column label="序号" type="index"></el-table-column>
                      <el-table-column
                        v-for="(item, index) in taskFeatureColumnsList"
                        :key="index + 'i'"
                        :label="item.label"
                        :prop="item.prop"
                        show-overflow-tooltip/>
                    </el-table>
                  </div>
                </el-card>
              </el-row>
              <el-row>
                <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 370px">
                  <div slot="header" class="header">
                    <el-row type="flex" align="middle">
                      <el-col span="12">
                        <span class="header-label" style="font-size: 18px; font-weight: bolder">人机协同</span>
                      </el-col>
                    </el-row>
                  </div>
                  <div style="margin: 15px; text-align: center">
                    <el-row type="flex" align="middle">
                      <el-col span="3"><span style="font-size: 17px; font-weight: bolder">优化建议:</span></el-col>
                      <el-col span="4">
                        <el-input v-model="HumanInLoopForm.node" placeholder="请输入1-300节点"></el-input>
                      </el-col>
                      <el-col span="2">
                        <el-button size="mini">查看</el-button>
                      </el-col>
                      <el-col span="5">
                        <span style="text-align: left; font-size: 15px; color: #373d41;padding-top: 20px">{{HumanInLoopForm.node}}号节点的特征有效率:</span>
                      </el-col>
                    </el-row>
                    <el-row type="flex" align="middle" style="padding-top: 10px">
                      <el-col span="3"><div style="font-size: 17px; font-weight: bolder"></div></el-col>
                      <el-col span="4">
                        <el-select v-model="HumanInLoopForm.operator" placeholder="请选择">
                          <el-option
                            v-for="item in operator_options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                          </el-option>
                        </el-select>
                      </el-col>
                      <el-col span="2"><el-button size="mini">查看</el-button></el-col>
                      <el-col span="5">
                        <span style="text-align: left; font-size: 15px; color: #373d41;padding-top: 10px">{{HumanInLoopForm.operator}}算子的特征有效率:</span>
                      </el-col>
                    </el-row>
                    <el-row type="flex" align="middle" style="margin-top: 20px">
                      <el-col span="3"><span style="font-size: 17px; font-weight: bolder">专家干预:</span></el-col>
                      <el-col span="20">
                        <el-row type="flex" align="middle" >
                          <el-col span="3" style="text-align: left"><span style="font-size: 13px;">删除节点:</span></el-col>
                          <el-col style="text-align: left">
                            <el-input v-model="HumanInLoopForm.nodesForDelete" placeholder="请输入删除节点列表" style="width: 200px"></el-input>
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                    <el-row type="flex" align="center" style="padding-top: 20px">
                      <el-col span="3"><div style="font-size: 17px; font-weight: bolder"></div></el-col>
                      <el-col span="20">
                        <el-row>
                          <el-col span="3" style="text-align: left">
                            <span style="font-size: 13px;">添加算子:</span>
                          </el-col>
                          <el-col span="21" style="text-align: left;">
                            <el-checkbox-group v-model="HumanInLoopForm.operatorForAdd">
                              <el-checkbox label="sum"></el-checkbox>
                              <el-checkbox label="log"></el-checkbox>
                              <el-checkbox label="mean"></el-checkbox>
                            </el-checkbox-group>
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                    <el-row type="flex" align="middle" style="padding-top: 20px">
                      <el-col span="3"><div style="font-size: 17px; font-weight: bolder"></div></el-col>
                      <el-col span="20">
                        <el-row>
                          <el-col span="3" style="text-align: left">
                            <span style="font-size: 13px;">删除算子:</span>
                          </el-col>
                          <el-col span="21" style="text-align: left;">
                            <el-checkbox-group v-model="HumanInLoopForm.operatorForDelete">
                              <el-checkbox label="sum"></el-checkbox>
                              <el-checkbox label="log"></el-checkbox>
                              <el-checkbox label="mean"></el-checkbox>
                            </el-checkbox-group>
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                  </div>
                  <el-row>
                    <el-col span="3"><div style="border-radius: 4px;min-height: 36px;"></div></el-col>
                    <el-col span="5"><el-button type="primary">继续学习</el-button></el-col>
                    <el-col span="5"><el-button type="primary" style="margin-left: 30px">结束学习</el-button></el-col>
                  </el-row>
                </el-card>
              </el-row>
            </el-col>
              <el-col span="8">
              <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 530px">
                <div slot="header" class="header">
                  <el-row type="flex" align="middle">
                    <el-col span="12">
                      <span class="header-label" style="font-size: 18px; font-weight: bolder">交互记录</span>
                    </el-col>
                  </el-row>
                </div>
                <div style="margin: 15px; text-align: center;">
                  <el-table
                    :data="IteractionRecord"
                    border stripe
                    ref="iteraction_record_table">
                    <el-table-column label="交互次数" type="index" :index="indexMethod"> </el-table-column>
                    <el-table-column prop="record_efficiency" label="当前特征有效率"></el-table-column>
                    <el-table-column prop="record_accuracy" label="任务准确度"></el-table-column>
                  </el-table>
                </div>
              </el-card>
              <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 530px">
                <div slot="header" class="header">
                  <el-row type="flex" align="middle">
                    <el-col span="12">
                      <span class="header-label" style="font-size: 18px; font-weight: bolder">前100重要特征</span>
                    </el-col>
                  </el-row>
                </div>
                <el-row v-if="draw == false">
                  <div style="text-align: center">
                    <el-row>
                      <img src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px">
                    </el-row>
                    <el-row><span style="color: darkgray">暂无记录</span></el-row>
                  </div>
                </el-row>
                <div style="margin: 15px; text-align: center;">
                  <div id="featureCharts" style="width: 100%; height: 650px; margin: 0 auto;"></div>
                </div>
              </el-card>
            </el-col>
            </el-row>
          </div>
          <div v-else>
            <el-row v-if="newResultForm.isNewResult==false">
              <div style="text-align: center">
                <el-row>
                  <img src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px">
                </el-row>
                <el-row><span style="color: darkgray">暂无记录</span></el-row>
              </div>
            </el-row>
            <el-row v-if="newResultForm.isNewResult==true">
              <el-col span="16">
                <el-row>
                  <el-col span="13">
                    <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }">
                      <div slot="header" class="header">
                        <el-row type="flex" align="middle">
                          <el-col span="12">
                            <span class="header-label" style="font-size: 18px; font-weight: bolder">当前任务概况</span>
                          </el-col>
                          <!--                      <el-col span="12" style="text-align: right">-->
                          <!--                        <el-link type="success">查看详情</el-link>-->
                          <!--                      </el-col>-->
                        </el-row>
                      </div>
                      <div style="margin: 15px; text-align: center">
                        <el-row  v-for="item in newResultForm.taskDetails" :key="item.type" style="line-height: 5px">
                          <el-col span="6">
                            <h3 style="text-align: left">{{item.label}}</h3>
                          </el-col>
                          <el-col span="18" style="text-align: left">
                            <h4 style="font-weight: lighter">{{item.value}}</h4>
                          </el-col>
                        </el-row>
                        <el-row style="line-height: 5px" type="flex" align="middle">
                          <el-col span="6">
                            <h3 style="text-align: left">已选功能模块</h3>
                          </el-col>
                          <el-col span="18" style="text-align: left">
                            <el-checkbox-group v-model="newResultForm.checkedModules" v-if="displayType == 0">
                              <el-checkbox v-for="(item, index) in moduleOptions" :label="item.value" :key="index" :value="item.value" disabled>{{item.label}}</el-checkbox>
                            </el-checkbox-group>
                            <el-checkbox-group v-model="newResultForm.checkedModules" v-else-if="displayType == 1">
                              <el-checkbox v-for="(item, index) in moduleOptions2" :label="item.value" :key="index" :value="item.value" disabled>{{item.label}}</el-checkbox>
                            </el-checkbox-group>
                            <el-checkbox-group v-model="newResultForm.checkedModules" v-else>
                              <el-checkbox v-for="(item, index) in moduleOptions3" :label="item.value" :key="index" :value="item.value" disabled>{{item.label}}</el-checkbox>
                            </el-checkbox-group>
                          </el-col>
                        </el-row>
                      </div>
                    </el-card>
                  </el-col>
                  <el-col span="11">
                    <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }">
                      <div slot="header" class="header">
                        <el-row type="flex" align="middle">
                          <el-col span="12">
                            <span class="header-label" style="font-size: 18px; font-weight: bolder">当前效果</span>
                          </el-col>
                        </el-row>
                      </div>
                      <div style="margin: 15px; text-align: center; height: 300px">
                        <el-row v-if="newResultForm.efficiency != null">
                          <el-col span="12">
                            <el-row>
                              <el-progress type="dashboard" :percentage="newResultForm.efficiency" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">
                              </el-progress>
                            </el-row>
                            <span style="color: steelblue; font-size: 18px;">特征有效率</span>
                          </el-col>
                          <el-col span="12">
                            <el-row>
                              <el-progress type="dashboard" :percentage="newResultForm.accuracy" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">
                              </el-progress>
                            </el-row>
                            <span style="color: steelblue; font-size: 18px;">任务准确率</span>
                          </el-col>
                        </el-row>
                        <el-row v-else>
                          <div style="text-align: center">
                            <el-row>
                              <img src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px">
                            </el-row>
                            <el-row><span style="color: darkgray">暂无记录</span></el-row>
                          </div>
                        </el-row>
                      </div>
                    </el-card>
                  </el-col>
                </el-row>
                <el-row>
                  <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 370px">
                    <div slot="header" class="header">
                      <el-row type="flex" align="middle">
                        <el-col span="12">
                          <span class="header-label" style="font-size: 18px; font-weight: bolder">当前任务生成特征</span>
                        </el-col>
                      </el-row>
                    </div>
                    <div style="margin: 15px; text-align: center">
                      <el-table
                        border stripe
                        ref="task_feature_table"
                        height="250"
                        solt="append"
                        style="font-size: 15px"
                        :data="taskFeatureList">
                        <el-table-column label="序号" type="index"></el-table-column>
                        <el-table-column
                          v-for="(item, index) in taskFeatureColumnsList"
                          :key="index + 'i'"
                          :label="item.label"
                          :prop="item.prop"
                          show-overflow-tooltip/>
                      </el-table>
                    </div>
                  </el-card>
                </el-row>
              </el-col>
              <el-col span="8">
                <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 710px">
                  <div slot="header" class="header">
                    <el-row type="flex" align="middle">
                      <el-col span="12">
                        <span class="header-label" style="font-size: 18px; font-weight: bolder">前100重要特征</span>
                      </el-col>
                    </el-row>
                  </div>
                  <el-row v-if="draw == false">
                    <div style="text-align: center">
                      <el-row>
                        <img src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px">
                      </el-row>
                      <el-row><span style="color: darkgray">暂无记录</span></el-row>
                    </div>
                  </el-row>
                  <div id="featureCharts" style="width: 100%; height: 650px; margin: 0 auto;"></div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="已有特征工程">
          <el-card>
            <div class="table_box2">
              <el-row>
                <el-col :span="24">
                  <el-table
                    :data="HumanFeaData"
                    border stripe
                    ref="featureEng_list_table"
                    height="550"
                    style="font-size: 15px"
                    solt="append">
                    <el-table-column  label="序号" type="index" style="font-weight: bolder"> </el-table-column>
                    <el-table-column prop="featureEng_name" label="特征工程名" style="font-weight: bolder"> </el-table-column>
                    <el-table-column prop="featureEng_type" label="特征工程类型" style="font-weight: bolder"> </el-table-column>
                    <el-table-column prop="featureEng_accuracy" label="任务效果" style="font-weight: bolder">
                      <template slot-scope="scope">
                        <el-progress v-if="scope.row.featureEng_accuracy!=null"
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
                        <el-progress v-if="scope.row.featureEng_efficiency!=null"
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
                    <el-table-column prop="operate_state" label="状态" style="text-align: center">
                      <template slot-scope="scope">
                        <span v-if="scope.row.operate_state==='已完成'" style="color: green">已完成</span>
                        <span v-else-if="scope.row.operate_state==='交互中'"  style="color: orange">交互中</span>
                        <span v-else-if="scope.row.operate_state==='已停止'"  style="color: red">已停止</span>
                      </template>
                    </el-table-column>
                    <el-table-column label="结果">
                      <template slot-scope="scope">
                        <span>
                          <el-button size="mini" @click="queryResult(scope.row)" :disabled="scope.row.operate_state==='交互中' || scope.row.operate_state==='已停止'">结果报告</el-button>
                        </span>
                      </template>
                    </el-table-column>
                    <!--新操作栏-->
                    <el-table-column label="操作">
                      <template slot-scope="scope">
                        <el-row>
                          <el-button size="mini" type="primary" :disabled="scope.row.operate_state==='已完成'" @click="stopTask(scope.row)">停止任务</el-button>
                          <el-button size="mini" type="danger" icon="el-icon-delete" style="margin-top: 5px" @click="deleteFeatureEng(scope.row)">删除</el-button>
                        </el-row>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </el-tab-pane>
        <el-tab-pane label="特征库">
          <el-card>
            <div class="table_box2">
              <el-row>
                <el-col :span="24">
                  <el-table
                    border stripe
                    ref="feature_library_table"
                    height="550"
                    solt="append"
                    style="font-size: 15px"
                    :data="featureLibraryList">
                    <el-table-column label="序号" type="index"></el-table-column>
                    <el-table-column
                      v-for="(item, index) in featureLibraryColumnsList"
                      :key="index + 'i'"
                      :label="item.label"
                      :prop="item.prop"
                      show-overflow-tooltip/>
                  </el-table>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </el-tab-pane>
      </el-tabs>
      </div>
<!--      选择数据集，弹出的窗口-->
      <el-dialog title="选择数据集" :visible.sync="datasetDialogVisible" @close="getColumns">
        <dataset :isDialog="true" @dataset-choose = chooseDataset></dataset>
          <!-- <supplier :isDialog="true" @supplier-choose="supplierChoose"></supplier> -->
      </el-dialog>
    </div>
</template>

<script>
import Dataset from '../data/OriginDataset'
import featureEngApi from '../../api/queryFea'
import * as echarts from 'echarts'

const moduleOptions = [
  { value: '1', label: '特征解耦' },
  { value: '2', label: '特征学习' },
  { value: '3', label: '特征衍生' },
  { value: '4', label: '特征选择' }
]
const moduleOptions2 = [
  { value: '1', label: '特征构建' }
]
const moduleOptions3 = [
  { value: '1', label: '特征生成' }
]
export default {
  name: 'Feature',
  // props: {
  //   // 这里接受父组件传过来的数据，如果isDialog为true，则为弹窗
  //   isHuman: Boolean
  // },
  components: {
    Dataset
  },

  data () {
    return {
      // 选择数据集form
      chooseDatasetForm: {
        dataset_name: '',
        dataset_id: ''
      },
      checkedAll: false,
      moduleOptions,
      moduleOptions2,
      moduleOptions3,
      displayType: 0,
      newResultForm: {
        efficiency: 0,
        accuracy: 0,
        isNewResult: true,
        isFeatureVisual: true,
        checkedModules: [],
        taskDetails: [
          { type: 'name', label: '特征工程名', value: '' },
          { type: 'type', label: '特征工程类型', value: '' },
          { type: 'network', label: '网络拓扑', value: '300节点电网' },
          { type: 'mode', label: '运行方式', value: '' },
          { type: 'dataset', label: '数据集', value: '' }
        ]
      },
      HumanInLoopForm: {
        node: '',
        operator: '',
        nodesForDelete: '',
        operatorForAdd: '',
        operatorForDelete: ''
      },
      datasetId: '',
      datasetName: '',
      draw: false,
      // 弹出数据集对话框
      datasetDialogVisible: false,
      // 用来接收数据集的列名
      featureLibraryColumnsList: [{ label: '特征名', prop: 'name' },
        { label: '所属数据集', prop: 'dataset' },
        { label: '针对任务', prop: 'task' },
        { label: '特征构建', prop: 'featureConstruct' },
        { label: '特征生成', prop: 'featureGeneration' },
        { label: '特征解耦', prop: 'featureDecoupling' },
        { label: '特征学习', prop: 'featureLearning' },
        { label: '特征衍生', prop: 'featureDerivation' },
        { label: '特征选择', prop: 'featureSelection' }],
      taskFeatureColumnsList: [{ label: '特征名', prop: 'name' },
        { label: '所属数据集', prop: 'dataset' },
        { label: '针对任务', prop: 'task' },
        { label: '特征解耦', prop: 'featureDecoupling' },
        { label: '特征学习', prop: 'featureLearning' },
        { label: '特征衍生', prop: 'featureDerivation' },
        { label: '特征选择', prop: 'featureSelection' }],
      // 已有特征工程具体数据
      HumanFeaData: [],
      // 用来接受特征库的具体数据
      featureLibraryList: [],
      taskFeatureList: [],
      loading: false,
      pagination_featureLibrary: {
        page: 1,
        pageSize: 20,
        total: 0
      },
      pagination_featureEngList: {
        page: 1,
        pageSize: 20,
        total: 0
      },
      pagination_taskFeatureList: {
        page: 1,
        pageSize: 20,
        total: 0
      },
      totalPage_featureLibrary: 5,
      totalPage_featureEngList: 5,
      totalPage_taskFeatureList: 5,
      countTotal_featureLibrary: 15,
      countTotal_featureEngList: 15,
      countTotal_taskFeature: 15,
      selectedIds: [],
      checked: false,
      otherHeight: 0,
      pageHeight: 0,
      operator_options: [{ value: '0', label: '求和' }],
      IteractionRecord: []
    }
  },
  created () {
    // 用假数据暂时替代
    this.featureLibraryList = []
    this.taskFeatureList = []
    this.HumanFeaData = []
    this.getLatestTaskDetails()
  },
  mounted () {
    // this.lazyLoading_featureLibrary()
    // this.lazyLoading_featureEngList()
    // this.lazyLoading_taskFeatureList()
  },
  methods: {
    deleteFeatureEng (row) {
      console.log(row.featureEng_id)
      featureEngApi.deleteData(row.featureEng_id).then(response => {
        const resp = response.data.data
        console.log(resp)
        this.getLatestTaskDetails()
      })
    },
    stopTask (row) {
      console.log(row.featureEng_id)
      featureEngApi.stopTask(row.featureEng_id).then(response => {
        const resp = response.data
        console.log(resp)
        if (resp.meta.code === 200) {
          this.$message.success('任务停止成功')
        } else {
          this.$message.error('任务停止失败')
        }
        this.getAllFeatureEngs()
      })
    },
    getLatestTaskDetails () {
      // 当前任务概况+当前效果
      this.displayType = 0
      featureEngApi.queryLatestResults().then(response => {
        const resp = response.data.data
        console.log('当前任务概况')
        console.log(resp)
        this.newResultForm.checkedModules = []
        this.newResultForm.isNewResult = resp.isNewResult
        console.log(resp.isNewResult === true)
        if (resp.isNewResult === true) {
          this.newResultForm.efficiency = resp.original_efficiency
          this.newResultForm.accuracy = resp.original_accuracy
          for (let i = 0; i < this.newResultForm.taskDetails.length; i = i + 1) {
            const key = this.newResultForm.taskDetails[i].type
            this.newResultForm.taskDetails[i].value = resp[key]
            if (key === 'type') {
              if (this.newResultForm.taskDetails[i].value === '纯人工方法') {
                this.displayType = 1
                this.taskFeatureColumnsList = [{ label: '特征名', prop: 'name' }, { label: '所属数据集', prop: 'dataset' }, { label: '针对任务', prop: 'task' }, { label: '特征构建', prop: 'featureConstruct' }]
              } else if (this.newResultForm.taskDetails[i].value === '纯机器方法') {
                this.displayType = 2
                this.taskFeatureColumnsList = [{ label: '特征名', prop: 'name' }, { label: '所属数据集', prop: 'dataset' }, { label: '针对任务', prop: 'task' }, { label: '特征生成', prop: 'featureGeneration' }]
              }
            }
          }
          if (resp.checkedModules !== null && resp.checkedModules !== '') {
            const modules = resp.checkedModules.split(',')
            for (let i = 0; i < modules.length; i = i + 1) {
              this.newResultForm.checkedModules.push(modules[i])
            }
            if (this.newResultForm.checkedModules.length === 4) {
              this.checkedAll = true
            }
          }
          this.getLatestFeatures()
        } else {
          this.getAllFeatureEngs()
        }
      })
    },
    getLatestFeatures () {
      featureEngApi.queryLatestFeatures().then(response => {
        const resp = JSON.parse(response.data.data)
        console.log(resp)
        const upper = resp.length
        for (let i = 0; i < upper; i = i + 1) {
          this.taskFeatureList.push({ name: resp[i].name, dataset: resp[i].dataset, task: resp[i].task, featureConstruct: resp[i].featureConstruct, featureGeneration: resp[i].featureGeneration, featureDecoupling: resp[i].featureDecoupling, featureLearning: resp[i].featureLearning, featureDerivation: resp[i].featureDerivation, featureSelection: resp[i].featureSelection })
        }
      })
      this.getAllFeatureEngs()
    },
    getAllFeatureEngs () {
      this.HumanFeaData = []
      // 已有特征工程
      featureEngApi.query().then(response => {
        const resp = response.data
        console.log(resp.data)
        if (resp.data != null) {
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
            this.HumanFeaData.push({ featureEng_id: resp.data[i].featureEng_id, featureEng_name: resp.data[i].featureEng_name, featureEng_type: type, featureEng_accuracy: resp.data[i].FeatureEng_accuracy, featureEng_efficiency: resp.data[i].FeatureEng_efficiency, operate_state: state })
          }
          this.getFeatureLibrary()
        }
      })
    },
    getFeatureLibrary () {
      //  特征库
      this.featureLibraryList = []
      featureEngApi.queryFeatureLibrary().then(response => {
        const resp = JSON.parse(response.data.data)
        console.log(resp)
        if (resp != null) {
          const upper = resp.length
          for (let i = 0; i < upper; i = i + 1) {
            this.featureLibraryList.push({ name: resp[i].name, dataset: resp[i].dataset, task: resp[i].task, featureConstruct: resp[i].featureConstruct, featureGeneration: resp[i].featureGeneration, featureDecoupling: resp[i].featureDecoupling, featureLearning: resp[i].featureLearning, featureDerivation: resp[i].featureDerivation, featureSelection: resp[i].featureSelection })
          }
          console.log('featureLibraryList')
          console.log(this.featureLibraryList)
        }
      })
      console.log(this.checkedAll)
      if (this.checkedAll) {
        this.getLatestRecord()
      } else {
        this.drawChart()
      }
    },
    getLatestRecord () {
      featureEngApi.queryLatestRecord().then(response => {
        const resp = JSON.parse(response.data.data)
        console.log(resp)
        const upper = resp.length
        for (let i = 0; i < upper; i = i + 1) {
          this.IteractionRecord.push({ record_efficiency: resp[i].record_efficiency + '%', record_accuracy: resp[i].record_accuracy + '%' })
        }
        this.drawChart()
      })
    },
    drawChart () {
      featureEngApi.queryFeatureScore().then(response => {
        const resp = JSON.parse(response.data.data)
        if (resp === null) {
          this.draw = false
        } else {
          this.draw = true
          console.log('draw_fig')
          console.log(resp)
          // 基于准备好的dom，初始化echarts实例  这个和上面的main对应
          const myChart = echarts.init(document.getElementById('featureCharts'))
          const yaxis = resp.name
          const value = resp.value
          // 指定图表的配置项和数据
          const option = {
            grid: {
              containLabel: true
            },
            tooltip: {},
            dataZoom: [
              {
                yAxisIndex: [0],
                show: true,
                realtime: true,
                type: 'inside',
                startValue: 0,
                endValue: 10,
                zoomLock: true
                // handleSize: 100
              }
            ],
            xAxis: { type: 'value' },
            yAxis: {
              data: yaxis,
              inverse: true
            },
            series: [
              {
                name: '特征重要性',
                type: 'bar',
                data: value,
                itemStyle: {
                  color: {
                    type: 'linear', // 线性渐变
                    x: 0,
                    y: 0,
                    x2: 1,
                    y2: 0,
                    colorStops: [{
                      offset: 0,
                      color: '#58F3E1'
                    }, {
                      offset: 1,
                      color: '#4EAACC' // 100%处的颜色为蓝
                    }]
                  }
                }
              }
            ]
          }
          myChart.setOption(option)
        }
      })
    },
    indexMethod (index) {
      return index
    },
    lazyLoading_taskFeatureList () {
      // const dom = document.querySelector('.el-table__body-wrapper')
      const dom = this.$refs.task_feature_table.bodyWrapper
      dom.addEventListener('scroll', (v) => {
        const scrollDistance = dom.scrollHeight - dom.scrollTop - dom.clientHeight
        if (scrollDistance <= 1) {
          if (this.pagination_taskFeatureList.page >= this.totalPage_taskFeatureList) {
            this.$message.warning('特征库数据已全部加载')
          }
          if (this.pagination_taskFeatureList.page < this.totalPage_taskFeatureList) {
            this.pagination_taskFeatureList.page = this.pagination_taskFeatureList.page + 1
            var cIndex = this.countTotal_taskFeature + 10
            for (let i = (this.countTotal_taskFeature + 1); i <= cIndex; i = i + 1) {
              this.taskFeatureList.push({ name: 'feature' + i, dataset: '暂稳数据集', task: '---', featureDecoupling: '---', featureLearning: '---', featureDerivation: '---', featureSelection: '---' })
            }
            this.countTotal_taskFeature += 10
          }
        }
      })
    },
    chooseDataset (currentRow) {
      this.chooseDatasetForm.dataset_name = currentRow.dataset_name
      this.chooseDatasetForm.dataset_id = currentRow.dataset_id
      this.datasetId = currentRow.dataset_id
      this.datasetName = currentRow.dataset_name
      console.log(this.datasetId)
      this.datasetDialogVisible = false
      console.log(currentRow)
    },
    queryResult (row) {
      this.$router.push({
        path: '/feature/result',
        query: {
          featureEng_id: row.featureEng_id
        }
      })
    },
    // 获取数据集列名
    getColumns () {
      // console.log(this.datasetId)
      localStorage.setItem('datasetId', this.datasetId)
      localStorage.setItem('datasetName', this.datasetName)
    },
    // 跳转到人工特征工程页面
    goHumanFea () {
      // this.$emit('columns-get', this.columnsList)
      if (this.datasetId === '' || this.datasetName === '') {
        this.$message.error('请选择数据集')
      } else {
        this.$router.push('/feature/humanfea')
      }
    },
    // 点击查看特征工程按钮
    queryFeatureEng () {
      this.$router.push('/feature/queryFea')
    }
  }
}
</script>

<style scoped>
  .el-form {
    margin: 10px auto;
    /* width: 1000px; */
  }
  .buttons {
    float: right;
  }
  /* .el-button{
    width: 150px;
  } */

  #selectForm >>> .el-form-item__label {
    font-size: 12px;
  }
  .box-card {
    height: 320px;
    .header {
      position: relative;
      .header-label {
        padding-left: 10px;
      }
    }
    .footer {
      font-size: 18px !important;
      background-color: rgb(245, 247, 251);
      display: flex;
      height: 50px;
      justify-content: space-evenly;
    }
    .card-label {
      color: rgb(197, 197, 197);
      margin-right: 8px;
      width: 70px;
      display: inline-block;
      margin-bottom: 5px;
    }
  }
  /deep/.el-tabs__item {
    /* 修改为您想要的文字大小 */
    font-size: 16px!important;
    height: 50px;
  }
  .el-card{
    margin: 5px;
  }
</style>
