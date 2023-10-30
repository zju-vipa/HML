<template>
    <div>
    <el-card>
        <!-- 当前任务 -->
        <h3>结果报告</h3>
        <div>
            <el-button class="opbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
        </div>
        <!-- <div @click="backPage"><i class="el-icon-arrow-left backPage"></i><span>返回</span></div> -->
      <el-row>
        <el-col span="15">
          <el-row v-if="newResultForm.isNewResult==true">
            <div style="text-align: center">
              <el-row>
                <img src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px">
              </el-row>
              <el-row><span style="color: darkgray">暂无记录</span></el-row>
            </div>
          </el-row>
          <el-row v-else>
            <el-col span="10">
              <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }">
                <div slot="header" class="header">
                  <el-row type="flex" align="middle">
                    <el-col span="12">
                      <span class="header-label" style="font-size: 18px; font-weight: bolder">特征可视化</span>
                    </el-col>
                    <el-col span="12" style="text-align: right">
                      <el-link type="success">查看详情</el-link>
                    </el-col>
                  </el-row>
                </div>
                <div style="margin: 15px; text-align: center">
                  <el-row>
                    <el-row><img v-if="newResultForm.isFeatureVisual" src="./../../assets/img/empty-state.png" style="text-align: center; width: 200px; height: 200px"></el-row>
                    <el-row><span style="color: darkgray">暂无数据</span></el-row>
                  </el-row>
                </div>
              </el-card>
            </el-col>
            <el-col span="14">
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
            <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 350px">
              <div slot="header" class="header">
                <el-row type="flex" align="middle">
                  <el-col span="12">
                    <span class="header-label" style="font-size: 18px; font-weight: bolder">人机协同</span>
                  </el-col>
                </el-row>
              </div>
              <div style="margin: 15px; text-align: center">
                <el-row type="flex" align="middle">
                  <el-col span="2"><span style="font-size: 17px; font-weight: bolder">优化建议:</span></el-col>
                  <el-col span="4">
                    <el-row>
                      <el-input v-model="HumanMachineForm.node" placeholder="请输入1-300节点"></el-input>
                    </el-row>
                  </el-col>
                  <el-col span="2"><el-button size="mini">查看</el-button></el-col>
                  <el-col span="4">
                    <el-row>
                      <el-select v-model="HumanMachineForm.operator" placeholder="请选择">
                        <el-option
                          v-for="item in operator_options"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value">
                        </el-option>
                      </el-select>
                    </el-row>
                  </el-col>
                  <el-col span="2"><el-button size="mini">查看</el-button></el-col>
                  <el-col span="5"><span style="font-size: 17px"></span></el-col>
                </el-row>
                <el-row style="text-align: left">
                  <el-col span="2"><div style="border-radius: 4px;min-height: 36px;"></div></el-col>
                  <el-col span="4">
                    <span style="text-align: left; font-size: 15px; color: #373d41;padding-top: 20px">{{HumanMachineForm.node}}号节点的特征有效率:</span>
                  </el-col>
                  <el-col span="2"><div style="border-radius: 4px;min-height: 36px;"></div></el-col>
                  <el-col span="4">
                    <span style="text-align: left; font-size: 15px; color: #373d41;padding-top: 10px">{{HumanMachineForm.operator}}算子的特征有效率:</span>
                  </el-col>
                </el-row>
                <el-row type="flex" align="middle" style="margin-top: 20px">
                  <el-col span="2"><span style="font-size: 17px; font-weight: bolder">专家干预:</span></el-col>
                  <el-col span="20">
                    <el-row type="flex" align="middle" >
                      <el-col span="2"><span style="font-size: 13px;">删除节点:</span></el-col>
                      <el-col style="text-align: left">
                        <el-input v-model="HumanMachineForm.nodesForDelete" placeholder="请输入删除节点列表" style="width: 200px"></el-input>
                      </el-col>
                    </el-row>
                    <el-row type="flex" align="middle" style="padding-top: 20px">
                      <el-col span="2"><span style="font-size: 13px;">添加算子:</span></el-col>
                      <el-col style="text-align: left">
                        <el-checkbox-group v-model="HumanMachineForm.operatorForAdd">
                          <el-checkbox label="求和"></el-checkbox>
                          <el-checkbox label="平均"></el-checkbox>
                        </el-checkbox-group>
                      </el-col>
                    </el-row>
                    <el-row type="flex" align="middle" style="padding-top: 20px">
                      <el-col span="2"><span style="font-size: 13px;">删除算子:</span></el-col>
                      <el-col style="text-align: left">
                        <el-checkbox-group v-model="HumanMachineForm.operatorForDelete">
                          <el-checkbox label="求和"></el-checkbox>
                          <el-checkbox label="平均"></el-checkbox>
                        </el-checkbox-group>
                      </el-col>
                    </el-row>
                  </el-col>
                </el-row>
              </div>
              <el-row>
                <el-col span="2"><div style="border-radius: 4px;min-height: 36px;"></div></el-col>
                <el-button type="primary">继续学习</el-button>
              </el-row>

            </el-card>
          </el-row>
        </el-col>
        <el-col span="9">
          <el-card class="box-card" shadow="always" :body-style="{ padding: '0px' }" style="height: 670px">
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
                <el-table-column label="交互次数" type="index"> </el-table-column>
                <el-table-column prop="record_efficiency" label="当前特征有效率"></el-table-column>
                <el-table-column prop="record_accuracy" label="任务准确度"></el-table-column>
              </el-table>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
    </div>
</template>
<script>
// import queryFeaApi from './../../api/queryFea'
// 操作状态

export default {

  data () {
    return {
      newResultForm: {
        efficiency: 70,
        accuracy: 80,
        isNewResult: false,
        isFeatureVisual: true
      },
      HumanMachineForm: {
        node: 0,
        operator: '',
        nodesForDelete: '',
        operatorForAdd: '',
        operatorForDelete: ''
      },
      operator_options: [{ value: '0', label: '求和' }],
      IteractionRecord: [{ record_efficiency: '10%', record_accuracy: '10%' }]
    }
  },

  created () {
    // this.getHumanFeaInfo()
    // 暂时用假数据替代

  },
  mounted () {

  },
  methods: {
    backPage () {
      this.$router.back()
    }
  }
}
</script>

<style scoped>
  /* h3{
    text-align: center;
  } */
  .backPage{
    margin-bottom: 30px;
    margin-left: 10px;
    font-size: 15px;
    color: #367FA9;
    font-weight: bold;
    margin-right: 10px;
  }
  .el-card{
    margin: 10px 20px;
  }
  h3{
    padding-bottom: 10px;
    border-bottom: 3px solid rgb(102, 102, 102)
  }
  .opbtn{
    margin-bottom: 10px;
  }
  /* .el-button--goon.is-active,
  .el-button--goon:active {
    background: #20B2AA;
    border-color: #20B2AA;
    color: #fff;
  }
  .el-button--goon:focus,
  .el-button--goon:hover {
    background: #48D1CC;
    border-color: #48D1CC;
    color: #fff;
  }
  .el-button--goon {
    color: #FFF;
    background-color: #20B2AA;
    border-color: #20B2AA;
  } */
  .box-card {
    height: 300px;
    .header {
      position: relative;
      .label{
        padding: 0 3px;
        background-color: #fdf0da;
        color: #f19901;
      }
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

</style>
