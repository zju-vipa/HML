<template>
  <div>
    <!-- 卡片区域 -->
    <el-card>
      <el-button class="queryBtn" @click="queryFeatureEng" type="primary">查看特征工程</el-button>
           <!-- 表单区域 -->
      <el-form label-position="right" label-width="250px" :model="addFeatureForm" :rules="addFeatureFormRules" ref="addFeatureFormRef" class="demo-ruleForm">
            <el-form-item class="label" label="特征工程名" prop="featureEng_name">
              <el-input clearable style="width:410px" v-model="addFeatureForm.featureEng_name" placeholder="请填写特征工程名"></el-input>
            </el-form-item>
            <el-form-item class="label" label="特征工程类型" prop="featureEng_type">
              <el-input disabled="" style="width:410px" v-model="addFeatureForm.featureEng_type"></el-input>
            </el-form-item>
            <el-form-item class="label" label="特征工程步骤" prop="featureEng_processes">
              <el-card class="card-form">
                <el-form label-width="100px" label-position="left" :model="processConstructForm">
                  <el-form-item  label="特征构建">
                      <el-select style="width:220px" v-model="processConstructForm.operate_name" placeholder="请选择特征"
                    @change="handleselectTrainname">
                      <el-option
                        v-for="(item,index) in algorithm_name" :key="index"
                        :label="item"
                        :value="item">
                      </el-option>
                    </el-select>
                  </el-form-item >
                    <el-form-item class="label" v-for="(params, index) in algorithm_parameters"
                      :label="params.name" :key="index">
                        <el-select v-if="params.name==='col_retain'"  :multiple="labelMultible"
                          v-model="params.value" placeholder="请选择保留列">
                            <el-option
                              v-for="(item,index) in columnsList" :key="index"
                              :label="item"
                              :value="item">
                            </el-option>
                        </el-select>
                        <el-input v-else style="width:350px" v-model="params.value"></el-input>
                    </el-form-item>
                </el-form>
              </el-card>
              <el-card class="card-form">
                  <el-form label-width="100px" label-position="left"  :model="processExtractForm">
                    <el-form-item  label="特征提取">
                        <el-select style="width:220px" @change="handleselectTrainname2"
                        v-model="processExtractForm.operate_name" placeholder="请选择特征">
                        <el-option
                          v-for="(item,index) in algorithm_name2" :key="index"
                          :label="item"
                          :value="item">
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item class="label" v-for="(params, index) in algorithm_parameters2"
                      :label="params.name" :key="index">
                        <el-select v-if="params.name==='col_retain'"  :multiple="labelMultible2"
                          v-model="params.value" placeholder="请选择保留列">
                            <el-option
                              v-for="(item,index) in columnsList" :key="index"
                              :label="item"
                              :value="item">
                            </el-option>
                        </el-select>
                        <el-input v-else style="width:220px" v-model="params.value"></el-input>
                    </el-form-item>
                </el-form>
              </el-card>

            </el-form-item>
            <el-form-item class="label" label="新数据集名称" prop="new_dataset_name" >
              <el-input style="width:410px" clearable  v-model="addFeatureForm.new_dataset_name" placeholder="请填写新数据集名称"></el-input>
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
        featureEng_type: 'Manual',
        featureEng_processes: [
        ],
        original_dataset_id: '',
        new_dataset_name: ''
      },
      operate_nameValue1: '',
      operate_columnsValue1: [],
      operate_columnsValue2: [],
      operate_nameValue2: '',
      n_componentsValue: 1,
      algorithm_name: [],
      algorithm_name2: [],
      algorithm_name3: [],
      addFeatureFormRules: {
        feature_name: [
          { required: true, message: '请选择特征', trigger: 'blur' }
        ]
      },
      // 在特征首页选择的数据集及其列名
      OriginDatasetId: '',
      columnsList: [],
      algorithm_category: 'FeatureEng_construct',
      // 根据算法类型收到的算法总数据
      algorithm_Options: [],
      // 算法参数
      algorithm_parameters: {},
      labelMultible: false,
      algorithm_category2: 'FeatureEng_extract',
      // 根据算法类型收到的算法总数据
      algorithm_Options2: [],
      algorithm_Options3: [],
      // 算法参数
      algorithm_parameters2: {},
      labelMultible2: false,
      processConstructForm: {},
      processExtractForm: {}

    }
  },
  created () {
    this.getOriginDatasetId()
    this.getAlgorithm()
  },
  methods: {
    // 点击确定按钮，提交上传数据表单
    submitHumanForm () {
      console.log(this.processExtractForm.algorithm_parameters2)
      console.log(this.processConstructForm.algorithm_parameters)
      if (this.processExtractForm.algorithm_parameters2 !== undefined) {
        for (let i = 0; i < this.processExtractForm.algorithm_parameters2.length; i++) {
          this.processExtractForm[this.processExtractForm.algorithm_parameters2[i].name] = this.processExtractForm.algorithm_parameters2[i].value
        }
        this.addFeatureForm.featureEng_processes.push(this.processExtractForm)
      }
      if (this.processConstructForm.algorithm_parameters !== undefined) {
        for (let i = 0; i < this.processConstructForm.algorithm_parameters.length; i++) {
          this.processConstructForm[this.processConstructForm.algorithm_parameters[i].name] = this.processConstructForm.algorithm_parameters[i].value
        }
        this.addFeatureForm.featureEng_processes.push(this.processConstructForm)
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
        this.algorithm_Options = response.data.data
        this.algorithm_name = response.data.data.map(item => item.algorithm_name)
        // console.log(this.algorithm_Options)
      })
      learnApi.queryAlgorithm(this.algorithm_category2).then(response => {
        this.algorithm_Options2 = response.data.data
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
      this.getColumns()
      for (let i = 0; i < this.algorithm_Options.length; i++) {
        if (this.algorithm_Options[i].algorithm_name === this.processConstructForm.operate_name) {
          // 首先，将返回的json格式转换一下
          this.algorithm_parameters = JSON.parse(this.algorithm_Options[i].algorithm_parameters)
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
    // 当训练方法发生改变的时候
    handleselectTrainname2 () {
      this.getColumns()
      for (let i = 0; i < this.algorithm_Options2.length; i++) {
        if (this.algorithm_Options2[i].algorithm_name === this.processExtractForm.operate_name) {
          this.algorithm_parameters2 = JSON.parse(this.algorithm_Options2[i].algorithm_parameters)
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
    width:390px;
    box-shadow: none;
  }
</style>
