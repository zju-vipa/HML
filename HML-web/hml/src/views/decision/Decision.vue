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
                          <span style="color: steelblue; font-size: 18px;">决策器识别率</span>
                        </el-col>
                        <el-col span="12">
                          <el-row>
                            <el-progress type="dashboard" :percentage="newResultForm.accuracy" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">
                            </el-progress>
<!--                            <span class="progress-text">{{ newResultForm.accuracy }}</span>-->
                          </el-row>
                          <span style="color: steelblue; font-size: 18px;">蒸馏器识别率</span>
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
                  <div style="display: flex; margin: 15px;">
                  <!-- 左侧区域：选择栏和按钮 -->
                  <div style="flex: 1; margin: 15px; text-align: left">
                      <!-- 数据集选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>数据集：</label>
                          <el-select v-model="selectedDataset" placeholder="选择数据集" style="width: 300px;">
                            <el-option label="China-300" value="China-300" ></el-option>
<!--                            <el-option label="case39" value="case39"></el-option>-->
<!--                              <el-option v-for="dataset in datasets" :key="dataset.value" :label="dataset.label" :value="dataset.value"></el-option>-->
                          </el-select>
                      </div>
                      <!-- 决策器名称选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>决策器名称：</label>
<!--                          <el-select v-model="selectedDecisionMakerName" placeholder="选择决策器名称">-->
<!--                            <el-option label="dec_eng1" value="dec_eng1"></el-option>-->
<!--                            <el-option label="dec_eng2" value="dec_eng2"></el-option>-->
<!--                              <el-option v-for="name in decisionMakerNames" :key="name.value" :label="name.label" :value="name.value"></el-option>-->
<!--                          </el-select>-->
                        <el-input v-model="selectedDecisionMakerName" placeholder="输入决策器名称" style="width: 300px;"></el-input>
                      </div>
                      <!-- 决策器类型选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>决策器类型：</label>
                          <el-select v-model="selectedDecisionMakerType" placeholder="选择决策器类型" style="width: 300px;">
                              <el-option label="机器自主决策" value="machine"></el-option>
                              <el-option label="人机智能决策" value="human-machine"></el-option>
                          </el-select>
                      </div>
                      <!-- 显示选中的决策器类型 -->
<!--                      <p v-if="selectedDecisionMakerType">已选择的决策器类型: {{ selectedDecisionMakerType }}</p>-->
                      <!-- 按钮区域 -->
                      <div style="margin-top: 10px;">
                          <el-button type="primary" @click="handleAddDecisionMaker">添加决策器</el-button>
                          <el-button @click="viewDecisionMaker" :disabled="!isDecisionMakerAdded">查看决策器</el-button>
                      </div>
                  </div>
                  <!-- 右侧区域：仪表盘 -->
                  <div style="flex: 1; margin: 15px; text-align: right; display: flex; align-items: flex-end; justify-content: flex-start;">
<!--                  <div style="flex: 1; margin: 15px; text-align: right">-->
<!--                    <el-progress v-if="isDashboardVisible" type="dashboard" :percentage="progress"></el-progress>-->
                    <el-progress v-if="isDashboardVisible" type="dashboard" :percentage="progress" style="transform: scale(1.5); transform-origin: bottom left;"></el-progress>
<!--                    <div v-if="isDashboardVisible" style="flex: 1;">-->
<!--                        &lt;!&ndash; 这里放置仪表盘的内容 &ndash;&gt;-->
<!--&lt;!&ndash;                        <div>仪表盘内容</div>&ndash;&gt;-->
<!--                        <div v-if="isDashboardVisible" style="flex: 1; padding-left: 20px;">-->
<!--                            &lt;!&ndash; Element UI 进度条作为仪表盘 &ndash;&gt;-->
<!--                            <el-progress type="circle" :percentage="progress"></el-progress>-->
<!--                        </div>-->
<!--                    </div>-->
                  </div>
                  </div>
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
                  <div style="display: flex; margin: 15px;">
                  <!-- 左侧区域：选择栏和按钮 -->
                  <div style="flex: 1; margin: 15px; text-align: left">
                      <!-- 数据集选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>数据集：</label>
                          <el-select v-model="selectedDataset1" placeholder="选择数据集" style="width: 300px;">
                            <el-option label="China-300" value="China-300"></el-option>
<!--                            <el-option label="case39" value="case39"></el-option>-->
<!--                              <el-option v-for="dataset in datasets" :key="dataset.value" :label="dataset.label" :value="dataset.value"></el-option>-->
                          </el-select>
                      </div>
                      <!-- 决策器名称选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>决策器名称：</label>
<!--                          <el-select v-model="selectedDecisionMakerName1" placeholder="选择决策器名称">-->
<!--                            <el-option label="dec_eng1" value="dec_eng1"></el-option>-->
<!--                            <el-option label="dec_eng2" value="dec_eng2"></el-option>-->
<!--&lt;!&ndash;                              <el-option v-for="name in decisionMakerNames" :key="name.value" :label="name.label" :value="name.value"></el-option>&ndash;&gt;-->
<!--                          </el-select>-->
                            <el-select v-model="selectedDecisionMakerName1" placeholder="选择决策器名称" style="width: 300px;">
                                <el-option v-for="item in decisionMakerOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                      </div>
                      <!-- 决策器类型选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>蒸馏器名称：</label>
<!--                          <el-select v-model="selectedDecisionMakerType1" placeholder="蒸馏器名称">-->
<!--                              <el-option label="dec_tree1" value="dec_tree1"></el-option>-->
<!--                              <el-option label="dec_tree2" value="dec_tree2"></el-option>-->
<!--                          </el-select>-->
                        <el-input v-model="selectedDecisionMakerType1" placeholder="输入蒸馏器名称" style="width: 300px;"></el-input>
                      </div>
                      <!-- 显示选中的决策器类型 -->
<!--                      <p v-if="selectedDecisionMakerType1">已选择的决策器类型: {{ selectedDecisionMakerType1 }}</p>-->
                      <!-- 按钮区域 -->
                      <div style="margin-top: 10px;">
                          <el-button type="primary" @click="handleAddDecisionMaker1">添加蒸馏器</el-button>
                          <el-button @click="viewDecisionMaker1" :disabled="!isDecisionMakerAdded1">查看蒸馏器</el-button>
                      </div>
                  </div>
                  <!-- 右侧区域：仪表盘 -->
                  <div style="flex: 1; margin: 15px; text-align: right; display: flex; align-items: flex-end; justify-content: flex-start;">
<!--                  <div style="flex: 1; margin: 15px; text-align: right">-->
<!--                    <el-progress v-if="isDashboardVisible" type="dashboard" :percentage="progress"></el-progress>-->
                    <el-progress v-if="isDashboardVisible1" type="dashboard" :percentage="progress1" style="transform: scale(1.5); transform-origin: bottom left;"></el-progress>
<!--                    <div v-if="isDashboardVisible" style="flex: 1;">-->
<!--                        &lt;!&ndash; 这里放置仪表盘的内容 &ndash;&gt;-->
<!--&lt;!&ndash;                        <div>仪表盘内容</div>&ndash;&gt;-->
<!--                        <div v-if="isDashboardVisible" style="flex: 1; padding-left: 20px;">-->
<!--                            &lt;!&ndash; Element UI 进度条作为仪表盘 &ndash;&gt;-->
<!--                            <el-progress type="circle" :percentage="progress"></el-progress>-->
<!--                        </div>-->
<!--                    </div>-->
                  </div>
                  </div>
                </el-card>
                </el-col>
              </el-row>
              <!-- <el-row> -->
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
                          <el-select v-model="selectedDataset2" placeholder="选择案例">
                              <el-option label="case1" value="case1"></el-option>
                              <el-option label="case2" value="case2"></el-option>
                              <el-option label="case3" value="case3"></el-option>
                              <el-option label="case4" value="case4"></el-option>
                              <el-option label="case5" value="case5"></el-option>
                              <el-option v-for="dataset in datasets" :key="dataset.value" :label="dataset.label" :value="dataset.value"></el-option>
                          </el-select>
                      </div>
                      <!-- 决策器名称选择栏 -->
                      <div style="margin-bottom: 10px;">
                          <label>蒸馏器名称：</label>
                          <el-select v-model="selectedDecisionMakerName2" placeholder="选择蒸馏器">
<!--                              <el-option label="dec_tree1" value="dec_tree1"></el-option>-->
<!--                              <el-option label="dec_tree2" value="dec_tree2"></el-option>-->
                            <el-option v-for="item in decisionMakerOptions1" :key="item.value" :label="item.label" :value="item.value"></el-option>
<!--                              <el-option v-for="name in decisionMakerNames" :key="name.value" :label="name.label" :value="name.value"></el-option>-->
                          </el-select>
                      </div>
<!--                      <p v-if="selectedDecisionMakerType32">已选择的决策器类型: {{ selectedDecisionMakerType3 }}</p>-->
                      <!-- 按钮区域 -->
                      <div style="margin-top: 10px;">
                          <el-button type="primary" @click="handleAddDecisionMaker2">可视化决策路径</el-button>
                          <el-button  :disabled="!isDecisionMakerAdded2" @click="getVisualizationImage">查看结果</el-button>
<!--                          <el-button @click="viewResult">查看结果</el-button>-->
                      </div>
                  </div>
                  <!-- 右侧区域：仪表盘 -->
                  <div style="flex: 1; margin: 15px; text-align: right; margin-top: 20px;">
<!--                      <div v-if="showImagetree" style="text-align: center; margin-top: 20px;">-->
<!--                        <img src="./../../assets/img/decision_tree_simplified.png" alt="展示图片">-->
<!--                      </div>-->
                     <img v-if="visualizationImageUrl" :src="visualizationImageUrl" width="990" height="165" alt="Visualization" @click="openModal">
                  </div>
                      <!-- 模态弹窗 -->
                  <div v-if="showModal" class="modal">
                    <div class="modal-content">
                      <span class="close" @click="closeModal">&times;</span>
                      <img :src="visualizationImageUrl" alt="Visualization"  class="modal-image">
                    </div>
                  </div>
                  </div>
                </el-card>
              </el-row>
            </el-col>
            <el-col span="4">
<!--              <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 1040px">-->
<!--                <div slot="header" class="header">-->
<!--                  <el-row type="flex" align="middle">-->
<!--                    <el-col span="16">-->
<!--                      <span class="header-label" style="font-size: 18px; font-weight: bolder">交互记录</span>-->
<!--                    </el-col>-->
<!--                  </el-row>-->
<!--                </div>-->
<!--                <div style="margin: 15px; text-align: center;">-->
<!--                  <el-table-->
<!--                    :data="IteractionRecord"-->
<!--                    border stripe-->
<!--                    ref="iteraction_record_table">-->
<!--                    <el-table-column label="交互记录" type="index" :index="indexMethod"> </el-table-column>-->
<!--                    <el-table-column prop="record_efficiency" label="决策器名称"></el-table-column>-->
<!--&lt;!&ndash;                    <el-table-column prop="record_accuracy" label="蒸馏器名称"></el-table-column>&ndash;&gt;-->
<!--                  </el-table>-->
<!--                </div>-->
<!--              </el-card>-->
                      <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 1040px">
                        <div slot="header" class="header">
                          <el-row type="flex" align="middle">
                            <el-col span="18">
                              <span class="header-label" style="font-size: 18px; font-weight: bolder">交互记录</span>
                            </el-col>
                          </el-row>
                        </div>
                        <div style="margin: 15px; text-align: center;">
                          <!-- 决策器名称表格 -->
                          <el-table :data="decisionMakerOptions" border stripe style="margin-bottom: 20px;">
                            <el-table-column label="记录" type="index"></el-table-column>
                            <el-table-column prop="value" label="决策器名称">
                                <template slot-scope="scope">
                                  <span @click="handleDecisionMakerNameClick(scope.row.value)">
                                    {{ scope.row.value }}
                                  </span>
                                </template>
                            </el-table-column>
                          </el-table>
                          <!-- 蒸馏器名称表格 -->
                          <el-table :data="decisionMakerOptions1" border stripe>
                            <el-table-column label="记录" type="index"></el-table-column>
                            <el-table-column prop="value" label="蒸馏器名称">
                              <template slot-scope="scope">
                                  <span @click="handleDecisionMakerNameClick1(scope.row.value)">
                                    {{ scope.row.value }}
                                  </span>
                              </template>
                            </el-table-column>
                          </el-table>
                        </div>
                      </el-card>
<!--                <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 1040px">-->
<!--                  <div slot="header" class="header">-->
<!--                    <el-row type="flex" align="middle">-->
<!--                      <el-col span="16">-->
<!--                        <span class="header-label" style="font-size: 18px; font-weight: bolder">交互记录</span>-->
<!--                      </el-col>-->
<!--                    </el-row>-->
<!--                  </div>-->
<!--                  <div style="margin: 15px; text-align: center;">-->
<!--                    &lt;!&ndash; 决策器名称表格 &ndash;&gt;-->
<!--                    <el-table :data="decisionMakerOptions" style="margin-bottom: 20px;">-->
<!--                      <el-table-column prop="value" label="决策器名称"></el-table-column>-->
<!--                    </el-table>-->
<!--                    &lt;!&ndash; 蒸馏器名称表格 &ndash;&gt;-->
<!--                    <el-table :data="decisionMakerOptions1">-->
<!--                      <el-table-column prop="value" label="蒸馏器名称"></el-table-column>-->
<!--                    </el-table>-->
<!--                  </div>-->
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
// import axios from 'axios'
// import * as d3 from 'd3'
// import axios from 'axios'

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
      // 1229交互记录卡片
      decisionMakerNames1: [], // 存储决策器的名称
      distillerNames: [], // 存储蒸馏器的名称
      // 1229轮训更新名称信息
      pollingTimer: null,
      // 1229蒸馏器名称信息传递
      decisionMakerOptions1: [],
      // 1229决策器名称信息传递
      decisionMakerOptions: [],
      showImagetree: false,
      // 1205新仪表盘
      // progress: 75, // 这里设置你的进度值
      // isDashboardVisible: false, // 控制仪表盘显示的数据属性
      // 决策器优化卡片
      progress: 0, // 仪表盘
      isDashboardVisible: false, // 仪表盘
      timer: null, // 仪表盘
      isDecisionMakerAdded: false, // 是否成功添加
      selectedDecisionMakerType: null,
      selectedDataset: null,
      selectedDecisionMakerName: null,
      // 决策器蒸馏卡片
      progress1: 0, // 仪表盘
      isDashboardVisible1: false, // 仪表盘
      timer1: null, // 仪表盘
      isDecisionMakerAdded1: false, // 是否成功添加
      selectedDecisionMakerType1: null,
      selectedDataset1: null,
      selectedDecisionMakerName1: null,
      // 决策器路径可视化卡片
      visualizationImageUrl: '', // 图片加载
      showModal: false, // 控制模态弹窗的显示
      isDecisionMakerAdded2: false, // 是否成功添加
      selectedDecisionMakerType2: null,
      selectedDataset2: null,
      selectedDecisionMakerName2: null,
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
    // 1229交互记录卡片
    this.fetchDecisionMakerNames()
    this.fetchDistillerNames()
    // 1229决策器名称信息传递
    this.fetchDecisionMakers()
    this.fetchDecisionMakers1()
    // 用假数据暂时替代
    // eslint-disable-next-line no-unreachable
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
    // this.fetchDecisionMakers()
    // this.fetchDecisionMakers1()
    this.pollingTimer = setInterval(() => {
      this.fetchDecisionMakers()
      this.fetchDecisionMakers1()
    }, 1000) // 30000毫秒 = 30秒
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
      // this.isDashboardVisible = true // 在点击按钮时显示仪表盘
    },
    viewResult () {
      this.showImagetree = true
    },
    // 1226GCN决策器优化卡片
    handleAddDecisionMaker () {
      // 1229更新名称表单状态
      this.fetchDecisionMakers()
      // this.fetchDecisionMakers1()
      // 重置仪表盘状态
      this.progress = 0
      this.isDashboardVisible = false
      clearInterval(this.timer)
      // 弹窗提示表单的完整性
      const missingFields = []
      if (!this.selectedDataset) {
        missingFields.push('数据集')
      }
      if (!this.selectedDecisionMakerName) {
        missingFields.push('决策器名称')
      }
      if (!this.selectedDecisionMakerType) {
        missingFields.push('决策器类型')
      }
      if (missingFields.length > 0) {
        this.$message({
          message: `请添加${missingFields.join('、')}`,
          type: 'warning'
        })
        return
      }
      // 提交表单
      const payload = {
        selectedDataset: this.selectedDataset,
        selectedDecisionMakerName: this.selectedDecisionMakerName,
        selectedDecisionMakerType: this.selectedDecisionMakerType
      }
      decisionApi.addDecisionMaker(payload)
        .then(response => {
          this.$message.success('添加成功')
          this.isDecisionMakerAdded = true // 更新状态，成功添加了
          this.startProgress() // 仪表盘开始计时
          // 这里可以根据需要添加更多的逻辑
        })
        .catch(error => {
          console.error('添加失败', error)
        })
    },
    // 1226GCN决策器优化卡片——仪表盘
    startProgress () {
      this.timer = setInterval(() => {
        if (this.progress < 100) {
          this.progress += 0.5 // 或者根据实际情况调整增量
        } else {
          clearInterval(this.timer) // 到达 100% 后停止计时
        }
      }, 100) // 调整时间间隔以控制速度
    },
    // 1226GCN决策器优化卡片——显示仪表盘
    viewDecisionMaker () {
      this.isDashboardVisible = true // 显示仪表盘
    },
    // 1226GCN决策器蒸馏卡片
    handleAddDecisionMaker1 () {
      // 1229更新名称表单状态
      // this.fetchDecisionMakers()
      this.fetchDecisionMakers1()
      this.fetchDecisionMakerNames()
      this.fetchDistillerNames()
      // 重置仪表盘状态
      this.progress1 = 0
      this.isDashboardVisible1 = false
      clearInterval(this.timer1)
      // 弹窗提示表单的完整性
      const missingFields = []
      if (!this.selectedDataset1) {
        missingFields.push('数据集')
      }
      if (!this.selectedDecisionMakerName1) {
        missingFields.push('决策器名称')
      }
      if (!this.selectedDecisionMakerType1) {
        missingFields.push('决策器类型')
      }
      if (missingFields.length > 0) {
        this.$message({
          message: `请添加${missingFields.join('、')}`,
          type: 'warning'
        })
        return
      }
      // 提交表单
      const payload = {
        selectedDataset: this.selectedDataset1,
        selectedDecisionMakerName: this.selectedDecisionMakerName1,
        selectedDecisionMakerType: this.selectedDecisionMakerType1
      }
      decisionApi.addDecisionMaker1(payload)
        .then(response => {
          this.$message.success('添加成功')
          this.isDecisionMakerAdded1 = true // 更新状态，成功添加了
          this.startProgress1() // 仪表盘开始计时
          // 这里可以根据需要添加更多的逻辑
        })
        .catch(error => {
          console.error('添加失败', error)
        })
    },
    // 1226GCN决策器优化卡片——仪表盘
    startProgress1 () {
      this.timer1 = setInterval(() => {
        if (this.progress1 < 100) {
          this.progress1 += 1 // 或者根据实际情况调整增量
        } else {
          clearInterval(this.timer1) // 到达 100% 后停止计时
        }
      }, 100) // 调整时间间隔以控制速度
    },
    // 1226GCN决策器优化卡片——显示仪表盘
    viewDecisionMaker1 () {
      this.isDashboardVisible1 = true // 显示仪表盘
    },
    // 1226GCN决策路径可视化
    handleAddDecisionMaker2 () {
      // 弹窗提示表单的完整性
      const missingFields = []
      if (!this.selectedDataset2) {
        missingFields.push('决策案例')
      }
      if (!this.selectedDecisionMakerName2) {
        missingFields.push('蒸馏器名称')
      }
      if (missingFields.length > 0) {
        this.$message({
          message: `请添加${missingFields.join('、')}`,
          type: 'warning'
        })
        return
      }
      // 提交表单
      const payload = {
        selectedDataset: this.selectedDataset2,
        selectedDecisionMakerName: this.selectedDecisionMakerName2
        // selectedDecisionMakerType: this.selectedDecisionMakerType2
      }
      decisionApi.addDecisionMaker2(payload)
        .then(response => {
          this.$message.success('添加成功')
          this.isDecisionMakerAdded2 = true // 更新状态，成功添加了
          // this.startProgress1() // 仪表盘开始计时
          // 这里可以根据需要添加更多的逻辑
        })
        .catch(error => {
          console.error('添加失败', error)
        })
    },
    // 1227GCN决策路径可视化——显示图片
    getVisualizationImage () {
      const params = { param1: this.selectedDataset2, param2: this.selectedDecisionMakerName2 }
      decisionApi.fetchVisualizationImage(params)
        .then(response => {
          if (response.data.meta.code === 200) {
            this.visualizationImageUrl = response.data.data.imageData
          }
        })
        .catch(error => {
          console.error('Error fetching visualization image:', error)
        })
    },
    openModal () {
      this.showModal = true
    },
    closeModal () {
      this.showModal = false
    },
    // 1229决策器名称传递
    fetchDecisionMakers () {
      // axios.get('/decision/get/decisionmakers')
      decisionApi.fetchDecisionMakers()
        .then(response => {
          if (response.data.meta.code === 200) {
            this.decisionMakerOptions = response.data.data.map(name => ({ label: name, value: name }))
          }
        })
        .catch(error => {
          console.error('Error fetching decision makers~~:', error)
          // 处理错误
        })
    },
    // 1229蒸馏器名称传递
    fetchDecisionMakers1 () {
      // axios.get('/decision/get/decisionmakers')
      decisionApi.fetchDecisionMakers1()
        .then(response => {
          if (response.data.meta.code === 200) {
            this.decisionMakerOptions1 = response.data.data.map(name => ({ label: name, value: name }))
          }
        })
        .catch(error => {
          console.error('Error fetching decision makers~~:', error)
          // 处理错误
        })
    },
    // 未使用
    fetchDecisionMakerNames () {
    // 发送请求到后端，URL和方法根据实际情况调整
      decisionApi.fetchDecisionMakers()
        .then(response => {
          this.decisionMakerNames1 = response.data.data
        }).catch(error => {
          console.error('Error fetching decision maker names:', error)
        })
    },
    // 未使用——获取蒸馏器的名称
    fetchDistillerNames () {
      // 发送请求到后端，URL和方法根据实际情况调整
      decisionApi.fetchDecisionMakers1()
        .then(response => {
          this.distillerNames = response.data.data
        }).catch(error => {
          console.error('Error fetching distiller names:', error)
        })
    },
    // 1230交互记录卡片——删除名称——处理决策器名称的点击事件
    handleDecisionMakerNameClick (decisionMakerName) {
      this.$confirm('确定要删除这个决策器吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.deleteDecisionMaker(decisionMakerName)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 1230交互记录卡片——删除决策器名称——向后端发送删除请求
    deleteDecisionMaker (decisionMakerName) {
      decisionApi.deleteDesionMaker(decisionMakerName)
      // this.$axios.post('/api/delete/decisionmaker', { decisionMakerName })
        .then(response => {
          if (response.data.meta.code === 200) {
            this.$message.success('删除成功')
            this.fetchDecisionMakers()
            this.fetchDecisionMakers1()
            // 这里可以添加代码来更新前端的显示，比如重新加载决策器列表
          } else {
            this.$message.error('删除失败！')
          }
        })
        .catch(error => {
          console.error('删除失败~', error)
          this.$message.error('删除时发生错误')
        })
    },
    // 1230交互记录卡片——删除名称——处理蒸馏器名称的点击事件
    handleDecisionMakerNameClick1 (decisionMakerName) {
      this.$confirm('确定要删除这个蒸馏器吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.deleteDecisionMaker1(decisionMakerName)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 1230交互记录卡片——删除蒸馏器名称——向后端发送删除请求
    deleteDecisionMaker1 (decisionMakerName) {
      decisionApi.deleteDesionMaker1(decisionMakerName)
      // this.$axios.post('/api/delete/decisionmaker', { decisionMakerName })
        .then(response => {
          if (response.data.meta.code === 200) {
            this.$message.success('删除成功')
            this.fetchDecisionMakers()
            this.fetchDecisionMakers1()
            // 这里可以添加代码来更新前端的显示，比如重新加载决策器列表
          } else {
            this.$message.error('删除失败！')
          }
        })
        .catch(error => {
          console.error('删除失败~', error)
          this.$message.error('删除时发生错误')
        })
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
  .modal {
  display: block; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0, 0, 0); /* Fallback color */
  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
.modal-image {
  width: 100%; /* 或者使用具体的像素值，例如 800px */
  height: auto; /* 设置为 auto 以保持图片的宽高比 */
  display: block; /* 使图片块级显示 */
  margin: 0 auto; /* 水平居中 */
}
</style>
