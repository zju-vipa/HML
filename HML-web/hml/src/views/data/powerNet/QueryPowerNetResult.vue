<template>
  <div>
    <!-- 标题 -->
    <div>
      <el-col :span="2">
        <el-button class="backbtn" size="mini" type="info" plain @click="backPage" icon="el-icon-arrow-left">返回</el-button>
      </el-col>
      <el-col :span="22">
        <h2>电网数据生成任务结果</h2>
      </el-col>
    </div>
    <div>
      <el-card>
        <!-- 任务信息 -->
        <div><h3>任务信息</h3></div>
        <el-form label-position="right" label-width="150px" :model="powerNetJobInfo">
          <el-row>
            <el-col :span="10">
              <el-form-item label="任务名称" prop="pn_job_name">
                <el-input disabled  v-model="powerNetJobInfo.pn_job_name" style="width: 300px"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item label="生成方式" prop="pn_job_type">
                <el-select disabled v-model="powerNetJobInfo.pn_job_type" style="width: 300px">
                  <el-option v-for="(option, index) in generateTypeOptions" :key="index" :label="option.name" :value="option.type"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
              <el-col :span="20">
              <el-form-item label="任务描述" prop="pn_job_description">
                <el-input disabled  v-model="powerNetJobInfo.pn_job_description" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
      <el-card>
          <!-- 初始电网信息 -->
        <div><h3>初始电网信息</h3></div>
        <el-form label-position="right" label-width="150px" :model="initPowerNetInfo">
          <el-row>
            <el-col :span="10">
              <el-form-item label="样例名称" prop="init_net_name">
                <el-select disabled v-model="initPowerNetInfo.init_net_name" style="width: 300px">
                  <el-option v-for="(option, index) in initNetOptions" :key="index" :label="option.name" :value="option.type"></el-option>
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
        <div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card style="height: 400px">
              <div><h4>母线</h4></div>
              <el-table :data="initPowerNetInfo.init_net_components.bus" border stripe
                height="300" style="width:100%">
                <el-table-column width="120" v-for="(item,index) in componentColumns.bus"
                  :key="index" :prop="item" :label="item" :formatter="formatValues"></el-table-column>
              </el-table>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card style="height: 400px">
              <div><h4>负荷</h4></div>
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
              <div><h4>电机</h4></div>
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
      <el-card v-if="powerNetJobInfo.pn_job_type==='A'">
        <div><h3>扰动参数信息</h3></div>
        <el-form label-position="right" label-width="150px" :model="disturbSettings" :rules="disturbSettingsFormRules" ref="disturbSettingsFormRef" class="demo-ruleForm">
          <el-row>
            <el-col :span="24">
              <el-form-item label="扰动源类型" prop="disturb_src_type_list">
                <el-input disabled v-model.number="disturbSettings.disturb_src_type_list" style="width: 800px"></el-input>
                <!-- <el-checkbox-group disabled v-model="disturbSettings.disturb_src_type_list">
                  <el-checkbox label="gen_p">电机P</el-checkbox>
                  <el-checkbox label="gen_v">电机V</el-checkbox>
                  <el-checkbox label="load_p">负荷P</el-checkbox>
                  <el-checkbox label="load_q">负荷Q</el-checkbox>
                </el-checkbox-group> -->
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="20">
              <el-form-item label="扰动源个数" prop="disturb_n_var">
                <el-input disabled v-model.number="disturbSettings.disturb_n_var" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="20">
              <el-form-item label="扰动范围" prop="disturb_radio">
                <el-input disabled v-model.number="disturbSettings.disturb_radio" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="20">
              <el-form-item label="扰动次数" prop="disturb_n_sample">
                <el-input disabled v-model.number="disturbSettings.disturb_n_sample" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
      <!-- 方式C（CTGAN）：生成参数设置 -->
      <el-card v-if="powerNetJobInfo.pn_job_type==='C' && ganSettings.set_human_origin===true">
        <div><h3>Step 3: 生成参数设置</h3></div>
        <el-form label-position="right" label-width="150px" :model="ganSettings" :rules="ganSettingsFormRules" ref="ganSettingsFormRef" class="demo-ruleForm">
          <el-row align="middle" style="margin-bottom: 30px">
            <el-col align="center">
              <img :src="ganSettings.loss_img">
              <!-- <span style="margin-top: 5px;">图</span> -->
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="生成样本数量" prop="n_sample">
                <el-input v-model.number="ganSettings.n_sample" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="稳定性条件控制" prop="cond_stability">
                <el-radio-group v-model="ganSettings.cond_stability" >
                  <el-radio v-for="(option, index) in ganStabilityOptions"
                  :key="index" :label="option.type">{{option.name}}
                  </el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="负荷条件控制" prop="cond_load">
                <el-radio-group v-model="ganSettings.cond_load" >
                  <el-radio v-for="(option, index) in ganLoadOptions"
                  :key="index" :label="option.type">{{option.name}}
                  </el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="人在回路调参" prop="set_human">
                <el-select v-model="ganSettings.set_human" placeholder="请选择是否设置人在回路调参" style="width:400px">
                  <el-option label="是" :value=true></el-option>
                  <el-option label="否" :value=false></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <el-button v-if="powerNetJobInfo.pn_job_type==='C' && ganSettings.set_human_origin===true" class="createbtn" size="medium" type="primary" @click="addHumanSetPowerNetDataset">重新生成</el-button>
      </el-card>
      <el-card v-if="powerNetJobInfo.pn_job_type==='A'">
        <h3>潮流计算结果（至多显示30条）</h3>
        <el-table :data="powerFlowResultData" border stripe  style="width: 100%">
          <el-table-column  label="序号" type="index"> </el-table-column>
          <el-table-column prop="sample_name" label="扰动位置"> </el-table-column>
          <el-table-column prop="sample_before" label="扰动前"> </el-table-column>
          <el-table-column prop="sample_after" label="扰动后"> </el-table-column>
          <el-table-column prop="success" label="收敛情况"></el-table-column>
        </el-table>
        <el-button type="primary" class="downloadbtn" icon="el-icon-download" @click="handleDownloadResult">下载潮流计算结果</el-button>
      </el-card>
      <el-card v-if="powerNetJobInfo.pn_job_type==='B'">
        <h3>暂稳计算结果（至多显示30条）</h3>
        <el-table :data="powerFlowResultData" border stripe  style="width: 100%">
          <el-table-column  label="序号" type="index"> </el-table-column>
          <el-table-column prop="success" label="暂稳情况"></el-table-column>
        </el-table>
        <el-button type="primary" class="downloadbtn" icon="el-icon-download" @click="handleDownloadResult">下载暂稳结果</el-button>
      </el-card>
      <el-card v-if="powerNetJobInfo.pn_job_type==='C'">
        <h3>CTGAN生成数据</h3>
        <!-- <el-table :data="powerFlowResultData" border stripe  style="width: 100%">
          <el-table-column  label="序号" type="index"> </el-table-column>
        </el-table> -->
        <el-button type="primary" class="downloadbtn" icon="el-icon-download" @click="handleDownloadResult">下载电网数据集</el-button>
      </el-card>
      <el-card v-if="powerNetJobInfo.pn_job_type==='D'">
        <h3>数据无偏化样本生成结果</h3>
        <!-- <el-table :data="powerFlowResultData" border stripe  style="width: 100%">
          <el-table-column  label="序号" type="index"> </el-table-column>
        </el-table> -->
        <el-button type="primary" class="downloadbtn" icon="el-icon-download" @click="downloadZIP">下载结果文件</el-button>
      </el-card>
    </div>
  </div>
</template>
<script>
import queryPowerNetApi from './../../../api/queryPowerNet'
// 生成方式类型
const generateTypeOptions = [
  { type: 'A', name: '潮流数据生成' }, // 潮流
  { type: 'B', name: '暂稳数据生成' }, // 暂稳
  { type: 'C', name: 'CTGAN模型生成' },
  { type: 'D', name: '数据无偏化样本生成' } // 清华 场景驱动的数据无偏化技术
]
// CTGAN生成条件：无；稳定；不稳定
const ganStabilityOptions = [
  { type: 0, name: '不设置' },
  { type: 1, name: '暂态稳定' },
  { type: 2, name: '暂态失稳' }
]
const ganLoadOptions = [
  { type: '0', name: '不设置' },
  { type: '0.7', name: '70%' },
  { type: '0.75', name: '75%' },
  { type: '0.8', name: '80%' },
  { type: '0.85', name: '85%' },
  { type: '0.9', name: '90%' },
  { type: '0.95', name: '95%' },
  { type: '1.0', name: '100%' },
  { type: '1.05', name: '105%' },
  { type: '1.1', name: '110%' },
  { type: '1.15', name: '115%' },
  { type: '1.2', name: '120%' },
  { type: '1.25', name: '125%' },
  { type: '1.3', name: '130%' }
]
// 样例名称
const initNetOptions = ['case5', 'case9', 'case14', 'case30', 'case_ieee30', 'case39', 'case57', 'case118', 'case300']
// 其他组件内容选择
const otherSelectOptions = ['line', 'shunt', 'switch', 'impedance', 'trafo']
const componentColumns = {
  bus: ['name', 'vn_kv', 'type', 'zone', 'max_vm_pu', 'min_vm_pu', 'in_service'],
  load: [// 'name',
    'bus', 'p_mw', 'q_mvar', 'const_z_percent', 'const_i_percent', 'sn_mva', 'scaling',
    'in_service',
    // 'type',
    'controllable'
    // 'max_p_mw', 'min_p_mw', 'max_q_mvar', 'min_q_mvar'
  ],
  gen: [// 'name', 'type',
    'bus', 'p_mw', 'vm_pu',
    // 'sn_mva',
    'min_q_mvar', 'max_q_mvar',
    'scaling', 'max_p_mw', 'min_p_mw',
    // 'vn_kv', 'xdss_pu', 'rdss_pu', 'cos_phi',
    'in_service'],
  line: [// 'name', 'std_type',
    'from_bus', 'to_bus', 'length_km', 'r_ohm_per_km', 'x_ohm_per_km', 'c_nf_per_km',
    // 'r0_ohm_per_km', 'x0_ohm_per_km', 'c0_nf_per_km',
    'g_us_per_km', 'max_i_ka', 'parallel', 'df', 'type',
    'max_loading_percent',
    // 'endtemp_degree',
    'in_service'],
  shunt: [// 'name',
    'bus', 'p_mw', 'q_mvar', 'vn_kv', 'step', 'in_service'],
  switch: ['name', 'bus', 'element', 'et', 'type', 'closed'],
  impedance: ['name', 'from_bus', 'to_bus', 'rft_pu', 'xft_pu', 'rtf_pu', 'xtf_pu', 'sn_mva', 'in_service'],
  trafo: [// 'name', 'std_type',
    'hv_bus', 'lv_bus', 'sn_mva', 'vn_hv_kv', 'vn_lv_kv', 'vk_percent',
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
    //   // 电网数据生成任务列表
    //   powerNetData: [],
    //   // 全部任务数，已完成任务数，未完成任务数 (异步)
    //   powerNetJobCnt: 0,
    //   powerNetJobDoneCnt: 0,
    //   powerNetJobUndoneCnt: 0
      // 任务ID，名称，生成方式，描述
      addHumanSetPowerNetDatasetForm: {},
      ganSettingsFormRules: {
        n_sample: [
          { required: true, message: '请填写样本数', trigger: 'blur' }
        ],
        cond_stability: [
          { required: true, message: '请选择稳定条件', trigger: 'blur' }
        ],
        cond_load: [
          { required: true, message: '请选择负荷条件', trigger: 'blur' }
        ],
        set_human: [
          { required: true, message: '请选择是否设置人在回路调参', trigger: 'blur' }
        ]
      },
      powerNetJobInfo: {
        pn_job_id: '',
        pn_job_name: '',
        pn_job_type: 'A',
        pn_job_description: '略',
        pn_job_generate_state: '0'
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
      // 调整参数
      // 扰动源类型，扰动源个数，扰动范围，扰动次数
      disturbSettings: {
        disturb_src_type_list: ['gen_p'],
        disturb_n_var: 1,
        disturb_radio: 1,
        disturb_n_sample: 1
      },
      faultSettings: {
        load_list: '0.8, 1.0, 1.2',
        fault_line_list: [1, 2, 3, 4],
        line_percentage_list: ['0.1', '0.2'],
        fault_time_list: '1, 2, 4, 8'
      },
      ganSettings: {
        n_sample: 10,
        cond_stability: 1,
        cond_load: '0',
        set_human_origin: false,
        set_human: false,
        loss_img: ''
      },
      unbiasedSettings: {
        sample_num: 10,
        fault_line: 12
      },
      // to do
      // 潮流计算结果
      powerFlowResultData: [],
      generateTypeOptions,
      ganStabilityOptions,
      ganLoadOptions,
      initNetOptions,
      otherSelectOptions,
      componentColumns,
      componentOtherColumns: []
    }
  },
  created () {
    this.getPowerNetJobInfo(this.$route.query.jobId)
  },
  methods: {
    // 根据id获取电网数据生成任务信息
    getPowerNetJobInfo (jobId) {
      queryPowerNetApi.queryJob(jobId).then(response => {
        console.log(response)
        const resp = response.data
        if (resp.meta.code === 200) {
          this.$message.success('加载任务信息成功')
          // 任务信息
          this.powerNetJobInfo = {
            pn_job_id: jobId,
            pn_job_name: resp.data.powerNetDataset.power_net_dataset_name,
            pn_job_type: resp.data.powerNetDataset.power_net_dataset_type,
            pn_job_description: resp.data.powerNetDataset.power_net_dataset_description,
            pn_job_generate_state: resp.data.powerNetDataset.generate_state
          }
          // 潮流计算结果
          this.powerFlowResultData = resp.data.resultData
          // 参数设置 方式A
          this.disturbSettings.disturb_src_type_list = resp.data.powerNetDataset.disturb_src_type_list.split(',')
          this.disturbSettings.disturb_n_var = resp.data.powerNetDataset.disturb_n_var
          this.disturbSettings.disturb_radio = resp.data.powerNetDataset.disturb_radio
          this.disturbSettings.disturb_n_sample = resp.data.powerNetDataset.disturb_n_sample
          // 方式B 参数设置
          // 方式C ctgan 参数设置
          this.ganSettings.n_sample = resp.data.powerNetDataset.n_sample
          this.ganSettings.cond_stability = resp.data.powerNetDataset.cond_stability
          this.ganSettings.cond_load = resp.data.powerNetDataset.cond_load
          // set_human_origin 是原任务的是否人在回路（决定了是否有这个功能），set_human 是调参的新任务是否继续人在回路调参
          this.ganSettings.set_human_origin = resp.data.powerNetDataset.set_human
          this.ganSettings.set_human = resp.data.powerNetDataset.set_human
          if (this.ganSettings.set_human_origin === true) {
            this.ganSettings.loss_img = 'data:image/jpeg;base64,' + resp.data.loss_img
          }
          // 样例信息
          this.initPowerNetInfo.init_net_name = resp.data.powerNetDataset.init_net_name
          this.getInitNetInfo(this.initPowerNetInfo.init_net_name)
        }
        console.log(this.ganSettings)
      })
    },
    // 根据样例名称获得样例描述、组件数统计、组件内容、网络拓扑图
    getInitNetInfo (name) {
      queryPowerNetApi.queryNetDescription(name).then(response => {
        console.log(response)
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
            line: resp.data.component.line,
            other_select: 'line',
            other: resp.data.component.line,
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
    handleDownloadResult () {
      if (this.powerNetJobInfo.pn_job_generate_state === '2') {
        queryPowerNetApi.downloadResult(this.powerNetJobInfo.pn_job_id).then(response => {
          console.log(response)
          const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }))
          const link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          link.setAttribute('download', this.powerNetJobInfo.pn_job_id + 'powerNet' + '.csv')
          document.body.appendChild(link)
          link.click()
        })
      } else {
        return this.$message.error('未完成，不能下载')
      }
    },
    // 下载结果文件压缩包
    downloadZIP () {
      if (this.powerNetJobInfo.pn_job_generate_state === '2') {
        const loading = this.$loading({
          lock: true,
          text: '文件打包传输中......',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        })
        queryPowerNetApi.downloadZIP(this.powerNetJobInfo.pn_job_id).then(response => {
          const resp = response.data
          loading.close()
          if (resp.code) {
            this.$message.info(resp.extra_message)
          } else {
            const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/zip' }))
            const link = document.createElement('a')
            link.style.display = 'none'
            link.href = url
            link.setAttribute('download', `all_result_${this.$route.params.id}.zip`)
            document.body.appendChild(link)
            link.click()
          }
        })
      } else {
        return this.$message.error('未完成，不能下载')
      }
    },
    // 一键生成
    addHumanSetPowerNetDataset () {
      // 验证表单数据正确
      var valid = false
      if (this.powerNetJobInfo.pn_job_type === 'C') {
        valid = this.$refs.ganSettingsFormRef.validate
      }
      // 转换成query需要的格式
      if (valid) {
        this.addHumanSetPowerNetDatasetForm = {
          pn_job_name: `${this.powerNetJobInfo.pn_job_name}_hml`,
          pn_job_type: this.powerNetJobInfo.pn_job_type,
          pn_job_description: this.powerNetJobInfo.pn_job_description,
          init_net_name: this.initPowerNetInfo.init_net_name,
          disturb_src_type_list: this.disturbSettings.disturb_src_type_list,
          disturb_n_var: this.disturbSettings.disturb_n_var,
          disturb_radio: this.disturbSettings.disturb_radio,
          disturb_n_sample: this.disturbSettings.disturb_n_sample,
          load_list: this.faultSettings.load_list.split(','),
          fault_line_list: this.faultSettings.fault_line_list,
          line_percentage_list: this.faultSettings.line_percentage_list,
          fault_time_list: this.faultSettings.fault_time_list.split(','),
          n_sample: this.ganSettings.n_sample,
          // cond_stability: this.ganSettings.cond_stability.toString,
          cond_stability: this.ganSettings.cond_stability,
          cond_load: this.ganSettings.cond_load,
          set_human: this.ganSettings.set_human,
          sample_num: this.unbiasedSettings.sample_num,
          fault_line: this.unbiasedSettings.fault_line
        }
      }
      console.log(this.addHumanSetPowerNetDatasetForm)
      queryPowerNetApi.addPowerNetDataset(this.addHumanSetPowerNetDatasetForm).then(response => {
        const resp = response.data
        console.log(response)
        if (resp.meta.code === 204) {
          this.$message.success('添加电网数据生成任务成功')
          this.$router.back()
        } else {
          this.$message.error('添加电网数据生成任务失败')
        }
      })
      // this.$router.back()
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
  .downloadbtn{
    float: right;
    margin-top: 20px;
    margin-bottom: 20px;
  }
  .el-col{
    min-height: 1px;
  }
  .el-form-item{
  margin-bottom: 30px;
  }
</style>
