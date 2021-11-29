import pandapower as pp
import pandapower.networks as pn
import numpy as np
import copy
import torch
import gym
from env.utils import load_variable
from env.generator import generate
from env import ROOT_PATH
import os


class TransmissionSectionEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, args, train=True):
        # 电网环境名
        if args.env_id == 'case118':
            self.original_net = pn.case118()           # 初始电网样本
            self.section_lines = [104, 105, 106, 109]  # 输电断面中的输电线下标
            self.section_trafos = [9]                  # 输电断面中的变压器下标
            self.power_target = [500, 1000]            # 目标功率区间
        else:
            assert False, 'env_id not exist'

        self.n_bus = self.original_net.bus.shape[0]  # 电网母线个数
        self.n_gen = self.original_net.gen.shape[0]  # 电网发电机个数

        self.current_power_section = None
        print(ROOT_PATH)
        if not os.path.exists(os.path.join(ROOT_PATH, args.env_id, 'train_control_nets.pt')):
            print('making data........')
            generate(args)

        if train:
            self.control_nets = load_variable(os.path.join(ROOT_PATH, args.env_id, 'train_control_nets.pt'))
        else:
            self.control_nets = load_variable(os.path.join(ROOT_PATH, args.env_id, 'test_control_nets.pt'))

        self.n_net = len(self.control_nets['control_nets_power_section'])

        self.n_adjust_step = 2  # 调整步长
        self.adjust_ratio = np.linspace(0.5, 1.4, num=self.n_adjust_step)  # 调整率
        self.action_space = gym.spaces.Discrete(n=self.n_gen * self.n_adjust_step)
        # 创建动作空间，大小为调整步长*发电机个数

        self.observation_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(self.n_bus * 4,), dtype=np.float32)
        # 创建状态空间，大小为母线数*4，对应p v q theta, 状态范围为-1~1

        self.current_step = 0
        self.current_idx = None
        self.current_net_undo = None
        self.current_net = None
        self.converged = None
        self.success = None
        self.info = None

    def reset(self):
        self.current_step = 0
        self.current_idx = np.random.randint(0, self.n_net)  # 随机从电网样本中采样电网编号
        self.current_net = self._load_net(self.current_idx)  # 初始化电网PQ值
        self.current_net_undo = copy.deepcopy(self.current_net)  # 保存电网副本？
        self.current_power_section = copy.deepcopy(self.control_nets['control_nets_power_section'][self.current_idx])
        return self._get_state()    # 对current_net进行潮流计算

    # 指定某一样本
    def set(self, idx):

        if idx >= self.n_net:
            return None
        self.current_step = 0
        self.current_idx = idx
        self.current_net = self._load_net(self.current_idx)  # 初始化电网PQ值
        self.current_net_undo = copy.deepcopy(self.current_net)  # 保存电网副本？
        self.current_power_section = copy.deepcopy(self.control_nets['control_nets_power_section'][self.current_idx])
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

        x = torch.tensor(np.array(self.current_net.res_bus), dtype=torch.float32)  # res_bus?

        return x.view(-1)

    def step(self, action):
        action = int(action)
        self.current_step += 1
        self.current_net_undo = copy.deepcopy(self.current_net)
        action_gen_idx = np.floor(action / self.n_adjust_step)
        action_ratio_idx = action % self.n_adjust_step
        print("Action Info: {}号发电机出力水平调至{}%".format(action_gen_idx, self.adjust_ratio[action_ratio_idx]))
        self.current_net.gen['p_mw'][action_gen_idx] *= self.adjust_ratio[action_ratio_idx]
        state = self._get_state()

        self.current_power_section = self._get_power_section()
        reward, done, info = self._get_reward_done()
        return state, reward, done, info

    def _get_reward_done(self):
        info = {}
        self.success = None
        done = False
        if self.converged:
            if self.power_target[0] < self.current_power_section < self.power_target[1]:
                print("Done Info: success")
                reward = 20
                done = True
                self.success = True
            else:
                reward = -1 * abs(self.current_power_section -
                                  (self.power_target[1] + self.power_target[0]) / 2.0) / 1000.0
                # reward = -1
        else:
            print("Done Info: error")
            reward = -100
            done = True
            self.success = False

        if self.current_step > 50:
            print("Done Info: truncate")
            info["TimeLimit.truncated"] = not done
            done = True
            self.success = False

        info['is_converged'] = self.converged
        info['is_success'] = self.success

        return reward, done, info

    def _get_power_section(self):
        power_section = np.sum(np.abs(self.current_net.res_line.loc[self.section_lines, 'p_from_mw']))
        power_section += np.sum(np.abs(self.current_net.res_trafo.loc[self.section_trafos, 'p_hv_mw']))
        return power_section


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_id', type=str, default='case118', help="电网环境名")
    args = parser.parse_args()

    env = TransmissionSectionEnv(args, evaluation=True)
    n_action = env.action_space.n
    print(env.n_net)
    for i in range(2000):
        s0 = env.set(i)
        if s0 is not None:
            random = np.random.randint(low=0, high=n_action)
            state, reward, done, temp = env.step(random)
            print(i, '  ', reward)
            print(type(env.current_net.gen['p_mw']))
        else:
            break
        print(env.current_net.gen['p_mw'])
