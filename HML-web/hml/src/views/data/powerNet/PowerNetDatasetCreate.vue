<template>
  <div>
    <!-- 标题 -->
    <div>
      <el-col :span="2">
        <el-button class="backbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
      </el-col>
      <el-col :span="22">
        <h2>电网数据生成任务创建</h2>
      </el-col>
    </div>
    <div>
      <!-- 任务信息 -->
      <el-card>
        <div><h3>Step 1: 任务设置</h3></div>
        <el-form label-position="right" label-width="150px" :model="powerNetJobInfo" :rules="powerNetJobInfoFormRules" ref="powerNetJobInfoFormRef" class="demo-ruleForm">
          <el-row>
            <el-col :span="10">
              <el-form-item label="任务名称" prop="pn_job_name">
                <el-input v-model="powerNetJobInfo.pn_job_name" style="width: 300px"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item label="生成方式" prop="pn_job_type">
                <el-select v-model="powerNetJobInfo.pn_job_type" style="width: 300px">
                  <el-option v-for="(option, index) in generateTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
              <el-col :span="20">
              <el-form-item label="任务描述" prop="pn_job_description">
                <el-input v-model="powerNetJobInfo.pn_job_description" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
      <!-- 初始电网信息 -->
      <el-card>
        <div><h3>Step 2: 初始电网选择</h3></div>
        <el-form label-position="right" label-width="150px" :model="initPowerNetInfo" :rules="initPowerNetInfoFormRules" ref="initPowerNetInfoFormRef" class="demo-ruleForm">
          <el-row>
            <el-col :span="10">
              <el-form-item label="样例名称" prop="init_net_name">
                <el-select v-model="initPowerNetInfo.init_net_name" @change="handleInitNetChange" style="width: 300px">
                  <el-option v-for="(option, index) in initNetOptions" :key="index" :label="option" :value="option"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
              <el-col :span="20">
              <el-form-item label="样例描述" prop="init_net_description">
                <el-input disabled v-model="initPowerNetInfo.init_net_description" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <!-- 初始电网统计信息 -->
        <el-table :data="initPowerNetInfo.init_net_component_number" border stripe style="width: 100%">
          <el-table-column prop="bus_number" label="母线数量"></el-table-column>
          <el-table-column prop="load_number" label="负荷数量"></el-table-column>
          <el-table-column prop="gen_number" label="电机数量"></el-table-column>
          <el-table-column prop="line_number" label="线路数量"></el-table-column>
        </el-table>
        <!-- 初始电网组件信息 -->
        <div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card style="height: 400px">
              <div><h3>母线</h3></div>
              <el-table :data="initPowerNetInfo.init_net_components.bus" border stripe
                height="300" style="width:100%">
                <el-table-column width="120" v-for="(item,index) in componentColumns.bus"
                  :key="index" :prop="item" :label="item" :formatter="formatValues"></el-table-column>
              </el-table>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card style="height: 400px">
              <div><h3>负荷</h3></div>
              <el-table :data="initPowerNetInfo.init_net_components.load" border stripe
                height="300" style="width:100%">
                <el-table-column width="120" v-for="(item,index) in componentColumns.load"
                  :key="index" :prop="item" :label="item" :formatter="formatValues"></el-table-column>
              </el-table>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card style="height: 400px">
              <div><h3>电机</h3></div>
              <el-table :data="initPowerNetInfo.init_net_components.gen" border stripe
                height="300" style="width:100%">
                <el-table-column width="120" v-for="(item,index) in componentColumns.gen"
                  :key="index" :prop="item" :label="item" :formatter="formatValues"></el-table-column>
              </el-table>
            </el-card>
          </el-col>
          <!-- 其他组件 默认line -->
          <el-col :span="12">
            <el-card style="height: 400px">
              <div>
                  <el-select style="padding-bottom: 10px" v-model="initPowerNetInfo.init_net_components.other_select" @change="handleOtherComponentChange">
                    <el-option v-for="(option, index) in otherSelectOptions" :key="index" :label="option" :value="option"></el-option>
                  </el-select>
              </div>
              <el-table :data="initPowerNetInfo.init_net_components.other" border stripe
                height="300" style="width:100%">
                <el-table-column width="120" v-for="(item,index) in componentOtherColumns"
                  :key="index" :prop="item" :label="item" :formatter="formatValues"></el-table-column>
              </el-table>
            </el-card>
          </el-col>
        </el-row>
        <el-row align="middle" style="margin-bottom: 30px">
          <el-col align="center">
            <img :src="initPowerNetInfo.init_net_topo_url">
          </el-col>
        </el-row>
      </div>
      </el-card>
      <!-- 扰动参数设置 -->
      <el-card>
        <div><h3>Step 3: 扰动参数设置</h3></div>
        <el-form label-position="right" label-width="150px" :model="disturbSettings" :rules="disturbSettingsFormRules" ref="disturbSettingsFormRef" class="demo-ruleForm">
          <el-row>
            <el-col :span="24">
              <el-form-item label="扰动源类型" prop="disturb_src_type_list">
                <el-checkbox-group v-model="disturbSettings.disturb_src_type_list">
                  <el-checkbox label="gen_p">电机P</el-checkbox>
                  <el-checkbox label="gen_v">电机V</el-checkbox>
                  <el-checkbox label="load_p">负荷P</el-checkbox>
                  <el-checkbox label="load_q">负荷Q</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="20">
              <el-form-item label="扰动源个数" prop="disturb_n_var">
                <el-input v-model.number="disturbSettings.disturb_n_var" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="20">
              <el-form-item label="扰动范围" prop="disturb_radio">
                <el-input v-model.number="disturbSettings.disturb_radio" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="20">
              <el-form-item label="扰动次数" prop="disturb_n_sample">
                <el-input v-model.number="disturbSettings.disturb_n_sample" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <el-button class="createbtn" size="medium" type="primary" @click="addPowerNetDataset">一键生成</el-button>
      </el-card>
    </div>
  </div>
</template>
<script>
import queryPowerNetApi from './../../../api/queryPowerNet'
// 生成方式类型
const generateTypeOptions = [
  { type: 'A', name: '方式A' },
  { type: 'B', name: '方式B' },
  { type: 'C', name: '方式C' }
]
// 样例名称
const initNetOptions = ['case5', 'case9', 'case14', 'case30', 'case_ieee30', 'case39', 'case57', 'case118', 'case300']
// 其他组件内容选择
const otherSelectOptions = ['line', 'shunt', 'switch', 'impedance', 'trafo']
const componentColumns = {
  bus: ['name', 'vn_kv', 'type', 'zone', 'max_vm_pu', 'min_vm_pu', 'in_service'],
  load: ['name', 'bus', 'p_mw', 'q_mvar', 'const_z_percent', 'const_i_percent', 'sn_mva', 'scaling',
    'in_service', 'type', 'controllable'
    // 'max_p_mw', 'min_p_mw', 'max_q_mvar', 'min_q_mvar'
  ],
  gen: ['name', 'type', 'bus', 'p_mw', 'vm_pu', 'sn_mva', 'min_q_mvar', 'max_q_mvar',
    'scaling', 'max_p_mw', 'min_p_mw',
    // 'vn_kv', 'xdss_pu', 'rdss_pu', 'cos_phi',
    'in_service'],
  line: ['name', 'std_type', 'from_bus', 'to_bus', 'length_km', 'r_ohm_per_km', 'x_ohm_per_km', 'c_nf_per_km',
    // 'r0_ohm_per_km', 'x0_ohm_per_km', 'c0_nf_per_km',
    'g_us_per_km', 'max_i_ka', 'parallel', 'df', 'type',
    'max_loading_percent',
    // 'endtemp_degree',
    'in_service'],
  shunt: ['name', 'bus', 'p_mw', 'q_mvar', 'vn_kv', 'step', 'in_service'],
  switch: ['name', 'bus', 'element', 'et', 'type', 'closed'],
  impedance: ['name', 'from_bus', 'to_bus', 'rft_pu', 'xft_pu', 'rtf_pu', 'xtf_pu', 'sn_mva', 'in_service'],
  trafo: ['name', 'std_type', 'hv_bus', 'lv_bus', 'sn_mva', 'vn_hv_kv', 'vn_lv_kv', 'vk_percent',
    'vkr_percent', 'pfe_kw', 'i0_percent',
    // 'vk0_percent', 'vkr0_percent', 'mag0_percent', 'mag0_rx', 'si0_hv_partial','vector_group',
    'shift_degree', 'tap_side', 'tap_neutral', 'tap_min', 'tap_max', 'tap_step_percent', 'tap_step_degree',
    'tap_pos', 'tap_phase_shifter', 'parallel', 'max_loading_percent', 'df', 'in_service']
}
export default {
  filters: {
    // is_done转换成 “已完成” “未完成”
    // applyJobStatusTrans (type) {
    //   return type ? '已完成' : '未完成'
    // }
  },
  data () {
    return {
      // 提交表单形式
      addPowerNetDatasetForm: {},
      powerNetJobInfoFormRules: {
        pn_job_name: [
          { required: true, message: '请填写任务名称', trigger: 'blur' }
        ],
        pn_job_type: [
          { required: true, message: '请选择生成方式', trigger: 'blur' }
        ]
      },
      initPowerNetInfoFormRules: {
        init_net_name: [
          { required: true, message: '请选择样例名称', trigger: 'blur' }
        ]
      },
      disturbSettingsFormRules: {
        disturb_src_type_list: [
          { required: true, message: '请选择扰动源类型', trigger: 'blur' }
        ],
        disturb_n_var: [
          { required: true, message: '请填写扰动源个数', trigger: 'blur' }
        ],
        disturb_radio: [
          { required: true, message: '请填写扰动源范围', trigger: 'blur' }
        ],
        disturb_n_sample: [
          { required: true, message: '请填写扰动次数', trigger: 'blur' }
        ]
      },
      // 任务ID，名称，生成方式，描述
      powerNetJobInfo: {
        pn_job_id: '',
        pn_job_name: '',
        pn_job_type: 'A',
        pn_job_description: '略'
      },
      // 初始电网样例名称，描述，网络结构，拓扑图
      initPowerNetInfo: {
        init_net_name: 'case5',
        init_net_description: '',
        init_net_component_number: [{
          bus_number: 0,
          load_number: 0,
          gen_number: 0,
          line_number: 0
        }],
        init_net_components: {
          bus: [],
          load: [],
          gen: [],
          other_select: 'line',
          other: [],
          line: [],
          shunt: [],
          switch: [],
          impedance: [],
          trafo: []
        },
        // columns_list: ['a', 'b', 'c', 'd'],
        init_net_topo_url: require('@/assets/img/logo.png')
      },
      // 扰动源类型，扰动源个数，扰动范围，扰动次数
      disturbSettings: {
        disturb_src_type_list: ['gen_p'],
        disturb_n_var: 1,
        disturb_radio: 5,
        disturb_n_sample: 20
      },
      // to do
      // 潮流计算结果
      powerFlowResultData: [],
      generateTypeOptions,
      initNetOptions,
      otherSelectOptions,
      componentColumns,
      componentOtherColumns: []
    }
  },
  created () {
    // this.getPowerNetJobInfo(this.$route.query.jobId)
    this.handleInitNetChange()
  },
  methods: {
    // 根据样例名称获得样例描述、组件数统计、组件内容、网络拓扑图
    handleInitNetChange () {
      queryPowerNetApi.queryNetDescription(this.initPowerNetInfo.init_net_name).then(response => {
        console.log(response)
        // console.log(this.initPowerNetInfo.init_net_components.other_select)
        const resp = response.data
        if (resp.meta.code === 200) {
          this.$message.success('加载样例成功')
          // 获得样例描述
          this.initPowerNetInfo.init_net_description = resp.data.example
          // 获得组件数
          this.initPowerNetInfo.init_net_component_number = [{
            bus_number: resp.data.description.bus_number,
            load_number: resp.data.description.load_number,
            gen_number: resp.data.description.gen_number,
            line_number: resp.data.description.line_number
          }]
          // 获得各种组件的内容
          this.initPowerNetInfo.init_net_components = {
            bus: resp.data.component.bus,
            load: resp.data.component.load,
            gen: resp.data.component.gen,
            other_select: 'line',
            other: resp.data.component.line,
            line: resp.data.component.line,
            shunt: resp.data.component.shunt,
            switch: resp.data.component.switch,
            impedance: resp.data.component.impedance,
            trafo: resp.data.component.trafo
          }
          this.componentOtherColumns = this.componentColumns.line
          // 获得拓扑图
          this.initPowerNetInfo.init_net_topo_url = resp.data.img_url
        }
      })
    },
    // 根据选择的组件类型显示“其他”块的组建内容
    handleOtherComponentChange () {
      if (this.initPowerNetInfo.init_net_components.other_select === 'line') {
        this.initPowerNetInfo.init_net_components.other = this.initPowerNetInfo.init_net_components.line
        this.componentOtherColumns = this.componentColumns.line
      } else if (this.initPowerNetInfo.init_net_components.other_select === 'shunt') {
        this.initPowerNetInfo.init_net_components.other = this.initPowerNetInfo.init_net_components.shunt
        this.componentOtherColumns = this.componentColumns.shunt
      } else if (this.initPowerNetInfo.init_net_components.other_select === 'switch') {
        this.initPowerNetInfo.init_net_components.other = this.initPowerNetInfo.init_net_components.switch
        this.componentOtherColumns = this.componentColumns.switch
      } else if (this.initPowerNetInfo.init_net_components.other_select === 'impedance') {
        this.initPowerNetInfo.init_net_components.other = this.initPowerNetInfo.init_net_components.impedance
        this.componentOtherColumns = this.componentColumns.impedance
      } else if (this.initPowerNetInfo.init_net_components.other_select === 'trafo') {
        this.initPowerNetInfo.init_net_components.other = this.initPowerNetInfo.init_net_components.trafo
        this.componentOtherColumns = this.componentColumns.trafo
      } else {
        this.initPowerNetInfo.init_net_components.other = []
        this.componentOtherColumns = []
      }
      // console.log(this.initPowerNetInfo.init_net_components.other_select)
      // console.log(this.initPowerNetInfo.init_net_components.other)
      // console.log(this.componentOtherColumns)
    },
    // 一键生成
    addPowerNetDataset () {
      // 验证表单数据正确
      const valid1 = this.$refs.powerNetJobInfoFormRef.validate
      const valid2 = this.$refs.initPowerNetInfoFormRef.validate
      const valid3 = this.$refs.disturbSettingsFormRef.validate
      if (valid1 && valid2 && valid3) {
        this.addPowerNetDatasetForm = {
          pn_job_name: this.powerNetJobInfo.pn_job_name,
          pn_job_type: this.powerNetJobInfo.pn_job_type,
          pn_job_description: this.powerNetJobInfo.pn_job_description,
          init_net_name: this.initPowerNetInfo.init_net_name,
          disturb_src_type_list: this.disturbSettings.disturb_src_type_list,
          disturb_n_var: this.disturbSettings.disturb_n_var,
          disturb_radio: this.disturbSettings.disturb_radio,
          disturb_n_sample: this.disturbSettings.disturb_n_sample
        }
      }
      queryPowerNetApi.addPowerNetDataset(this.addPowerNetDatasetForm).then(response => {
        const resp = response.data
        console.log(response)
        if (resp.meta.code === 204) {
          this.$message.success('添加电网数据生成任务成功')
        } else {
          this.$message.error('添加电网数据生成任务失败')
        }
      })
    },
    formatValues (row, column, cellValue) {
      if (cellValue === null) {
        return 'null'
      }
      if (cellValue === true) {
        return 'true'
      }
      if (cellValue === false) {
        return 'false'
      }
      return cellValue
    },
    // 返回上一页
    backPage () {
      this.$router.back()
    }
  }
}
</script>
<style scoped>
  .el-card{
    margin: 10px 20px;
  }
  h2{
     text-align: center;
  }
  h3{
    padding-bottom: 10px;
    /* border-bottom: 3px solid rgb(102, 102, 102) */
    border-bottom: 3px solid rgb(180, 180, 180);
  }
  h4{
    padding-bottom: 10px;
    /* border-bottom: 2px solid rgb(102, 102, 102) */
  }
  .backbtn{
    margin-top: 20px;
    /* margin-bottom: 10px; */
    margin-left:20px;
  }
  .createbtn{
    /* float: right; */
    /* margin-top: 20px; */
    margin-bottom: 10px;
    margin-left:400px;
  }
  .el-col{
    min-height: 1px;
  }
  .el-form-item{
  margin-bottom: 30px;
  }
</style>
