<template>

  <div>
    <!-- <div class="block">
    <span class="demonstration">默认</span>
    <el-slider v-model="value1"></el-slider>
    </div> -->
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
                <!--潮流数据 样例列表-->
                <el-select v-if="powerNetJobInfo.pn_job_type==='A'" v-model="initPowerNetInfo.init_net_name" @change="handleInitNetChange" style="width: 300px">
                  <el-option v-for="(option, index) in initNetOptionsA" :key="index" :label="option" :value="option"></el-option>
                </el-select>
                <!--暂稳数据 样例列表-->
                <el-select v-else-if="powerNetJobInfo.pn_job_type==='B' || powerNetJobInfo.pn_job_type==='C' || powerNetJobInfo.pn_job_type==='D'" v-model="initPowerNetInfo.init_net_name" @change="handleInitNetChange" style="width: 300px">
                  <el-option v-for="(option, index) in initNetOptionsB" :key="index" :label="option" :value="option"></el-option>
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
      <!-- 方式A（潮流数据）：扰动参数设置 -->
      <el-card v-if="powerNetJobInfo.pn_job_type==='A'">
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
      <!-- 方式B（暂稳数据）：暂稳参数设置 -->
      <el-card v-if="powerNetJobInfo.pn_job_type==='B'">
        <div><h3>Step 3: 故障参数设置</h3></div>
        <el-form label-position="right" label-width="150px" :model="faultSettings" :rules="faultSettingsFormRules" ref="faultSettingsFormRef" class="demo-ruleForm">
          <el-row>
            <el-col :span="24">
              <el-form-item label="负荷范围" prop="load_list">
                <el-input v-model="faultSettings.load_list" placeholder="例如：0.8, 1.0, 1.2"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="故障线路" prop="fault_line_list">
                <el-checkbox-group v-model="faultSettings.fault_line_list">
                  <el-checkbox v-for="count in 34" :key="count" :label="count">line{{count}}</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="线路故障位置" prop="line_percentage_list">
                <el-checkbox-group v-model="faultSettings.line_percentage_list">
                  <el-checkbox v-for="(option, index) in linePercentageOptions"
                  :key="index" :label="option" :value="option"></el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="故障持续时间（周期数）" prop="fault_time_list">
                <el-input v-model="faultSettings.fault_time_list" placeholder="例如：1, 2, 4, 8"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <el-button class="createbtn" size="medium" type="primary" @click="addPowerNetDataset">一键生成</el-button>
      </el-card>
      <!-- 方式C（CTGAN）：生成参数设置 -->
      <el-card v-if="powerNetJobInfo.pn_job_type==='C'">
        <div><h3>Step 3: 生成参数设置</h3></div>
        <el-form label-position="right" label-width="150px" :model="ganSettings" :rules="ganSettingsFormRules" ref="ganSettingsFormRef" class="demo-ruleForm">
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
        <el-button class="createbtn" size="medium" type="primary" @click="addPowerNetDataset">一键生成</el-button>
      </el-card>
      <!-- 方式D （清华 数据无偏化样本生成）：生成参数设置 -->
      <el-card v-if="powerNetJobInfo.pn_job_type==='D'">
        <div><h3>Step 3: 生成参数设置</h3></div>
        <el-form label-position="right" label-width="150px" :model="unbiasedSettings" :rules="unbiasedSettingsFormRules" ref="unbiasedSettingsFormRef" class="demo-ruleForm">
          <el-row>
            <el-col :span="24">
              <el-form-item label="生成样本数量" prop="sample_num">
                <el-input v-model.number="unbiasedSettings.sample_num" style="width: 800px"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="故障线路选择" prop="fault_line">
                <el-radio-group v-if="initPowerNetInfo.init_net_name=='case39'" v-model="unbiasedSettings.fault_line" >
                  <el-radio v-for="(option, index) in unbiasedFaultLineOptions"
                  :key="index" :label="option.type">{{option.name}}
                  </el-radio>
                </el-radio-group>
                <el-radio-group v-else-if="initPowerNetInfo.init_net_name=='case300'" v-model="unbiasedSettings.fault_line" >
                  <el-radio v-for="(option, index) in unbiasedFaultLineOptions300"
                  :key="index" :label="option.type">{{option.name}}
                  </el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="生成算法选择" prop="generate_algorithm">
                <el-radio-group v-model="unbiasedSettings.generate_algorithm" >
                  <el-radio v-for="(option, index) in unbiasedAlgorithmOptions"
                  :key="index" :label="option.type">{{option.name}}
                  </el-radio>
                </el-radio-group>
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
// 清华 数据无偏化样本生成，fault_line目前只支持12,26
const unbiasedFaultLineOptions = [
  { type: 12, name: '线路12' },
  { type: 26, name: '线路26' }
]
const unbiasedFaultLineOptions300 = [
  { type: 3, name: '线路3' },
  { type: 33, name: '线路33' },
  { type: 49, name: '线路3' },
  { type: 50, name: '线路33' },
  { type: 116, name: '线路116' },
  { type: 171, name: '线路171' }
]
const unbiasedAlgorithmOptions = [
  { type: 1, name: '蒙特卡洛生成' },
  { type: 2, name: '数据无偏化生成' }
]
// 方式A样例名称 （潮流）
const initNetOptionsA = ['case5', 'case9', 'case14', 'case30', 'case_ieee30', 'case39', 'case57', 'case118', 'case300']
// 方式B/c样例名称  （暂稳）
const initNetOptionsB = ['case39', 'case300']
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
const linePercentageOptions = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']
export default {
  filters: {
    // is_done转换成 “已完成” “未完成”
    // applyJobStatusTrans (type) {
    //   return type ? '已完成' : '未完成'
    // }
  },
  data () {
    return {
      value1: 0,
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
      faultSettingsFormRules: {
        load_list: [
          { required: true, message: '请填写负荷范围', trigger: 'blur' }
        ],
        fault_line_list: [
          { required: true, message: '请选择故障线路', trigger: 'blur' }
        ],
        line_percentage_list: [
          { required: true, message: '请选择故障位置', trigger: 'blur' }
        ],
        fault_time_list: [
          { required: true, message: '请填写故障持续时间', trigger: 'blur' }
        ]
      },
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
      unbiasedSettingsFormRules: {
        sample_num: [
          { required: true, message: '请填写样本数', trigger: 'blur' }
        ],
        fault_line: [
          { required: true, message: '请选择故障线路', trigger: 'blur' }
        ],
        generate_algorithm: [
          { required: true, message: '请选择生成算法', trigger: 'blur' }
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
        init_net_name: 'case39',
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
      faultSettings: {
        load_list: '0.8, 1.0, 1.2',
        fault_line_list: [1, 2, 3, 4],
        line_percentage_list: ['0.1', '0.2'],
        fault_time_list: '1, 2, 4, 8'
      },
      ganSettings: {
        n_sample: 10,
        // stability_switch: false,
        cond_stability: 1,
        // load_switch: false,
        cond_load: '0',
        set_human: false
      },
      unbiasedSettings: {
        sample_num: 10,
        fault_line: 12,
        generate_algorithm: 1
      },
      // to do
      // 潮流计算结果
      powerFlowResultData: [],
      generateTypeOptions,
      initNetOptionsA,
      initNetOptionsB,
      otherSelectOptions,
      componentColumns,
      componentOtherColumns: [],
      linePercentageOptions,
      ganStabilityOptions,
      ganLoadOptions,
      unbiasedFaultLineOptions,
      unbiasedFaultLineOptions300,
      unbiasedAlgorithmOptions
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
      var valid3 = false
      if (this.powerNetJobInfo.pn_job_type === 'A') {
        valid3 = this.$refs.disturbSettingsFormRef.validate
      } else if (this.powerNetJobInfo.pn_job_type === 'B') {
        valid3 = this.$refs.faultSettingsFormRef.validate
      } else if (this.powerNetJobInfo.pn_job_type === 'C') {
        valid3 = this.$refs.ganSettingsFormRef.validate
      } else if (this.powerNetJobInfo.pn_job_type === 'D') {
        valid3 = this.$refs.unbiasedSettingsFormRef.validate
      }
      // 转换成query需要的格式
      if (valid1 && valid2 && valid3) {
        this.addPowerNetDatasetForm = {
          pn_job_name: this.powerNetJobInfo.pn_job_name,
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
          fault_line: this.unbiasedSettings.fault_line,
          generate_algorithm: this.unbiasedSettings.generate_algorithm
        }
      }
      queryPowerNetApi.addPowerNetDataset(this.addPowerNetDatasetForm).then(response => {
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
    // 方式C：是否设置生成条件
    // stabilityConditionSwitch () {
    //   if (this.ganSettings.stability_switch === false) {
    //     this.ganSettings.cond_stability = 0
    //   }
    // },
    // loadConditionSwitch () {
    //   if (this.ganSettings.load_switch === false) {
    //     this.ganSettings.cond_load = '0'
    //   }
    // },
    formatToolTip1 (val) {
      return val
    },
    condControl1 () {
      console.log(this.ganSettings.cond_stability)
      console.log(this.ganSettings.cond_load)
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
