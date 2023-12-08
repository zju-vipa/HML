<template>
    <div>
<!--      <el-button @click="fetchDecisionTree11">查看决策树渲染结果1</el-button>-->
      <div>
        <el-dialog title="结果报告" :visible.sync="tree1DialogVisible" width="auto">
        <img v-if="tree1ImageUrl" :src="tree1ImageUrl" alt="决策树1" :width="imgWidth1 + 'px'" height="auto" @wheel="handleWheel($event, 'tree1')" @load="setInitialSize('tree1')" />
      </el-dialog>
      <el-dialog title="决策树2" :visible.sync="tree2DialogVisible" width="auto">
        <img v-if="tree2ImageUrl" :src="tree2ImageUrl" alt="决策树2" :width="imgWidth2 + 'px'" height="auto" @wheel="handleWheel($event, 'tree2')" @load="setInitialSize('tree2')" />
      </el-dialog>
      </div>
<!--      &lt;!&ndash; 卡片区域 &ndash;&gt;-->
<!--      <el-card >-->
<!--        &lt;!&ndash; form区域 &ndash;&gt;-->
<!--          <el-row type="flex" align="middle">-->
<!--            <el-col :span="2"><h3>创建特征工程</h3></el-col>-->
<!--            <el-col :span="4">-->
<!--&lt;!&ndash;              <el-form label-width="0px" label-position="right" :model="chooseDatasetForm" ref="chooseDatasetFormRef" id="chooseDatasetFormID">&ndash;&gt;-->
<!--&lt;!&ndash;                <el-form-item prop="dataset_name">&ndash;&gt;-->
<!--                  <el-input clearable readonly v-model="chooseDatasetForm.dataset_name"-->
<!--                  @click.native="datasetDialogVisible=true" placeholder="请选择数据集" style="width: 90%"></el-input>-->
<!--&lt;!&ndash;                </el-form-item>&ndash;&gt;-->
<!--&lt;!&ndash;              </el-form>&ndash;&gt;-->
<!--            </el-col>-->
<!--            <el-col :span="4">-->
<!--              <el-button type="primary" @click="goHumanFea">创建</el-button>-->
<!--            </el-col>-->
<!--          </el-row>-->
<!--            &lt;!&ndash; <el-form-item prop="dataset_name" label="数据集">-->
<!--              <el-input clearable  readonly v-model="chooseDatasetForm.dataset_name" style="width: 300px"-->
<!--                        @click.native="datasetDialogVisible=true" placeholder="请选择数据集"></el-input>-->
<!--            </el-form-item> &ndash;&gt;-->
<!--            &lt;!&ndash; <el-form-item label="特征工程">-->
<!--              <el-row>-->
<!--                <el-col :span="5">-->
<!--                  <el-button type="primary" @click="goHumanFea">人工特征工程</el-button>-->
<!--                </el-col>-->
<!--                <el-col :span="5">-->
<!--                  <el-button type="primary" >自动化特征工程</el-button>-->
<!--                </el-col>-->
<!--                <el-col :span="5">-->
<!--                  <el-button type="primary" >人在回路的特征工程</el-button>-->
<!--                </el-col>-->
<!--              </el-row>-->
<!--            </el-form-item> &ndash;&gt;-->
<!--      </el-card>-->

<!--          <el-table :data="datasetDetailList" border stripe  style="width: 100%">-->
<!--          &lt;!&ndash; <el-table-column  label="序号" type="index" width="120"> </el-table-column> &ndash;&gt;-->
<!--          <el-table-column width="120" v-for="(item,id) in columnsList" :key="id" :prop="item" :label="item"></el-table-column>-->
<!--          &lt;!&ndash; <el-table-column prop="age" label="数据集类型"> </el-table-column>-->
<!--          <el-table-column prop="checking_status" label="数据集介绍"> </el-table-column> &ndash;&gt;-->
<!--        </el-table>-->
      <div style="padding: 1%">
        <el-tabs type="border-card">
        <el-tab-pane label="决策面板">
          <div v-if="newResultForm.checkedModules.length==4">
            <el-col span="20">
              <el-row v-if="newResultForm.isNewResult==false">
                <div style="text-align: center">
                  <el-row>
                    <img src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px">
                  </el-row>
                  <el-row><span style="color: darkgray">暂无记录</span></el-row>
                </div>
              </el-row>
              <el-row v-else-if="newResultForm.isNewResult==true">
                <el-col span="12">
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
                           <h3 style="text-align: left">特征输入模块</h3>
                          </el-col>
                          <el-col span="18" style="text-align: left">
                            <el-checkbox-group v-model="newResultForm.checkedModules">
                              <el-checkbox v-for="(item, index) in moduleOptions" :label="item.value" :key="index" :value="item.value" disabled>{{item.label}}</el-checkbox>
                            </el-checkbox-group>
                          </el-col>
                        </el-row>
                    </div>
                  </el-card>
                </el-col>
                <el-col span="12">
                  <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }">
                    <div slot="header" class="header">
                      <el-row type="flex" align="middle">
                        <el-col span="12">
                          <span class="header-label" style="font-size: 18px; font-weight: bolder">决策统计</span>
                        </el-col>
                      </el-row>
                    </div>
                    <div style="margin: 15px; text-align: center; height: 300px">
                      <el-row>
                        <el-col span="12">
<!--                          <el-row>-->
<!--                            <el-progress class="no-percent-sign" type="dashboard" :percentage="newResultForm.efficiency" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">-->
<!--                            </el-progress>-->
<!--                          </el-row>-->
                          <el-row>
                            <el-progress class="no-percent-sign" type="dashboard" :percentage="newResultForm.efficiency" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">
                            </el-progress>
<!--                            <span class="progress-text">{{ efficiencyText }}</span>-->
                          </el-row>
                          <span style="color: steelblue; font-size: 18px;">决策器数目</span>
                        </el-col>
                        <el-col span="12">
                          <el-row>
                            <el-progress type="dashboard" :percentage="newResultForm.accuracy" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">
                            </el-progress>
<!--                            <span class="progress-text">{{ newResultForm.accuracy }}</span>-->
                          </el-row>
                          <span style="color: steelblue; font-size: 18px;">决策案例数目</span>
                        </el-col>
                      </el-row>
                    </div>
                  </el-card>
                </el-col>
              </el-row>
              <el-row>
                <el-col span="12">
                <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 360px">
                  <div slot="header" class="header">
                    <el-row type="flex" align="middle">
                      <el-col span="12">
                        <span class="header-label" style="font-size: 18px; font-weight: bolder">决策器优化</span>
                      </el-col>
                    </el-row>
                  </div>
<!--                    <div style="margin: 15px; text-align: left">-->
<!--                        &lt;!&ndash; 新添加的选择栏 &ndash;&gt;-->
<!--                        <label>数据集：</label>-->
<!--                        <el-select v-model="selectedDataset" placeholder="选择数据集">-->
<!--                            <el-option v-for="dataset in datasets" :key="dataset.value" :label="dataset.label" :value="dataset.value"></el-option>-->
<!--                        </el-select>-->
<!--                        <br>-->
<!--                        <label>决策器名称：</label>-->
<!--                        <el-select v-model="selectedDecisionMakerName" placeholder="选择决策器名称">-->
<!--                            <el-option v-for="name in decisionMakerNames" :key="name.value" :label="name.label" :value="name.value"></el-option>-->
<!--                        </el-select>-->
<!--                        <br>-->
<!--                        <label>决策器类型：</label>-->
<!--                        <el-select v-model="selectedDecisionMakerType" placeholder="选择决策器类型">-->
<!--                            <el-option label="机器自主决策" value="machine"></el-option>-->
<!--                            <el-option label="人机智能决策" value="human-machine"></el-option>-->
<!--                        </el-select>-->
<!--                        <br>-->
<!--                        &lt;!&ndash; 显示选中的决策器类型 &ndash;&gt;-->
<!--                        <p v-if="selectedDecisionMakerType">已选择的决策器类型: {{ selectedDecisionMakerType }}</p>-->
<!--                    </div>-->
                  <div style="display: flex; margin: 15px;">
                  <!-- 左侧区域：选择栏和按钮 -->
                  <div style="flex: 1; margin: 15px; text-align: left">
                      <!-- 数据集选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>数据集：</label>
                          <el-select v-model="selectedDataset" placeholder="选择数据集">
                              <el-option v-for="dataset in datasets" :key="dataset.value" :label="dataset.label" :value="dataset.value"></el-option>
                          </el-select>
                      </div>
                      <!-- 决策器名称选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>决策器名称：</label>
                          <el-select v-model="selectedDecisionMakerName" placeholder="选择决策器名称">
                              <el-option v-for="name in decisionMakerNames" :key="name.value" :label="name.label" :value="name.value"></el-option>
                          </el-select>
                      </div>
                      <!-- 决策器类型选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>决策器类型：</label>
                          <el-select v-model="selectedDecisionMakerType" placeholder="选择决策器类型">
                              <el-option label="机器自主决策" value="machine"></el-option>
                              <el-option label="人机智能决策" value="human-machine"></el-option>
                          </el-select>
                      </div>
                      <!-- 显示选中的决策器类型 -->
                      <p v-if="selectedDecisionMakerType">已选择的决策器类型: {{ selectedDecisionMakerType }}</p>
                      <!-- 按钮区域 -->
                      <div style="margin-top: 10px;">
                          <el-button type="primary">添加决策器</el-button>
                          <el-button @click="showDashboard">查看决策器</el-button>
                      </div>
                  </div>
                  <!-- 右侧区域：仪表盘 -->
                  <div style="flex: 1; margin: 15px; text-align: right">
                    <div v-if="isDashboardVisible" style="flex: 1;">
                        <!-- 这里放置仪表盘的内容 -->
<!--                        <div>仪表盘内容</div>-->
                        <div v-if="isDashboardVisible" style="flex: 1; padding-left: 20px;">
                            <!-- Element UI 进度条作为仪表盘 -->
                            <el-progress type="circle" :percentage="progress"></el-progress>
                        </div>
                    </div>
                  </div>
                  </div>
<!--                    <el-form-item prop="dataset_name" label="数据集">-->
<!--                      <el-input clearable readonly  style="width: 300px"-->
<!--                                 placeholder="请选择数据集"></el-input>-->
<!--                    </el-form-item>-->
<!--                    <el-form-item label="学习器名" prop="learner_name">-->
<!--                      <el-input clearable v-model="addLearnerForm.learner_name" placeholder="请填写学习器名" style="width: 300px"></el-input>-->
<!--                    </el-form-item>-->
<!--                    <el-form-item label="学习器类型" prop="learner_type">-->
<!--                      <el-select v-model="addLearnerForm.learner_type" placeholder="学习器类型" style="width: 300px">-->
<!--                        <el-option v-for="(option, index) in learnerTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>-->
<!--                      </el-select>-->
<!--                    </el-form-item>-->
<!--                    <el-form-item label="训练方法" prop="train_name">-->
<!--                      <el-select v-model="learnParamsForm.train_name" placeholder="请选择方法" style="width: 300px"-->
<!--                                 @change="handleselectTrainname">-->
<!--                        <el-option-->
<!--                          v-for="(item, index) in algorithm_Options" :key="index"-->
<!--                          :label="item.introduction"-->
<!--                          :value="item.algorithm_name">-->
<!--                        </el-option>-->
<!--                      </el-select>-->
<!--                    </el-form-item>-->
<!--                    <el-button class="submitBtn" type="primary" @click="submitAllForm">开始训练</el-button>-->
<!--                    <el-button @click="queryLearner" class="queryBtn" type="primary">查看学习器</el-button>-->
                </el-card>
                </el-col>
                <el-col span="12">
                <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 360px">
                  <div slot="header" class="header">
                    <el-row type="flex" align="middle">
                      <el-col span="12">
                        <span class="header-label" style="font-size: 18px; font-weight: bolder">决策器蒸馏</span>
                      </el-col>
                    </el-row>
                  </div>
<!--                    <div style="margin: 15px; text-align: left">-->
<!--                        &lt;!&ndash; 新添加的选择栏 &ndash;&gt;-->
<!--                        <label>数据集：</label>-->
<!--                        <el-select v-model="selectedDataset" placeholder="选择数据集">-->
<!--                            <el-option v-for="dataset in datasets" :key="dataset.value" :label="dataset.label" :value="dataset.value"></el-option>-->
<!--                        </el-select>-->
<!--                        <br>-->
<!--                        <label>决策器名称：</label>-->
<!--                        <el-select v-model="selectedDecisionMakerName" placeholder="选择决策器名称">-->
<!--                            <el-option v-for="name in decisionMakerNames" :key="name.value" :label="name.label" :value="name.value"></el-option>-->
<!--                        </el-select>-->
<!--                        <br>-->
<!--                        <label>决策器类型：</label>-->
<!--                        <el-select v-model="selectedDecisionMakerType" placeholder="选择决策器类型">-->
<!--                            <el-option label="机器自主决策" value="machine"></el-option>-->
<!--                            <el-option label="人机智能决策" value="human-machine"></el-option>-->
<!--                        </el-select>-->
<!--                        <br>-->
<!--                        &lt;!&ndash; 显示选中的决策器类型 &ndash;&gt;-->
<!--                        <p v-if="selectedDecisionMakerType">已选择的决策器类型: {{ selectedDecisionMakerType }}</p>-->
<!--                    </div>-->
                  <div style="display: flex; margin: 15px;">
                  <!-- 左侧区域：选择栏和按钮 -->
                  <div style="flex: 1; margin: 15px; text-align: left">
                      <!-- 数据集选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>数据集：</label>
                          <el-select v-model="selectedDataset" placeholder="选择数据集">
                              <el-option v-for="dataset in datasets" :key="dataset.value" :label="dataset.label" :value="dataset.value"></el-option>
                          </el-select>
                      </div>
                      <!-- 决策器名称选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>决策器名称：</label>
                          <el-select v-model="selectedDecisionMakerName" placeholder="选择决策器名称">
                              <el-option v-for="name in decisionMakerNames" :key="name.value" :label="name.label" :value="name.value"></el-option>
                          </el-select>
                      </div>
                      <!-- 决策器类型选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>决策器类型：</label>
                          <el-select v-model="selectedDecisionMakerType" placeholder="蒸馏器名称">
                              <el-option label="dec_tree" value="machine"></el-option>
                              <el-option label="..." value="human-machine"></el-option>
                          </el-select>
                      </div>
                      <!-- 显示选中的决策器类型 -->
                      <p v-if="selectedDecisionMakerType">已选择的决策器类型: {{ selectedDecisionMakerType }}</p>
                      <!-- 按钮区域 -->
                      <div style="margin-top: 10px;">
                          <el-button type="primary">添加蒸馏器</el-button>
                          <el-button @click="showDashboard">查看蒸馏器</el-button>
                      </div>
                  </div>
                  <!-- 右侧区域：仪表盘 -->
                  <div style="flex: 1; margin: 15px; text-align: right">
                    <div v-if="isDashboardVisible" style="flex: 1;">
                        <!-- 这里放置仪表盘的内容 -->
<!--                        <div>仪表盘内容</div>-->
                        <div v-if="isDashboardVisible" style="flex: 1; padding-left: 20px;">
                            <!-- Element UI 进度条作为仪表盘 -->
                            <el-progress type="circle" :percentage="progress"></el-progress>
                        </div>
                    </div>
                  </div>
                  </div>
<!--                    <el-form-item prop="dataset_name" label="数据集">-->
<!--                      <el-input clearable readonly  style="width: 300px"-->
<!--                                 placeholder="请选择数据集"></el-input>-->
<!--                    </el-form-item>-->
<!--                    <el-form-item label="学习器名" prop="learner_name">-->
<!--                      <el-input clearable v-model="addLearnerForm.learner_name" placeholder="请填写学习器名" style="width: 300px"></el-input>-->
<!--                    </el-form-item>-->
<!--                    <el-form-item label="学习器类型" prop="learner_type">-->
<!--                      <el-select v-model="addLearnerForm.learner_type" placeholder="学习器类型" style="width: 300px">-->
<!--                        <el-option v-for="(option, index) in learnerTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>-->
<!--                      </el-select>-->
<!--                    </el-form-item>-->
<!--                    <el-form-item label="训练方法" prop="train_name">-->
<!--                      <el-select v-model="learnParamsForm.train_name" placeholder="请选择方法" style="width: 300px"-->
<!--                                 @change="handleselectTrainname">-->
<!--                        <el-option-->
<!--                          v-for="(item, index) in algorithm_Options" :key="index"-->
<!--                          :label="item.introduction"-->
<!--                          :value="item.algorithm_name">-->
<!--                        </el-option>-->
<!--                      </el-select>-->
<!--                    </el-form-item>-->
<!--                    <el-button class="submitBtn" type="primary" @click="submitAllForm">开始训练</el-button>-->
<!--                    <el-button @click="queryLearner" class="queryBtn" type="primary">查看学习器</el-button>-->
                </el-card>
                </el-col>
              </el-row>
              <el-row>
              <el-row>
                <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 340px">
                  <div slot="header" class="header">
                    <el-row type="flex" align="middle">
                      <el-col span="12">
                        <span class="header-label" style="font-size: 18px; font-weight: bolder">决策路径可视化</span>
                      </el-col>
                    </el-row>
                  </div>
                  <div style="display: flex; margin: 15px;">
                  <!-- 左侧区域：选择栏和按钮 -->
                  <div style="flex: 1; margin: 15px; text-align: left">
                      <!-- 数据集选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>决策案例：</label>
                          <el-select v-model="selectedDataset" placeholder="选择数据集">
                              <el-option v-for="dataset in datasets" :key="dataset.value" :label="dataset.label" :value="dataset.value"></el-option>
                          </el-select>
                      </div>
                      <!-- 决策器名称选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>蒸馏器名称：</label>
                          <el-select v-model="selectedDecisionMakerName" placeholder="选择决策器名称">
                              <el-option v-for="name in decisionMakerNames" :key="name.value" :label="name.label" :value="name.value"></el-option>
                          </el-select>
                      </div>
                      <!-- 决策器类型选择栏 -->
<!--                      <div style="margin-bottom: 10px;">-->
<!--                          <label>决策器类型：</label>-->
<!--                          <el-select v-model="selectedDecisionMakerType" placeholder="选择决策器类型">-->
<!--                              <el-option label="机器自主决策" value="machine"></el-option>-->
<!--                              <el-option label="人机智能决策" value="human-machine"></el-option>-->
<!--                          </el-select>-->
<!--                      </div>-->
                      <!-- 显示选中的决策器类型 -->
                      <p v-if="selectedDecisionMakerType">已选择的决策器类型: {{ selectedDecisionMakerType }}</p>
                      <!-- 按钮区域 -->
                      <div style="margin-top: 10px;">
                          <el-button type="primary">可视化决策路径</el-button>
                          <el-button @click="viewResult">查看结果</el-button>
                      </div>
                  </div>
                  <!-- 右侧区域：仪表盘 -->
                  <div style="flex: 1; margin: 15px; text-align: right">
                      <div v-if="showImagetree" style="text-align: center; margin-top: 20px;">
                        <img src="./../../assets/img/decision_tree_simplified.png" alt="展示图片">
                      </div>
                  </div>
                  </div>
                </el-card>
              </el-row>
            </el-col>
            <el-col span="4">
              <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 1040px">
                <div slot="header" class="header">
                  <el-row type="flex" align="middle">
                    <el-col span="16">
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
                    <el-table-column prop="record_efficiency" label="决策器名称"></el-table-column>
                    <el-table-column prop="record_accuracy" label="蒸馏器名称"></el-table-column>
                  </el-table>
                </div>
              </el-card>
<!--              <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 550px">-->
<!--                <div slot="header" class="header">-->
<!--                  <el-row type="flex" align="middle">-->
<!--                    <el-col span="12">-->
<!--                      <span class="header-label" style="font-size: 18px; font-weight: bolder">决策路径</span>-->
<!--                    </el-col>-->
<!--                  </el-row>-->
<!--                </div>-->
<!--                <div style="margin: 15px; text-align: center;">-->
<!--&lt;!&ndash;                  <div id="featureCharts" style="width: 400px; height: 500px; margin: 0 auto"></div>&ndash;&gt;-->
<!--                    当前路径：节点4小于等于0.986，节点75小于等于0.330，节点40小于等于-2.582，节点76小于等于-5.498366117477417-->
<!--                </div>-->
<!--              </el-card>-->
            </el-col>
          </div>
          <div v-else>
            <el-col span="20">
              <el-row v-if="newResultForm.isNewResult==false">
                <div style="text-align: center">
                  <el-row>
                    <img src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px">
                  </el-row>
                  <el-row><span style="color: darkgray">暂无记录</span></el-row>
                </div>
              </el-row>
              <el-row v-else-if="newResultForm.isNewResult==true">
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
                          <h3 style="text-align: left">特征输入模块</h3>
                        </el-col>
                        <el-col span="18" style="text-align: left">
                          <el-checkbox-group v-model="newResultForm.checkedModules">
                            <el-checkbox v-for="(item, index) in moduleOptions" :label="item.value" :key="index" :value="item.value" disabled>{{item.label}}</el-checkbox>
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
                          <span class="header-label" style="font-size: 18px; font-weight: bolder">决策统计</span>
                        </el-col>
                      </el-row>
                    </div>
                    <div style="margin: 15px; text-align: center; height: 300px">
                      <el-row>
                        <el-col span="12">
                          <el-row>
                            <el-progress type="dashboard" :percentage="newResultForm.efficiency" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">
                            </el-progress>
                          </el-row>
                          <span style="color: steelblue; font-size: 18px;">人机智能决策数目</span>
                        </el-col>
                        <el-col span="12">
                          <el-row>
                            <el-progress type="dashboard" :percentage="newResultForm.accuracy" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">
                            </el-progress>
                          </el-row>
                          <span style="color: steelblue; font-size: 18px;">知识决策蒸馏识别率</span>
                        </el-col>
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
                        <span class="header-label" style="font-size: 18px; font-weight: bolder">当前决策案例</span>
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
            <el-col span="4">
              <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 710px">
                <div slot="header" class="header">
                  <el-row type="flex" align="middle">
                    <el-col span="12">
                      <span class="header-label" style="font-size: 18px; font-weight: bolder">前100重要特征</span>
                    </el-col>
                  </el-row>
                </div>
                <div id="featureCharts" style="width: 400px; height: 500px; margin: 0 auto"></div>
              </el-card>
            </el-col>
          </div>
        </el-tab-pane>
        <el-tab-pane label="已有案例">
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
                    <el-table-column prop="featureEng_name" label="样本" style="font-weight: bolder"> </el-table-column>
                    <el-table-column prop="featureEng_type" label="决策方式" style="font-weight: bolder"> </el-table-column>
                    <el-table-column prop="featureEng_result" label="真实标签" style="font-weight: bolder">
<!--                      <template slot-scope="scope">-->
<!--                        <el-progress-->
<!--                          type="line"-->
<!--                          :stroke-width="10"-->
<!--                          :percentage="scope.row.featureEng_result"-->
<!--                          color="green">-->
<!--                        </el-progress>-->
<!--                      </template>-->
                    </el-table-column>
                    <el-table-column prop="featureEng_efficiency1" label="决策标签">
<!--                      <template slot-scope="scope">-->
<!--                        <el-progress-->
<!--                          type="line"-->
<!--                          :stroke-width="10"-->
<!--                          :percentage="scope.row.featureEng_efficiency1"-->
<!--                          :color="blue">-->
<!--                        </el-progress>-->
<!--                      </template>-->
                    </el-table-column>
                    <el-table-column prop="featureEng_efficiency" label="蒸馏标签">
<!--                      <template slot-scope="scope">-->
<!--                        <el-progress-->
<!--                          type="line"-->
<!--                          :stroke-width="10"-->
<!--                          :percentage="scope.row.featureEng_efficiency"-->
<!--                          :color="blue">-->
<!--                        </el-progress>-->
<!--                      </template>-->
                    </el-table-column>
                    <el-table-column prop="operate_state" label="状态" style="text-align: center">
                      <template slot-scope="scope">
                        <span v-if="scope.row.operate_state==='已完成'" style="color: green">已完成</span>
                        <span v-else-if="scope.row.operate_state==='交互中'"  style="color: orange">交互中</span>
                      </template>
                    </el-table-column>
                    <el-table-column label="结果">
                      <template>
                        <span>
                          <el-button size="mini" @click="fetchDecisionTree11">结果报告</el-button>
                        </span>
<!--                         弹窗部分 -->
                            <!-- 决策树1的弹窗 -->
<!--                        <el-dialog title="决策树1" :visible.sync="tree1DialogVisible" width="auto">-->
<!--                          <img v-if="tree1ImageUrl" :src="tree1ImageUrl" alt="决策树1" :width="imgWidth1 + 'px'" height="auto" @wheel="handleWheel($event, 'tree1')" @load="setInitialSize('tree1')" />-->
<!--                        </el-dialog>-->
<!--                        <el-dialog :visible.sync="resultReportDialogVisible" title="结果报告" width="80%" :style="{minHeight: '400px'}">-->
<!--                          <img :src="resultReportImage" alt="结果报告">-->
<!--                        </el-dialog>-->
                      </template>
                    </el-table-column>
                    <!--新操作栏-->
                    <el-table-column label="操作">
                      <template>
                        <el-row>
                          <el-button size="mini" type="primary">停止任务</el-button>
                          <el-button size="mini" type="danger" icon="el-icon-delete" style="margin-top: 5px">删除</el-button>
                        </el-row>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </el-tab-pane>
<!--        <el-tab-pane label="特征库">-->
<!--          <el-card>-->
<!--            <div class="table_box2">-->
<!--              <el-row>-->
<!--                <el-col :span="24">-->
<!--                  <el-table-->
<!--                    border stripe-->
<!--                    ref="feature_library_table"-->
<!--                    height="550"-->
<!--                    solt="append"-->
<!--                    style="font-size: 15px"-->
<!--                    :data="featureLibraryList">-->
<!--                    <el-table-column label="序号" type="index"></el-table-column>-->
<!--                    <el-table-column-->
<!--                      v-for="(item, index) in featureLibraryColumnsList"-->
<!--                      :key="index + 'i'"-->
<!--                      :label="item.label"-->
<!--                      :prop="item.prop"-->
<!--                      show-overflow-tooltip/>-->
<!--                  </el-table>-->
<!--                </el-col>-->
<!--              </el-row>-->
<!--            </div>-->
<!--          </el-card>-->
<!--        </el-tab-pane>-->
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
// import Dataset from '../data/OriginDataset'
// import featureApi from '../../api/feature'
import * as echarts from 'echarts'
// import Dataset from '../data/OriginDataset'
// import QueryHumanFeature from './../feature/QueryHumanFeature'
// import QueryLearner from './../learn/QueryLearner'
import featureApi from './../../api/feature'
// import decisionApi from './../../api/decision'
// import axios from 'axios'
// import * as d3 from 'd3'
import Dataset from '../data/OriginDataset'
// import QueryHumanFeature from './../feature/QueryHumanFeature'
// import QueryLearner from './../learn/QueryLearner'
// import featureApi from './../../api/feature'
import decisionApi from './../../api/decision'
// import axios from 'axios'
// import * as d3 from 'd3'

const moduleOptions = [
  { value: '1', label: '原始特征' },
  { value: '2', label: '特征工程' }
  // { value: '3', label: '人机协同' }
  // { value: '4', label: '特征选择' }
]
export default {
  name: 'Decision',
  // props: {
  //   // 这里接受父组件传过来的数据，如果isDialog为true，则为弹窗
  //   isHuman: Boolean
  // },
  components: {
    Dataset
    // QueryHumanFeature,
    // QueryLearner
  },
  computed: {
    efficiencyText () {
      return `${this.newResultForm.efficiency}`
    }
  },
  data () {
    return {
      showImagetree: false,
      // 1205新仪表盘
      progress: 75, // 这里设置你的进度值
      isDashboardVisible: false, // 控制仪表盘显示的数据属性
      selectedDecisionMakerType: null,
      // 1205新卡片
      selectedDataset: null,
      selectedDecisionMakerName: null,
      // selectedDecisionMakerType: null,
      datasets: [], // 数据集列表
      decisionMakerNames: [], // 决策器名称列表
      // ↑新卡片
      imgWidth1: null, // 1023决策树1的图片宽度
      imgWidth2: null, // 1023决策树2的图片宽度
      tree1DialogVisible: false, // 1023控制决策树1的弹窗可见性
      tree2DialogVisible: false, // 1023控制决策树2的弹窗可见性
      tree1ImageUrl: '', // 1023决策树
      tree2ImageUrl: '', // 1023决策树
      resultReportDialogVisible: false,
      resultReportImage: './../../assets/img/pic1108.png',
      zoomScale: 1, // 图片的缩放比例
      // 选择数据集form
      chooseDatasetForm: {
        dataset_name: '',
        dataset_id: ''
      },
      moduleOptions,
      newResultForm: {
        efficiency: 12,
        accuracy: 16,
        isNewResult: true,
        isFeatureVisual: true,
        checkedModules: ['1', '2', '3', '4'],
        taskDetails: [
          { type: 'name', label: '任务名称', value: '人机协同智能决策与知识增强' },
          { type: 'type', label: '决策方式', value: '人机智能决策' },
          { type: 'network', label: '网络拓扑', value: '300节点电网' },
          // { type: 'mode', label: '运行方式', value: '001夏平初始' },
          { type: 'dataset', label: '数据集', value: '暂稳判别数据集' }
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
      // 弹出数据集对话框
      datasetDialogVisible: false,
      // 用来接收数据集的列名
      featureLibraryColumnsList: [{ label: '样本', prop: 'name' },
        { label: '所属数据集', prop: 'dataset' },
        { label: '针对任务', prop: 'task' },
        { label: '决策方式', prop: 'featureDecoupling' },
        { label: '真实标签', prop: 'featureLearning' },
        { label: '决策标签', prop: 'featureDerivation' },
        { label: '蒸馏标签', prop: 'featureSelection' }],
      taskFeatureColumnsList: [{ label: '样本', prop: 'name' },
        { label: '所属数据集', prop: 'dataset' },
        { label: '针对任务', prop: 'task' },
        { label: '决策方式', prop: 'featureDecoupling' },
        { label: '真实标签', prop: 'featureLearning' },
        { label: '决策标签', prop: 'featureDerivation' },
        { label: '蒸馏标签', prop: 'featureSelection' }],
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
      IteractionRecord: [{ record_efficiency: '99.26%', record_accuracy: '95.79%' }]
    }
  },
  created () {
    // 用假数据暂时替代
    this.featureLibraryList = []
    this.HumanFeaData = []
    this.taskFeatureList = []
    for (let i = 1; i <= this.countTotal_featureLibrary; i = i + 1) {
      const nameString = String.fromCharCode(i / 4 + 65) + '_' + i % 4
      this.featureLibraryList.push({ name: nameString, dataset: '暂稳数据集', task: '暂态判稳任务', featureDecoupling: '人机智能决策', featureLearning: '暂态稳定', featureDerivation: '人机协同特征生成', featureSelection: '基于模型的特征选择' })
    }
    for (let i = 0; i < this.countTotal_featureEngList; i++) {
      this.HumanFeaData.push({ featureEng_name: '决策样本' + i, featureEng_type: '人机智能决策', featureEng_result: '暂态稳定', featureEng_efficiency: '暂态稳定', featureEng_efficiency1: '暂态稳定', operate_state: '已完成' })
    }
    for (let i = 0; i < this.countTotal_taskFeature; i++) {
      // const nameString = String.fromCharCode(i / 4 + 65) + '决策树' + '_' + i % 4
      const nameString = '决策树' + String.fromCharCode(i / 4 + 65) + '_' + i % 4
      this.taskFeatureList.push({ name: nameString, dataset: '暂稳数据集', task: '暂态判稳任务', featureDecoupling: '人机智能决策', featureLearning: '暂态稳定', featureDerivation: '暂态稳定', featureSelection: '暂态稳定' })
    }
  },

  mounted () {
    this.lazyLoading_featureLibrary()
    this.lazyLoading_featureEngList()
    this.lazyLoading_taskFeatureList()
    this.drawChart()
  },
  methods: {
    drawChart () {
      // 基于准备好的dom，初始化echarts实例  这个和上面的main对应
      const myChart = echarts.init(document.getElementById('featureCharts'))
      // 用于生成假数据
      let countNum = 0
      const yaxis = []
      const value = []
      for (let i = 0; i < 25; i = i + 1) {
        for (let j = 0; j < 4; j = j + 1) {
          yaxis.push(String.fromCharCode(i + 65) + '_' + j)
          value.push(100 - countNum)
          countNum = countNum + 1
        }
      }
      // 指定图表的配置项和数据
      const option = {
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
    },
    indexMethod (index) {
      return index
    },
    lazyLoading_taskFeatureList () {
      // const dom = document.querySelector('.el-table__body-wrapper')
      const dom = this.$refs.task_feature_table.bodyWrapper
      console.log(dom)
      dom.addEventListener('scroll', (v) => {
        const scrollDistance = dom.scrollHeight - dom.scrollTop - dom.clientHeight
        console.log('鼠标滑动-scrollDistance', scrollDistance)
        if (scrollDistance <= 1) {
          if (this.pagination_taskFeatureList.page >= this.totalPage_taskFeatureList) {
            this.$message.warning('特征库数据已全部加载')
          }
          if (this.pagination_taskFeatureList.page < this.totalPage_taskFeatureList) {
            this.pagination_taskFeatureList.page = this.pagination_taskFeatureList.page + 1
            console.log('页面已经到达底部,可以请求接口,请求第' + this.pagination_taskFeatureList.page + '页数据')
            var cIndex = this.countTotal_taskFeature + 10
            for (let i = (this.countTotal_taskFeature + 1); i <= cIndex; i = i + 1) {
              this.taskFeatureList.push({ name: 'feature' + i, dataset: '暂稳数据集', task: '---', featureDecoupling: '---', featureLearning: '---', featureDerivation: '---', featureSelection: '---' })
            }
            this.countTotal_taskFeature += 10
          }
        }
      })
    },
    lazyLoading_featureLibrary () {
      // const dom = document.querySelector('.el-table__body-wrapper')
      const dom = this.$refs.feature_library_table.bodyWrapper
      console.log(dom)
      dom.addEventListener('scroll', (v) => {
        const scrollDistance = dom.scrollHeight - dom.scrollTop - dom.clientHeight
        console.log('鼠标滑动-scrollDistance', scrollDistance)
        if (scrollDistance <= 1) {
          if (this.pagination_featureLibrary.page >= this.totalPage_featureLibrary) {
            this.$message.warning('特征库数据已全部加载')
          }
          if (this.pagination_featureLibrary.page < this.totalPage_featureLibrary) {
            this.pagination_featureLibrary.page = this.pagination_featureLibrary.page + 1
            console.log('页面已经到达底部,可以请求接口,请求第' + this.pagination_featureLibrary.page + '页数据')
            var cIndex = this.countTotal_featureLibrary + 10
            for (let i = (this.countTotal_featureLibrary + 1); i <= cIndex; i = i + 1) {
              this.featureLibraryList.push({ name: 'feature' + i, dataset: '暂稳数据集', task: '---', featureDecoupling: '---', featureLearning: '---', featureDerivation: '---', featureSelection: '---' })
            }
            this.countTotal_featureLibrary += 10
          }
        }
      })
    },
    lazyLoading_featureEngList () {
      // const dom = document.querySelector('.el-table__body-wrapper')
      const dom = this.$refs.featureEng_list_table.bodyWrapper
      console.log(dom)
      dom.addEventListener('scroll', (v) => {
        const scrollDistance = dom.scrollHeight - dom.scrollTop - dom.clientHeight
        console.log('鼠标滑动-scrollDistance', scrollDistance)
        if (scrollDistance <= 1) {
          if (this.pagination_featureEngList.page >= this.totalPage_featureEngList) {
            this.$message.warning('已有特征工程数据已全部加载')
          }
          if (this.pagination_featureEngList.page < this.totalPage_featureEngList) {
            this.pagination_featureEngList.page = this.pagination_featureEngList.page + 1
            console.log('页面已经到达底部,可以请求接口,请求第' + this.pagination_featureEngList.page + '页数据')
            var cIndex = this.countTotal_featureEngList + 10
            for (let i = (this.countTotal_featureEngList + 1); i <= cIndex; i = i + 1) {
              this.HumanFeaData.push({ featureEng_name: '特征工程' + i, featureEng_type: '暂稳数据集', featureEng_result: '10', featureEng_efficiency: '20', operate_state: '交互中' })
            }
            this.countTotal_featureEngList += 10
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
    queryResult () {
      this.$router.push('/feature/result')
    },
    // 获取数据集列名
    getColumns () {
      // console.log(this.datasetId)
      if (this.datasetId !== '') {
        localStorage.setItem('datasetId', this.datasetId)
        localStorage.setItem('datasetName', this.datasetName)
        featureApi.getDatasetColumns(this.datasetId).then(response => {
          console.log(response)
          const resp = response.data
          // if (resp.meta.code === 200) {
          //   this.$message.success('获取数据集成功')
          // }
          this.columnsList = resp.data
          console.log(this.columnsList)
        })
        featureApi.getData(this.datasetId).then(response => {
          console.log(response)
          const resp = response.data
          if (resp.meta.code === 200) {
            this.$message.success('获取数据成功')
          }
          // this.datasetDetailList = resp.data
          // console.log(this.datasetDetailList)
        })
      }
    },
    // 跳转到人工特征工程页面
    goHumanFea () {
      this.$emit('columns-get', this.columnsList)
      this.$router.push('/feature/humanfea')
    },
    // 点击查看特征工程按钮
    queryFeatureEng () {
      this.$router.push('/feature/queryFea')
    },
    showResultReport () {
      this.resultReportDialogVisible = true
    },
    handleImageZoom (event) {
      const zoomStep = 0.1
      if (event.deltaY > 0) {
        this.zoomScale = Math.max(this.zoomScale - zoomStep, 0.5) // 最小缩放比例为 0.5
      } else {
        this.zoomScale = Math.min(this.zoomScale + zoomStep, 3) // 最大缩放比例为 3
      }
      this.applyZoom()
    },
    applyZoom () {
      const image = this.$el.querySelector('.result-image')
      if (image) {
        image.style.transform = `scale(${this.zoomScale})`
      }
    },
    // 1023：决策树
    fetchDecisionTree11 () {
      // 先清除两张图片
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
        this.$message.error('获取决策树11失败')
      })
    },
    // 1023：决策树
    fetchDecisionTree22 () {
      // 先清除两张图片
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
    // // 1023：决策树
    // showTree1Dialog () {
    //   this.fetchDecisionTree1() // 获取决策树1的数据
    //   this.tree1DialogVisible = true // 显示决策树1的弹窗
    // },
    // // 1023：决策树
    // showTree2Dialog () {
    //   this.fetchDecisionTree2() // 获取决策树2的数据
    //   this.tree2DialogVisible = true // 显示决策树2的弹窗
    // },
    // 1023：决策树
    handleWheel (event, treeType) {
      const delta = event.deltaY > 0 ? 200 : -200
      if (treeType === 'tree1') {
        this.imgWidth1 = Math.max(1000, this.imgWidth1 + delta) // 更新决策树1的图片宽度
      } else if (treeType === 'tree2') {
        this.imgWidth2 = Math.max(1000, this.imgWidth2 + delta) // 更新决策树2的图片宽度
      }
    },
    setInitialSize (treeType) {
      if (treeType === 'tree1') {
        this.imgWidth1 = 1000 // 设置决策树1的初始宽度
      } else if (treeType === 'tree2') {
        this.imgWidth2 = 800 // 设置决策树2的初始宽度
      }
    },
    showDashboard () {
      this.isDashboardVisible = true // 在点击按钮时显示仪表盘
    },
    viewResult () {
      this.showImagetree = true
    }
  }
}
</script>

<style scoped>
  .result-image {
    width: 100%;
    transition: transform 0.2s;
    /* 保持图片居中显示 */
    display: block;
    margin: 0 auto;
  }
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
  /* 针对具体的进度条组件隐藏百分号 */
  .no-percent-sign .el-progress__text::after {
      content: none !important;
  }
  .no-percent-sign {
    position: relative;
  }
  .progress-text {
    position: absolute;
    top: 50%;  /* 调整这些值来正确地定位文本 */
    left: 50%;
    transform: translate(-50%, -50%);
    font-weight: bolder;
    font-size: 20px;
  }
  .no-percent-sign .el-progress__text {
    color: transparent !important;
}
  .no-percent-sign .el-progress__text {
    font-size: 0.1px !important; /* 或者使用更小的值，直到文本几乎不可见 */
    color: transparent !important; /* 可以选择性地保留，以确保文本不可见 */
}
</style>
