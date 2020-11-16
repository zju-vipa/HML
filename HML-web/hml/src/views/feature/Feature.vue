<template>
    <div>
      <!-- 卡片区域 -->
      <el-card >
        <!-- form区域 -->
          <el-form   label-width="100px" label-position="right" :model="chooseDatasetForm" ref="chooseDatasetFormRef">
            <el-form-item prop="dataset_name" label="数据集">
              <el-input clearable  readonly v-model="chooseDatasetForm.dataset_name" style="width: 300px"
                        @click.native="datasetDialogVisible=true" placeholder="请选择数据集"></el-input>
            </el-form-item>
            <el-form-item label="特征工程">
              <el-row>
                <el-col :span="5">
                  <el-button type="primary" round @click="goHumanFea">人工特征工程</el-button>
                </el-col>
                <el-col :span="5">
                  <el-button type="primary" round>自动化特征工程</el-button>
                </el-col>
                <el-col :span="5">
                  <el-button type="primary" round>人在回路的特征工程</el-button>
                </el-col>
              </el-row>
            </el-form-item>
          </el-form>
          <h3>数据集展示</h3>
          <el-table :data="datasetDetailList" border stripe  style="width: 100%">
          <!-- <el-table-column  label="序号" type="index" width="120"> </el-table-column> -->
          <el-table-column width="120" v-for="(item,id) in columnsList" :key="id" :prop="item" :label="item"></el-table-column>
          <!-- <el-table-column prop="age" label="数据集类型"> </el-table-column>
          <el-table-column prop="checking_status" label="数据集介绍"> </el-table-column> -->
        </el-table>
      </el-card>
<!--      选择数据集，弹出的窗口-->
      <el-dialog title="选择数据集" :visible.sync="datasetDialogVisible" @close="getColumns">
        <dataset :isDialog="true" @dataset-choose = chooseDataset></dataset>
        <!-- <supplier :isDialog="true" @supplier-choose="supplierChoose"></supplier> -->
      </el-dialog>
    </div>
</template>

<script>
import Dataset from '../data/OriginDataset'
import featureApi from '../../api/feature'
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
      datasetId: '',
      // 弹出数据集对话框
      datasetDialogVisible: false,
      // 用来接收数据集的列名
      columnsList: [],
      // 用来接受数据集的具体数据
      datasetDetailList: []
    }
  },
  methods: {
    // 接受数据集组件传来的数据
    chooseDataset (currentRow) {
      this.chooseDatasetForm.dataset_name = currentRow.dataset_name
      this.chooseDatasetForm.dataset_id = currentRow.dataset_id
      this.datasetId = currentRow.dataset_id
      console.log(this.datasetId)
      this.datasetDialogVisible = false
      console.log(currentRow)
    },
    // 获取数据集列名
    getColumns () {
      // console.log(this.datasetId)
      if (this.datasetId !== '') {
        featureApi.getDatasetColumns(this.datasetId).then(response => {
          console.log(response)
          const resp = response.data
          if (resp.meta.code === 200) {
            this.$message.success('获取数据集成功')
          }
          this.columnsList = resp.data
          localStorage.setItem('datasetId', this.datasetId)
          console.log(this.columnsList)
        })
        featureApi.getData(this.datasetId).then(response => {
          console.log(response)
          const resp = response.data
          // if (resp.meta.code === 200) {
          //   this.$message.success('获取数据集成功')
          // }
          this.datasetDetailList = resp.data
          console.log(this.datasetDetailList)
        })
      }
    },
    // 跳转到人工特征工程页面
    goHumanFea () {
      this.$emit('columns-get', this.columnsList)
      this.$router.push('/feature/humanfea')
    }
  }
}
</script>

<style scoped>
  .el-form {
    margin: 10px auto;
    /* width: 1000px; */
  }
  .el-button{
    width: 150px;
  }
</style>
