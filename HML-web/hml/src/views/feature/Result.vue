<template>
    <div>
    <el-card>
        <!-- 当前任务 -->
        <h3>结果报告</h3>
        <div>
            <el-button class="opbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
        </div>
        <!-- <div @click="backPage"><i class="el-icon-arrow-left backPage"></i><span>返回</span></div> -->
      <div v-if="newResultForm.checkedModules.length==4">
        <el-col span="16">
          <el-row v-if="newResultForm.isNewResult==false">
            <div style="text-align: center">
              <el-row>
                <img src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px">
              </el-row>
              <el-row><span style="color: darkgray">暂无记录</span></el-row>
            </div>
          </el-row>
          <el-row v-else-if="newResultForm.isNewResult==true && newResultForm.checkedModules.length==4">
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
                      <span class="header-label" style="font-size: 18px; font-weight: bolder">初始效果</span>
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
                      <span style="color: steelblue; font-size: 18px;">初始特征有效率</span>
                    </el-col>
                    <el-col span="12">
                      <el-row>
                        <el-progress type="dashboard" :percentage="newResultForm.accuracy" :stroke-width="20" :width="165" style="font-weight: bolder; font-size: 20px;">
                        </el-progress>
                      </el-row>
                      <span style="color: steelblue; font-size: 18px;">初始任务准确率</span>
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
                <el-button type="primary">继续学习</el-button>
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
          <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 550px">
            <div slot="header" class="header">
              <el-row type="flex" align="middle">
                <el-col span="12">
                  <span class="header-label" style="font-size: 18px; font-weight: bolder">前100重要特征</span>
                </el-col>
              </el-row>
            </div>
            <div style="margin: 15px; text-align: center;">
              <div id="featureCharts" style="width: 400px; height: 500px; margin: 0 auto"></div>
            </div>
          </el-card>
        </el-col>
      </div>
      <div v-else>
        <el-col span="16">
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
                    <el-col span="5">
                      <h3 style="text-align: left">{{item.label}}</h3>
                    </el-col>
                    <el-col span="19" style="text-align: left">
                      <h4 style="font-weight: lighter">{{item.value}}</h4>
                    </el-col>
                  </el-row>
                  <el-row style="line-height: 5px" type="flex" align="middle">
                    <el-col span="5">
                      <h3 style="text-align: left">已选功能模块</h3>
                    </el-col>
                    <el-col span="19">
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
                      <span class="header-label" style="font-size: 18px; font-weight: bolder">初始效果</span>
                    </el-col>
                  </el-row>
                </div>
                <div style="margin: 15px; text-align: center; height: 300px">
                  <el-row>
                    <el-col span="12">
                      <el-row>
                        <el-progress type="dashboard" :percentage="newResultForm.efficiency" :stroke-width="20" :width="190" style="font-weight: bolder; font-size: 20px;">
                        </el-progress>
                      </el-row>
                      <span style="color: steelblue; font-size: 18px;">初始特征有效率</span>
                    </el-col>
                    <el-col span="12">
                      <el-row>
                        <el-progress type="dashboard" :percentage="newResultForm.accuracy" :stroke-width="20" :width="190" style="font-weight: bolder; font-size: 20px;">
                        </el-progress>
                      </el-row>
                      <span style="color: steelblue; font-size: 18px;">初始任务准确率</span>
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
            <div id="featureCharts" style="width: 400px; height: 500px; margin: 0 auto"></div>
          </el-card>
        </el-col>
      </div>
    </el-card>
    </div>
</template>
<script>
// import queryFeaApi from './../../api/queryFea'
// 操作状态
import * as echarts from 'echarts'

const moduleOptions = [
  { value: '1', label: '特征解耦' },
  { value: '2', label: '特征学习' },
  { value: '3', label: '特征衍生' },
  { value: '4', label: '特征选择' }
]

export default {
  data () {
    return {
      moduleOptions,
      newResultForm: {
        efficiency: 87.63,
        accuracy: 89.35,
        isNewResult: true,
        isFeatureVisual: true,
        checkedModules: ['1', '2', '3', '4'],
        taskDetails: [
          { type: 'name', label: '特征工程名', value: '暂稳数据集1号特征工程' },
          { type: 'type', label: '特征工程类型', value: '人机协同特征衍生与选择' },
          { type: 'network', label: '网络拓扑', value: '300节点电网' },
          { type: 'mode', label: '运行方式', value: '001夏平初始' },
          { type: 'dataset', label: '数据集', value: '故障定位数据集' }
        ]
      },
      HumanMachineForm: {
        node: 0,
        operator: '',
        nodesForDelete: '',
        operatorForAdd: '',
        operatorForDelete: ''
      },
      HumanInLoopForm: {
        node: 0,
        operator: '',
        nodesForDelete: '',
        operatorForAdd: '',
        operatorForDelete: ''
      },
      taskFeatureColumnsList: [{ label: '特征名', prop: 'name' },
        { label: '所属数据集', prop: 'dataset' },
        { label: '针对任务', prop: 'task' },
        { label: '特征解耦', prop: 'featureDecoupling' },
        { label: '特征学习', prop: 'featureLearning' },
        { label: '特征衍生', prop: 'featureDerivation' },
        { label: '特征选择', prop: 'featureSelection' }],
      taskFeatureList: [],
      loading: false,
      pagination_taskFeatureList: {
        page: 1,
        pageSize: 20,
        total: 0
      },
      totalPage_taskFeatureList: 5,
      countTotal_taskFeature: 15,
      selectedIds: [],
      operator_options: [{ value: '0', label: '求和' }],
      IteractionRecord: [{ record_efficiency: '87.63%', record_accuracy: '89.35%' }]
    }
  },

  created () {
    // this.getHumanFeaInfo()
    // 暂时用假数据替代
    // 用假数据暂时替代
    this.taskFeatureList = []
    for (let i = 0; i < this.countTotal_taskFeature; i++) {
      const nameString = String.fromCharCode(i / 4 + 65) + '_' + i % 4
      this.taskFeatureList.push({ name: nameString, dataset: '暂稳数据集', task: '---', featureDecoupling: '---', featureLearning: '---', featureDerivation: '---', featureSelection: '---' })
    }
  },
  mounted () {
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
            this.$message.warning('当前任务生成特征已全部加载')
          }
          if (this.pagination_taskFeatureList.page < this.totalPage_taskFeatureList) {
            this.pagination_taskFeatureList.page = this.pagination_taskFeatureList.page + 1
            console.log('页面已经到达底部,可以请求接口,请求第' + this.pagination_taskFeatureList.page + '页数据')
            var cIndex = this.countTotal_taskFeature + 10
            for (let i = (this.countTotal_taskFeature + 1); i <= cIndex; i = i + 1) {
              const nameString = String.fromCharCode(i / 4 + 65) + '_' + i % 4
              this.taskFeatureList.push({ name: nameString, dataset: '暂稳数据集', task: '---', featureDecoupling: '---', featureLearning: '---', featureDerivation: '---', featureSelection: '---' })
            }
            this.countTotal_taskFeature += 10
          }
        }
      })
    },
    backPage () {
      this.$router.back()
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
