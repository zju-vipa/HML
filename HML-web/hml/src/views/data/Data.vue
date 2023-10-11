<template>
    <div>
<!--      tab便签区域-->
      <el-card>
        <div class="buttons">
          <el-button @click="gotoPowerNetDataset" type="primary">电网数据</el-button>
          <el-button @click="queryDataset" type="primary">查看原数据集</el-button>
          <el-button @click="queryDatasetHuFea" type="primary">查看特征处理数据集</el-button>
        </div>
        <el-form status-icon :model="uploadForm" :rules="uploadFormRules" ref="uploadFormRef"
                  label-width="200px" label-position="right">
            <el-form-item label="数据集名称" prop="dataset_name">
                  <el-input style="width:400px" clearable  v-model="uploadForm.dataset_name" placeholder="请输入数据集名称"></el-input>
            </el-form-item>
            <el-form-item label="是否公开" prop="if_public">
                <el-select v-model="uploadForm.if_public" placeholder="请选择是否公开" style="width: 400px">
                  <el-option v-for="option in publicOption" :key="option.type" :label="option.name" :value="option.type"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="是否进行分析" prop="if_profile">
              <el-select v-model="uploadForm.if_profile" placeholder="请选择是否分析" style="width:400px">
                <el-option label="是" :value=true></el-option>
                <el-option label="否" :value=false></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="数据简介" prop="introduction">
                <el-input clearable  type="textarea" style="width:400px"
                        v-model="uploadForm.introduction"></el-input>
            </el-form-item>
            <el-form-item >
              <el-row :gutter="40">
                <el-col :span="5">
                  <el-upload  :action="uploadURL"
                  list-type="text"
                  :headers="headers"
                  :on-success="handleSuccess">
                    <el-button  type="primary" icon="el-icon-document-add">导入</el-button>
                  </el-upload>
                </el-col>
                <el-col :span="5">
                  <el-button  type="primary" @click="submitDataForm">上传<i class="el-icon-upload el-icon--right"></i></el-button>
                </el-col>
              </el-row>
            </el-form-item>
        </el-form>
      </el-card>
    </div>
</template>

<script>
import datasetApi from '../../api/dataset'
// import request from '../../utils/request'
// 是否公开
const publicOption = [
  { type: true, name: '是' },
  { type: false, name: '否' }
]

export default {
  name: 'Data',
  computed: {
    headers () {
      return {
        // 这里一定要转成json，要不然就有双引号，token就出错了
        Authorization: JSON.parse(localStorage.getItem('token'))
        // 'content-type': 'multipart/form-data'
      }
    }
  },
  data () {
    return {
      publicOption,
      // Tab标签激活的名字
      activeName: 'upload',
      // 上传数据的表单
      uploadForm: {
        dataset_name: '',
        if_public: false,
        introduction: '',
        tmp_file_path: '',
        dataset_id: '',
        if_profile: false
      },
      // 上传文件地址
      // uploadURL: 'http://192.168.137.8:8021/api/private/v1/dataset/upload',
      uploadURL: 'http://10.214.211.137:8021/api/private/v1/dataset/upload',
      uploadFormRules: {
        dataset_name: [
          { required: true, message: '请输入数据名称', trigger: 'blur' }
        ],
        if_public: [
          { required: true, message: '请选择是否公开', trigger: 'blur' }
        ],
        introduction: [
          { required: true, message: '请输入数据简介', trigger: 'blur' }
        ]
      }
    }
  },
  created () {
  },
  methods: {
    // 点击确定按钮，提交上传数据表单
    submitDataForm () {
      this.$refs.uploadFormRef.validate(valid => {
        if (valid) {
          datasetApi.addDataset(this.uploadForm).then(response => {
            const resp = response.data
            console.log(response)
            if (resp.meta.code === 200) {
              this.$message.success('数据上传成功')
            } else {
              this.$message.error('数据上传失败')
            }
          })
        }
      })
    },
    // 点击上传按钮，文件一旦上传成功调用这个函数
    handleSuccess (response) {
      console.log(response)
      const resp = response.data
      if (response.meta.code === 200) {
        this.$message.success('导入数据集成功')
      } else {
        this.$message.error('导入数据集失败')
      }
      this.uploadForm.dataset_id = resp.dataset_id
      this.uploadForm.tmp_file_path = resp.tmp_file_path
    },
    // 查询数据集按钮
    queryDataset () {
      this.$router.push('/data/originDataset')
    },
    // 查询数据集按钮
    queryDatasetHuFea () {
      this.$router.push('/data/humanDataset')
    },
    downDataset () {
      datasetApi.download(this.uploadForm.dataset_id).then(response => {
        console.log(response)
      })
    },
    // 前往电网数据生成
    gotoPowerNetDataset () {
      this.$router.push('/data/powerNet')
    }
  }
}
</script>

<style scoped>
  .el-form {
    margin-top: 80px;
  }
  .buttons{
    float: right;
  }
  .queryBtn{
    width: 120px;
  }
</style>
