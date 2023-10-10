import pandapower as pp
import pandapower.networks as pn
import numpy as np
import copy
import torch
import gym
from utils import load_variable, ROOT_PATH
import pandapower.topology as pt
import dgl
import pandas
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


class TransmissionSectionEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, args, evaluation=False):
        # 电网环境名
        if args.env_id == 'S4case118' or args.env_id == 'S10case118':
            self.original_net = pn.case118()           # 初始电网样本
        elif args.env_id == 'S4case300' or args.env_id == 'S10case300':
            self.original_net = pp.from_json('case300cn.json')
        elif args.env_id == 'S10case9241' or args.env_id == 'S4case9241':
            self.original_net = pn.case9241pegase()
        else:
            assert False, 'env_id not exist'
        nxgraph = pt.create_nxgraph(self.original_net)
        self.graph = dgl.from_networkx(nxgraph)
        self.n_bus = self.original_net.bus.shape[0]  # 电网母线个数
        self.n_gen = self.original_net.gen.shape[0]  # 电网发电机个数

        self.current_power_section = None
        self.current_section = None
        self.evaluation = evaluation
        self.env_id = args.env_id

        if self.env_id == 'S10case9241' or self.env_id == 'S4case9241':
            self.n_line = 29  # 1w节点的输电线onehot只关注用上的输电线
        else:
            self.n_line = len(self.original_net.line)  # 电网输电线数量

        if not os.path.exists(os.path.join(ROOT_PATH, args.env_id, 'multi_train_control_nets.pt')):
            assert False, 'No Available Data!'

        if not self.evaluation:
            self.control_nets = load_variable(os.path.join(ROOT_PATH, args.env_id, 'multi_train_control_nets.pt'))
        else:
            self.control_nets = load_variable(os.path.join(ROOT_PATH, args.env_id, 'multi_test_control_nets.pt'))

        # 对发电机cost按序号排序，平衡机cost
        cost = self.original_net.poly_cost
        cost['element'] = pandas.to_numeric(cost['element'], downcast='integer')
        cost.set_index(['element'], inplace=True)
        cost.sort_index(inplace=True)
        self.gen_cost = cost.loc[cost['et'] == 'gen']
        self.ext_grid_cost = cost.loc[cost['et'] == 'ext_grid']

        self.n_net = len(self.control_nets['control_nets_power_section'])

        self.total_section_lines = []
        cur_section = None
        for i in range(self.n_net):
            section = self.control_nets['control_nets_section'][i]
            if section != cur_section:
                self.total_section_lines.append(section)
                cur_section = section

        # 1w节点，只统计用上的输电线onehot
        if self.env_id == 'S10case9241' or self.env_id == 'S4case9241':
            self.section_set = np.concatenate(self.total_section_lines).tolist()

        self.n_adjust_step = 2  # 调整步长
        self.adjust_ratio = np.linspace(0.8, 1.2, num=self.n_adjust_step)  # 调整率

        self.action_space = gym.spaces.Discrete(n=self.n_gen * self.n_adjust_step)
        # 创建动作空间，大小为调整步长*发电机个数
        self.observation_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(self.n_bus * 4+self.n_line,), dtype=np.float32)

        self.current_step = 0
        self.current_idx = -1
        self.current_net_undo = None
        self.current_net = None
        self.converged = None
        self.success = None
        self.trafos = None
        self.power_target = None
        self.info = None

    def _get_cost(self):
        gen_power_cost = sum(self.gen_cost['cp2_eur_per_mw2'] * (self.current_net.gen['p_mw']) ** 2 +
                             self.gen_cost['cp1_eur_per_mw'] * (self.current_net.gen['p_mw']))
        total_power_cost = int(gen_power_cost +
                               sum(self.ext_grid_cost['cp2_eur_per_mw2'] * (self.current_net.res_ext_grid['p_mw']) ** 2 +
                               self.ext_grid_cost['cp1_eur_per_mw'] * self.current_net.res_ext_grid['p_mw']))
        return -total_power_cost

    def _current_section_onehot(self):
        if self.env_id == 'S10case9241' or self.env_id == 'S4case9241':
            section_onehot = torch.zeros(self.n_line, dtype=torch.float32)
            for loc in self.current_section:
                section_onehot[self.section_set.index(loc)] = 1
        else:
            section_onehot = torch.zeros(self.n_line, dtype=torch.float32)
            for loc in self.current_section:
                section_onehot[loc] = 1

        return section_onehot

    def reset(self):
        self.current_step = 0
        if self.evaluation:
            self.current_idx += 1
            if self.current_idx == self.n_net:
                self.current_idx = 0
        else:
            self.current_idx = np.random.randint(0, self.n_net)  # 随机从电网样本中采样电网编号
        self.current_net = self._load_net(self.current_idx)  # 初始化电网PQ值
        self.current_net_undo = copy.deepcopy(self.current_net)  # 保存电网副本
        self.current_power_section = copy.deepcopy(self.control_nets['control_nets_power_section'][self.current_idx])
        self.current_section = copy.deepcopy(self.control_nets['control_nets_section'][self.current_idx])
        self.trafos = copy.deepcopy(self.control_nets['control_nets_trafos'][self.current_idx])
        target = copy.deepcopy(self.control_nets['control_nets_target'][self.current_idx])
        self.power_target = [int(target*0.2), int(target*1.4)]
        return self._get_state()    # 对current_net进行潮流计算

    def set(self, idx):
        if idx >= self.n_net:
            return None
        self.current_step = 0
        self.current_idx = idx
        self.current_net = self._load_net(self.current_idx)  # 初始化电网PQ值
        self.current_net_undo = copy.deepcopy(self.current_net)  # 保存电网副本
        self.current_power_section = copy.deepcopy(self.control_nets['control_nets_power_section'][self.current_idx])
        self.current_section = copy.deepcopy(self.control_nets['control_nets_section'][self.current_idx])
        self.trafos = copy.deepcopy(self.control_nets['control_nets_trafos'][self.current_idx])
        target = copy.deepcopy(self.control_nets['control_nets_target'][self.current_idx])
        self.power_target = [int(target*0.2), int(target*1.4)]
        return self._get_state()    # 对current_net进行潮流计算

    def _load_net(self, idx):
        net = copy.deepcopy(self.original_net)
        net.load['p_mw'] = copy.deepcopy(self.control_nets['control_nets_load_p'][idx])
        net.load['q_mvar'] = copy.deepcopy(self.control_nets['control_nets_load_q'][idx])
        net.gen['p_mw'] = copy.deepcopy(self.control_nets['control_nets_gen_p'][idx])
        return net

    def _get_state(self):
        try:
            pp.runpp(self.current_net)
            self.converged = True
        except Exception as e:
            assert isinstance(e, pp.powerflow.LoadflowNotConverged), 'Not Converged Error'
            self.converged = False
            self.current_net = self.current_net_undo
            pp.runpp(self.current_net)

        result = copy.deepcopy(self.current_net.res_bus)
        result['va_degree'] = (result['va_degree'] - np.mean(result['va_degree'])) / np.std(result['va_degree'])
        result['p_mw'] = (result['p_mw'] - np.mean(result['p_mw'])) / np.std(result['p_mw'])
        result['q_mvar'] = (result['q_mvar'] - np.mean(result['q_mvar'])) / np.std(result['q_mvar'])
        result['vm_pu'] = result['vm_pu'] - np.mean(result['vm_pu'])
        x = torch.tensor(np.array(result), dtype=torch.float32).reshape(-1)  # result_bus
        state = torch.cat((x, self._current_section_onehot()), dim=-1)
        return state

    def step(self, action):
        self.current_step += 1
        if action == -1:  # for debug
            pass
        else:
            self.current_net_undo = copy.deepcopy(self.current_net)
            action_gen_idx = np.floor(action / self.n_adjust_step)
            action_ratio_idx = action % self.n_adjust_step
            self.current_net.gen['p_mw'][action_gen_idx] *= self.adjust_ratio[action_ratio_idx]
        state = self._get_state()

        self.current_power_section = self._get_power_section()
        reward, done = self._get_reward_done()
        self.info = {'task_embedding': self._current_section_onehot(), 'is_converged': self.converged,
                     'is_success': self.success, 'cost': self._get_cost()}
        return state, reward, done, self.info

    def _get_reward_done(self):
        gen_cost = self._get_cost()
        self.success = None
        done = False
        if self.converged:
            if self.power_target[0] < self.current_power_section < self.power_target[1]:
                reward = 100
                done = True
                self.success = True
            else:
                reward = -1 * abs(self.current_power_section -
                                  (self.power_target[1] + self.power_target[0]) / 2.0) / 500.0
        else:
            reward = -100
            done = True
            self.success = False

        if self.current_step > 50:
            done = True
            self.success = False

        reward += 5e-6*gen_cost

        return reward, done

    def _get_power_section(self):
        power_section = np.sum(np.abs(self.current_net.res_line.loc[self.current_section, 'p_from_mw']))
        if self.trafos != -1:
            power_section += np.sum(np.abs(self.current_net.res_trafo.loc[[self.trafos], 'p_hv_mw']))
        return power_section
