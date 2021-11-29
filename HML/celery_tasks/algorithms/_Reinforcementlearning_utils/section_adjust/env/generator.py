# generate differents of environment
import pandapower as pp
import pandapower.networks as pn
import matplotlib.pyplot as plt
import numpy as np
import copy
from env.utils import save_variable
from env import ROOT_PATH
import os
'''
    此模块主要作用为生成不同负荷水平和变化负载、发电机编号的电网样本，同时用Pandapower计算
各样本的潮流断面功率功率，将符合要求区间的样本点剔除，剩下不满足功率区间的样本90%当做训练集，
10%当做测试集，并保存下来。
'''


def generate_control_nets(env_id, original_net, range_load_ratio, n_load_ratio, n_net_per_ratio,
                          n_load, n_gen, section_lines, section_trafos, power_target, data_mode):
    """
    生成大量随机电网样本
    :param env_id: 电网环境名
    :param original_net: 初始电网样本
    :param range_load_ratio: 负荷水平变化区间
    :param n_load_ratio: 负荷水平变化个数
    :param n_net_per_ratio: 每个负荷水平生成电网样本个数
    :param n_load: 电网负荷个数
    :param n_gen: 电网发电机个数
    :param section_lines: 输电断面中的输电线下标
    :param section_trafos: 输电断面中的变压器下标
    :param power_target: 目标功率区间
    :param data_mode: 数据生成模式，平均生成为‘average’
    :return:
    """
    control_nets_power_section = [[], []]
    control_nets_load_p = [[], []]
    control_nets_load_q = [[], []]
    control_nets_gen_p = [[], []]

    # 复制初始电网样本数据
    net_tmp = copy.deepcopy(original_net)  # 深拷贝

    # 生成等步长的负荷水平变化率
    load_ratios = np.linspace(range_load_ratio[0], range_load_ratio[1], n_load_ratio)
    # print(load_ratios)
    for ratio in load_ratios:
        for idx in range(n_net_per_ratio):
            # 随机选择需要修改的负荷及发电机，各为总数的一半(1/5)
            n_changed_load = np.random.randint(0, n_load, size=(int(n_load / 5),))
            n_changed_gen = np.random.randint(0, n_gen, size=(int(n_gen / 5),))

            # 复制初始电网样本数据
            net_tmp.load['p_mw'] = copy.deepcopy(original_net.load['p_mw'])
            net_tmp.load['q_mvar'] = copy.deepcopy(original_net.load['q_mvar'])
            net_tmp.gen['p_mw'] = copy.deepcopy(original_net.gen['p_mw'])

            # 在供需平衡的约束下修改负荷及发电机功率水平
            net_tmp.load.loc[n_changed_load, 'p_mw'] = net_tmp.load.loc[n_changed_load, 'p_mw'] * ratio
            net_tmp.load.loc[n_changed_load, 'q_mvar'] = net_tmp.load.loc[n_changed_load, 'q_mvar'] * ratio
            net_tmp.gen.loc[n_changed_gen, 'p_mw'] = net_tmp.gen.loc[n_changed_gen, 'p_mw'] * ratio * float(int(n_load / 5)) / float(int(n_gen / 5))

            # 平均初始样本功率
            if data_mode == 'average':
                each_data = sum(net_tmp.gen['p_mw'])/n_gen
                for i in range(n_gen):
                    net_tmp.gen['p_mw'][i] = each_data

            try:
                # 潮流计算
                pp.runpp(net_tmp)

                # 计算输电断面功率
                power_section = np.sum(np.abs(net_tmp.res_line.loc[section_lines, 'p_from_mw']))
                power_section += np.sum(np.abs(net_tmp.res_trafo.loc[section_trafos, 'p_hv_mw']))

                # 若输电断面功率在目标功率区间之内则抛弃该样本
                if power_target[0] > power_section or power_section > power_target[1]:
                    # 90% 训练样本，10% 测试样本
                    train_test_id = 0 if idx < n_net_per_ratio * 0.9 else 1
                    control_nets_power_section[train_test_id].append(copy.deepcopy(power_section))
                    control_nets_load_p[train_test_id].append(copy.deepcopy(net_tmp.load['p_mw']))
                    control_nets_load_q[train_test_id].append(copy.deepcopy(net_tmp.load['q_mvar']))
                    control_nets_gen_p[train_test_id].append(copy.deepcopy(net_tmp.gen['p_mw']))

            except Exception as e:
                # 若潮流不收敛则抛弃该样本
                assert isinstance(e, pp.powerflow.LoadflowNotConverged), 'Not Converged Error'
                continue

    # 绘制训练样本输电断面功率分布图
    plt.figure()
    plt.title("section power (train)")
    plt.scatter(list(range(len(control_nets_power_section[0]))), control_nets_power_section[0], marker='o', color='r', alpha=0.5, edgecolors='k', linewidths=1)
    plt.show()

    # 绘制测试样本输电断面功率分布图
    plt.figure()
    plt.title("section power (test)")
    plt.scatter(list(range(len(control_nets_power_section[1]))), control_nets_power_section[1], marker='o', color='b', alpha=0.5, edgecolors='k', linewidths=1)
    plt.show()

    train_control_nets = {'control_nets_power_section': control_nets_power_section[0],
                          'control_nets_load_p': control_nets_load_p[0],
                          'control_nets_load_q': control_nets_load_q[0],
                          'control_nets_gen_p': control_nets_gen_p[0]}

    test_control_nets = {'control_nets_power_section': control_nets_power_section[1],
                         'control_nets_load_p': control_nets_load_p[1],
                         'control_nets_load_q': control_nets_load_q[1],
                         'control_nets_gen_p': control_nets_gen_p[1]}

    os.makedirs(os.path.join(ROOT_PATH, env_id))
    save_variable(train_control_nets, os.path.join(ROOT_PATH, env_id, 'train_control_nets.pt'))
    save_variable(test_control_nets, os.path.join(ROOT_PATH, env_id, 'test_control_nets.pt'))


def generate(args):
    """
    生成大量随机电网样本，设置各类生成参数
    """

    # 电网环境名
    if args.env_id == 'case118':
        args.original_net = pn.case118()           # 初始电网样本
        args.section_lines = [104, 105, 106, 109]  # 输电断面中的输电线下标
        args.section_trafos = [9]                  # 输电断面中的变压器下标
        args.power_target = [300, 700]            # 目标功率区间
    else:
        assert False, 'env_id not exist'

    args.range_load_ratio = [0.1, 2.0]             # 负荷水平变化区间
    args.n_load_ratio = 20                         # 负荷水平变化个数
    args.n_net_per_ratio = 100                     # 每个负荷水平生成电网样本个数
    args.n_load = args.original_net.load.shape[0]  # 电网负载个数
    args.n_gen = args.original_net.gen.shape[0]    # 电网发电机个数
    args.data_mode = 'average'                     # 样本生成模式

    # 生成电网样本
    generate_control_nets(args.env_id, args.original_net, args.range_load_ratio, args.n_load_ratio, args.n_net_per_ratio,
                          args.n_load, args.n_gen, args.section_lines, args.section_trafos, args.power_target, args.data_mode)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_id', type=str, default='case118', help="电网环境名")
    args = parser.parse_args()

    generate(args)
