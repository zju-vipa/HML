import copy
import math
import os
from sklearn.preprocessing import MinMaxScaler
import xml.etree.ElementTree as ET
import shutil
import gym
import numpy as np
cnt = 0
Base_Mva = 100.0
Delta_p  = 1
Detail = 2


def copy_dirs(source_path, target_path):
    file_count = 0
    source_path = os.path.abspath(source_path)
    target_path = os.path.abspath(target_path)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if os.path.exists(source_path):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, target_path)
    return int(file_count)


class PSASPEnv(gym.Env):
    def __init__(self, args):
        self.args = args

        # 工作路径配置
        self.work_dir = args.work_dir  # "" (Temp 文件夹路径)
        self.data_dir = args.data_dir
        if self.args.is_training:
            self.run_dir = self.work_dir
        else:
            self.run_dir = args.run_dir
        self.case_file = args.case_file  # LF
        self.scence_file = args.scence_file  # AvaS_3000.npy

        # 基本元素信息
        self.get_element_info()
        self.get_basic_info()
        self.fluct_data = self.get_fluct_data(self.scence_file)
        self.fluct_scene = None
        self.steps = 0

        self.max_episode_steps = 20  # 最大探索步数

        self.action_result = []

        # 线路投切相关参数设定
        self.acline_capacity = 20 * np.ones(self.num_acline)  # 线路热稳极限传输功率 TODO：根据实际潮流情况制定差异化线路载流量，需要根据计算数据检查代码是否正确
        # self.special_aclines = np.array([140])  # 设置重点观察线路，示例中线路编号140 np.array([ 14,  24,  35,  54, 123, 164, 165, 213, 269, 275])
        # self.acline_capacity[self.special_aclines] = 10
        self.min_acline_rho_threshold = 0.9  # 线路负载率的低效阈值
        self.max_acline_rho_threshold = 1.0  # 线路负载率的最大阈值

        # 初始化线路跳闸相关向量
        # TODO：后续N-1及运维也可与此向量整合
        self.line_overload = np.zeros(self.num_acline)  # 初始化各线路的连续过载时长向量
        self.line_cut = np.zeros(self.num_acline)  # 初始化各线路的退运向量（智能体相关动作及线路跳闸导致的）

        # 平衡机相关参数设定
        self.balance_gens = [5, 34]  # 平衡机标号
        self.balance_gen_p_min = self.basic_gen_p_min[self.balance_gens]
        self.balance_gen_p_max = self.basic_gen_p_max[self.balance_gens]
        self.balance_gen_q_min = self.basic_gen_q_min[self.balance_gens]
        self.balance_gen_q_max = self.basic_gen_q_max[self.balance_gens]  # 平衡机出力上限

        self.reward_error = -100  # 潮流不收敛 reward
        self.reward_success = 500  # 成功调节 reward
        self.reward_gen_factor = 0.5  # 发电机调节量的惩罚因子

        self.action_gen = np.array([-1, 1], dtype=np.float32)  # 加减额定功率动作定义

        self.action_pcl = np.array([0, 1], dtype=np.float32)  # 启停并联电容电抗动作定义

        # self.action_avail_gen = np.where(self.basic_gen_p > 0)[0]  # 可控发电机
        self.action_avail_gen = np.where(self.basic_gen_p >= 0)[0]  # 可控发电机
        for balance_gen in self.balance_gens:  # 删除平衡发电机
            self.action_avail_gen = self.action_avail_gen[np.where(self.action_avail_gen != balance_gen)]

        self.action_converter = self.get_action_converter()  # 动作转换器
        self.action_space = gym.spaces.Discrete(n=self.action_converter.shape[0])

        self.observation_shape = (self.num_bus + self.num_acline + self.num_gen + 1,)  # 目标功率作为状态加入状态空间
        self.observation_space = gym.spaces.Box(low=-1.0, high=1.0, shape=self.observation_shape, dtype=np.float32)

    def get_action_converter(self):
        action_converter = np.zeros((len(self.action_avail_gen) * len(self.action_gen), self.num_gen))
        for i in range(len(self.action_avail_gen)):
            action_converter[(i * len(self.action_gen)):((i + 1) * len(self.action_gen)),
            self.action_avail_gen[i]] = self.action_gen
        return action_converter

    def reset(self, scene=None, flag=True):
        # 若未输入特别定义场景，则随机从场景集抽取，若定义，则以该定义内容作为场景源荷信息（演示集成用）
        copy_dirs(self.data_dir, self.work_dir)
        if scene is None:
            # 随机抽样得到训练场景
            scene_id = 1
            print("############")
            print("Scene Info: scenario:{}".format(scene_id))
            self.fluct_scene = self.fluct_data[(4 * scene_id):(4 * (scene_id + 1))]
        else:
            self.fluct_scene = scene

        self.set_scene_info(self.fluct_scene)
        self.steps = 0
        self.call_pf()
        #bus_v, acline_p, gen_p, _ = self.get_pf_result()
        bus_v, acline_p, gen_p, _, gen_q = self.get_pf_result()
        state = np.array(list(bus_v) + list(acline_p) + list(gen_p) + [self.target_ps[0]])
        #reward, done, info = self.get_reward(0.0, bus_v, acline_p, gen_p, _)

        reward, done, info = self.get_reward(0.0, bus_v, acline_p, gen_p, _, gen_q, 0.0, 0.0)
        return state



    def step(self, action):
        self.steps += 1
        init_target_sec_p = self.get_sec_p_sum(self.target_name[0])
        print("action: ", action)
        # 播报动作的物理意义
        action_gen_id = np.where(self.action_converter[action] != 0) [0][0]
        delta_gen_p = 0  # 发电机调整量

        if action_gen_id < self.num_gen:
            delta_gen_p = self.action_converter[action, action_gen_id] * Delta_p
            final_gen_p = delta_gen_p +self.scene_gen_p[action_gen_id]
            final_gen_p = min(max(self.basic_gen_p_min[action_gen_id], final_gen_p), self.basic_gen_p_max[action_gen_id])
            print('第{}步，Action Info: {}号发电机出力水平从{}调至{}'.format(self.steps, action_gen_id, self.scene_gen_p[action_gen_id], final_gen_p))
            action_flag = np.where(self.action_converter[action] != 0)[0]
            #self.action_count[action_flag[0]] += 1

            self.action_result.append([action_gen_id, self.scene_gen_p[action_gen_id], final_gen_p])
            self.scene_gen_p[action_gen_id] = final_gen_p
            self.scene_gen_flag[action_gen_id] = 1 if final_gen_p != 0 else 0
            gen_data = self.read_file_data('.L5')
            f_w = open(os.path.join(self.work_dir, self.case_file + '.L5'), 'w')
            for i in range(len(gen_data)):  # 逐行写入对应发电机的出力信息
                gen_info = list(gen_data[i])  # 将对应行的发电机数据读出并转换为列表方便修改

                gen_p_info = format(float(self.scene_gen_p[i]), '.6f')
                gen_info[2] = format(int(self.scene_gen_flag[i]))  # 按照PSASP数据格式和占位情况将最新的发电机有效标志信息更新self.scene_gen_p[i]
                gen_info[(31 - len(gen_p_info)):31] = gen_p_info  # 按照PSASP数据格式和占位情况将最新的发电机有效标志信息更新
                update_gen_info = ''.join(gen_info)
                f_w.writelines(update_gen_info)
            f_w.close()

        elif action_gen_id < (self.num_gen + self.num_load):
            # print('Action Info: {}号负荷调至{}%'.format(action_flag[0], 100 * int(1 - self.scene_gen_flag[action_flag[0]])))
            raise NotImplementedError
        else:
            # print('Action Info: {}号联络线进行投切动作'.format(action_flag[0] - self.num_gen - self.num_load))
            raise NotImplementedError

        self.call_pf()
        #bus_v, acline_p, gen_p, error_flag = self.get_pf_result()
        bus_v, acline_p, gen_p, error_flag, gen_q = self.get_pf_result()
        state = np.array(list(bus_v) + list(acline_p) + list(gen_p) + [self.target_ps[0]])
        # TODO：done出现的情况应全面考虑，如 到达场景最后一个时刻(self.step)，或因PSASP特性出现的其他表现
        #reward, done, info = self.get_reward(delta_gen_p, bus_v, acline_p, gen_p, error_flag)
        final_target_sec_p = self.get_sec_p_sum(self.target_name[0])
        reward, done, info = self.get_reward(delta_gen_p, bus_v, acline_p, gen_p, error_flag, gen_q, init_target_sec_p,
                                             final_target_sec_p)

        info.update(self.get_dic_info(bus_v, gen_p, acline_p))
        info.update(self.get_action_info())
        # print(info)
        return state, reward, done, info

    def get_reward(self, delta_gen_p, bus_v, acline_p, gen_p, error_flag, gen_q, init_p, final_p):
        reward = 0
        done = False
        info = {}
        reward_delta = 0.5

        # valid_bus_v = bus_v[bus_v != 0]
        if error_flag > 0:
            if not self.check_v_range(bus_v, 2):
                print("bus constrain failed!")
            if not self.check_sec(2):
                print("cut constrain failed!")
            if not self.check_balance(gen_p, gen_q):
                print("balance constrain failed!")
            reward += self.reward_error
            done = True

            info["done_info"] = "error"
            info["done_steps"] = self.steps
            if Detail >= 1:
                print("Done Info: error")
                print("Done Steps: {}".format(self.steps))
        else:
            # special_acline_rho = abs(acline_p[self.special_aclines] / self.acline_capacity)

            if self.is_success(acline_p):
                if self.check_v_range(bus_v, 0) and self.check_sec(2) and self.check_balance(gen_p, gen_q):
                    # 当系统在规定步长内将潮流调节收敛，则赋予最终奖励
                    reward += self.reward_success
                    done = True
                    info["done_info"] = "success"
                    info["done_steps"] = self.steps
                    if Detail >= 1:
                        print("Done Info: success")
                        print("Done Steps: {}".format(self.steps))

                else:
                    if not self.check_v_range(bus_v, 2):
                        print("bus constrain failed!")
                    if not self.check_sec(2):
                        print("cut constrain failed!")
                    if not self.check_balance(gen_p, gen_q):
                        print("balance constrain failed!")

            # 重点线路传输能力 reward
            # x = np.maximum(special_acline_rho - self.min_acline_rho_threshold, 0)
            # x[special_acline_rho >= self.max_acline_rho_threshold] = -x[
            #     special_acline_rho >= self.max_acline_rho_threshold]
            # reward += sum(x)

            # 平衡机越限 reward
            for i in range(len(self.balance_gens)):
                p = gen_p[self.balance_gens[i]]
                q = gen_q[self.balance_gens[i]]
                if p > self.balance_gen_p_max[i] or p < self.balance_gen_p_min[i]:
                    reward -= 2.5
                if q > self.balance_gen_q_max[i] or q < self.balance_gen_q_min[i]:
                    reward -= 2.5
            # reward -= sum(np.minimum(abs(gen_p[self.balance_gens]-self.balance_gen_p_min[[0,1]]), abs(gen_p[self.balance_gens]-self.balance_gen_p_max[[0,1]])))
            # reward -= sum(np.minimum(abs(gen_q[self.balance_gens]-self.balance_gen_q_min[[0,1]]), abs(gen_q[self.balance_gens]-self.balance_gen_q_max[[0,1]])))
            # print("平衡机越限 reward",-sum(np.maximum(balance_gen_rho - self.max_gen_rho_threshold, 0)))
            # 发电机调节量惩罚 reward
            # reward -= self.reward_gen_factor * delta_gen_p + reward_delta
            # print("发电机调节量惩罚 reward", -(self.reward_gen_factor * delta_gen_p + reward_delta))


            # 调节目标reward
            l, r = self.target_ps[0] * 0.9, self.target_ps[0] * 1.1
            init_dis = 0.0 if (init_p >= l and init_p <= r) else min(abs(init_p - l), abs(init_p - r))
            final_dis = 0.0 if (final_p >= l and final_p <= r) else min(abs(final_p - l), abs(final_p - r))
            # cut_reward = -2.5 if (init_p ==final_p and (final_p < l or final_p > r)) else (init_dis - final_dis) * 100
            # final_p_ratio = final_p/self.target_ps[0]
            cut_reward = -abs(final_p - self.target_ps[0] / 100)
            reward += cut_reward
            print(f"断面reward：{cut_reward} 初始功率：{init_p} 调整后功率：{final_p}")
            # print("断面功率reward", cut_reward)
            # print("totalReward", reward)
        if self.steps == self.max_episode_steps:
            info["done_info"] = "truncate"
            info["done_steps"] = self.steps
            info["TimeLimit.truncated"] = not done
            reward = -50
            if Detail >= 1:
                print("Done Info: truncate")
                print("Done Steps: {}".format(self.steps))
            done = True

        return reward, done, info

    def call_pf(self):
        # 运行潮流计算
        # pf_process = subprocess.Popen(os.path.join(self.work_dir, 'WMLFRTMsg.exe'), stdout=0)
        # time.sleep(self.pf_wait_time)  # 系统稍作暂停以确保数据结果文件的更新
        # pf_process.kill()
        cmd = f"WMLFRTMsg –e -lfpath " + self.work_dir + " -ename " + os.path.join(self.work_dir, "e_union_lf.out")

        output = os.system(cmd)
        # 返回值 0 或者其他 再观察
        # https://blog.51cto.com/u_15688254/5927508
        # print('cmd output:', output)

    def get_pf_result(self):
        # --------------------- 母线信息提取 ---------------------
        bus_data = self.read_file_data('.LP1')
        bus_v = np.zeros(self.num_bus)
        bus_err = False
        for i in range(1, len(bus_data)):  # 第一行为计算成功与否的信息，故直接从第二行读取
            bus_info = bus_data[i].split(',')  # 根据PSASP的数据格式和分割情况，提取对应的母线电压信息
            if '***************' in bus_info:  # TODO: modified
                bus_err = True
            else:
                ref_bus_id = self.basic_bus_name.index(bus_info[3][1:-1])
                bus_v[ref_bus_id] = float(bus_info[1])

        # --------------------- 线路信息提取 ---------------------
        # 读取交流线结果数据（当前读取结果为交流线+并联电容电抗器，直流线需要进一步理解查阅）
        acline_err, acline_p, _, __, ___ = self.get_LP2_data()

        # --------------------- 发电信息提取 ---------------------
        gen_data = self.read_file_data('.LP5')
        gen_p = np.zeros((self.num_gen))  # 建立发电机功率记录向量
        gen_q = np.zeros((self.num_gen))  # 建立发电机功率记录向量
        gen_err = False
        for i in range(len(gen_data)):
            gen_info = gen_data[i].split(',')
            if len(gen_info[4][1:-1]) == 0:  # 当文件中发电机名称为空时，视为出现潮流收敛问题，但有待进一步检查
                gen_err = True
            else:
                ref_gen_id = self.basic_gen_name.index(gen_info[4][1:-1])
                # if (gen_info[4][1:-1])=='Gen2E-7':
                #     print("1")
                gen_p[ref_gen_id] = float(gen_info[1])
                gen_q[ref_gen_id] = float(gen_info[2])

        error_flag = bus_err + acline_err + gen_err

        return bus_v, acline_p, gen_p, error_flag, gen_q

    def get_element_info(self):
        # 获取系统中的设备数量信息
        # 300节点算例存在母线270条，交流线452条（含并联电抗器），直流线7条，发电机95台，负荷142个
        element_data = self.read_file_data('.L0')
        element_info = element_data[0].split()  # 根据PSASP的数据格式和分割情况，提取对应的基本元件数量信息
        self.num_bus = int(element_info[0][:-1]) # + 1  # TODO：L0文件与实际L1文件中差1位，目前取后者
        self.num_acline = int(element_info[1][:-1])
        self.num_dcline = int(element_info[3][:-1])
        self.num_gen = int(element_info[4][:-1])
        self.num_load = int(element_info[5][:-1])

    def get_basic_info(self):
        # --------------------- 基础发电信息提取 ---------------------
        gen_data = self.read_file_data('.L5')
        self.basic_gen_p = np.zeros((len(gen_data)))
        self.basic_gen_q = np.zeros((len(gen_data)))
        self.basic_gen_flag = np.zeros((len(gen_data)))
        self.basic_gen_bus = np.zeros((len(gen_data)))
        self.basic_gen_p_max = np.zeros((len(gen_data)))
        self.basic_gen_p_min = np.zeros(len(gen_data))
        self.basic_gen_q_max = np.zeros((len(gen_data)))
        self.basic_gen_q_min = np.zeros(len(gen_data))
        self.basic_gen_name = []
        for i in range(len(gen_data)):
            gen_info = gen_data[i].split()  # 根据PSASP的数据格式和分割情况，提取对应的基本发电机有功无功信息
            self.basic_gen_flag[i] = int(gen_info[0][:-1])
            self.basic_gen_p[i] = float(gen_info[3][:-1]) * self.basic_gen_flag[i]
            self.basic_gen_q[i] = float(gen_info[4][:-1]) * self.basic_gen_flag[i]
            self.basic_gen_p_max[i] = float(gen_info[9][:-1])
            self.basic_gen_p_min[i] = float(gen_info[10][:-1])
            self.basic_gen_q_max[i] = float(gen_info[7][:-1])
            self.basic_gen_q_min[i] = float(gen_info[8][:-1])
            self.basic_gen_bus[i] = int(gen_info[1][:-1]) - 1  # TODO：检查 human_control 模块此处是否出现索引偏差
            self.basic_gen_name.append(gen_info[-1][4:-2])

        # Modify
        # --------------------- 基础母线信息提取 ---------------------
        bus_data = self.read_file_data('.L1')
        self.basic_bus_v_min = np.zeros(len(bus_data))
        self.basic_bus_v_max = np.zeros(len(bus_data))
        self.basic_bus_v_base = np.zeros(len(bus_data))
        self.basic_bus_v_used = np.zeros(len(bus_data))  # 只考虑投入使用的线路，否则会报错，因为LP1文件中没有使用的线路不显示
        self.basic_bus_name = []
        for i in range(len(bus_data)):
            bus_info = ((bus_data[i].replace(" ", "")).replace(",", ", ")).split(
                ",")  # 根据PSASP的数据格式和分割情况，提取对应的基本发负荷功无功信息
            self.basic_bus_name.append(bus_info[0][1:-1])
            self.basic_bus_v_base[i] = float(bus_info[1][:-1])
            self.basic_bus_v_min[i] = float(bus_info[4][:-1])
            self.basic_bus_v_max[i] = float(bus_info[3][:-1])
            self.basic_bus_v_used[i] = int(bus_info[2])

        # --------------------- 基础负荷信息提取 ---------------------
        load_data = self.read_file_data('.L6')
        self.basic_load_p = np.zeros(len(load_data))
        self.basic_load_q = np.zeros(len(load_data))
        for i in range(len(load_data)):
            load_info = load_data[i].split()  # 根据PSASP的数据格式和分割情况，提取对应的基本发负荷功无功信息
            self.basic_load_p[i] = float(load_info[4][:-1])
            self.basic_load_q[i] = float(load_info[5][:-1])

        # Modify
        # --------------------- 基础线路信息提取 ---------------------
        line_data = self.read_file_data('.L2')
        self.basic_line_status = np.zeros(len(line_data), dtype=int)
        self.basic_line_i = np.zeros(len(line_data), dtype=int)
        self.basic_line_j = np.zeros(len(line_data), dtype=int)  # 分别初始化线路的初始状态、i/j侧的母线编号数组
        self.basic_line_lc = np.zeros(len(line_data))
        self.basic_line_lim = np.zeros(len(line_data))
        self.basic_line_name = []
        for i in range(len(line_data)):
            line_info = ((line_data[i].replace(" ", "")).replace(",", ", ")).split()  # 根据PSASP的数据格式和分割情况，提取对应的基本线路状态信息
            self.basic_line_status[i] = int(line_info[0][:-1])
            self.basic_line_i[i] = int(line_info[1][:-1])
            self.basic_line_j[i] = int(line_info[2][:-1])
            self.basic_line_lc[i] = float(line_info[13][:-1])
            self.basic_line_lim[i] = float(line_info[14][:-1])
            self.basic_line_name.append(line_info[-1][1:-2])

        # Modify
        # --------------------- 变压器信息提取 ---------------------
        '''
        trans_data = self.read_file_data('.L3')
        self.basic_trans_lim = np.zeros(len(trans_data))
        self.basic_trans_name = []
        for i in range(len(trans_data)):
            trans_info = (trans_data[i].replace(" ", "")).split(",")  # 根据PSASP的数据格式和分割情况，提取对应的基本发负荷功无功信息
            self.basic_trans_lim[i] = float(trans_info[18][:-1])
            self.basic_trans_name.append(trans_info[24][1:-1])
        '''

        # Modify
        # --------------------- 断面约束信息提取 ---------------------
        sec_data = self.read_spec_data(os.path.join(self.run_dir, "LFCutAdj.txt"))
        constrain_info = sec_data[0].replace(" ", "").split(",")
        self.lin_con = True if int(constrain_info[0]) == 1 else False
        self.sec_con = True if int(constrain_info[1]) == 1 else False
        sec_data = sec_data[1:]
        self.sec_name = []
        self.sec_p_min = np.zeros(len(sec_data))
        self.sec_p_max = np.zeros(len(sec_data))
        for i in range(len(sec_data)):
            sec_info = sec_data[i].replace(" ", "").split(',')
            self.sec_name.append(sec_info[0][1:-1])
            self.sec_p_max[i] = float(sec_info[1])
            self.sec_p_min[i] = float(sec_info[2])
        # --------------------- 断面构成信息提取 ---------------------
        self.sec_tree = self.read_xml_data(os.path.join(self.run_dir, "LFCutConf.xml"))
        # --------------------- 调整目标 ---------------------
        target_data = self.read_spec_data(os.path.join(self.run_dir, "LFCutConf_Target.txt"))
        self.target_name = []
        self.target_type = np.zeros(len(target_data))
        self.target_ps = np.zeros(len(target_data))
        for i in range(len(target_data)):
            target_info = target_data[i].replace(" ", "").split(",")
            self.target_name.append(target_info[0][1:-1])
            self.target_type[i] = float(target_info[1])
            self.target_ps[i] = float(target_info[2])
        # 生成初始时刻的邻接矩阵
        # 根据初始时刻线路的连接关系确定初始邻接矩阵，由于母线编号从1开始，故此处索引-1；
        # 将无效的、单侧断开的线路对应连接关系处均赋值0
        # TODO:后续应特别处理其中的并联电抗器，并考虑直流线
        self.adj_matrix = np.zeros((self.num_bus, self.num_bus))
        for i in range(len(line_data)):
            self.adj_matrix[self.basic_line_i[i] - 1, self.basic_line_j[i] - 1] = self.basic_line_status[i]
            self.adj_matrix[self.basic_line_j[i] - 1, self.basic_line_i[i] - 1] = self.basic_line_status[i]
        self.adj_matrix[self.adj_matrix != 1] = 0

    def check_sec(self, flag=0):
        for i in range(len(self.sec_name)):
            sec_p = self.get_sec_p_sum(self.sec_name[i])*100
            if sec_p < self.sec_p_min[i] or sec_p > self.sec_p_max[i]:
                if flag >= 2:
                    print(f"断面约束：断面{self.sec_name[i]} 功率下限：{self.sec_p_min[i]} 断面功率：{sec_p} 断面功率上限：{self.sec_p_max[i]}", sec_p)
                return False
        return True


    #计算断面功率之和
    def get_sec_p_sum(self, cut_name):
        root = self.sec_tree
        ret = 0.0
        for i in range(len(root)):
            sec_info = root[i].attrib
            if sec_info["Name"]!=cut_name:
                continue
            for ch in root[i]:
                line_info = ch.attrib
                sig = 1.0 if float(line_info["BranchDirection"]) == 1 else -1.0
                line_id=0
                line_name = line_info["BranchName"]
                for  index in range(len(self.basic_line_name)):
                    if not (line_name in self.basic_line_name[index]):
                        continue
                    line_id = index
                    break
                _, p_i, __, p_j, ___ = self.get_LP2_data()
                p_num = p_i[line_id] if float(line_info["BranchDirection"]) == 1 else -1.0 * p_j[line_id]
                if Detail == 3:
                    print(f"支路 {line_name} (断面 {cut_name} ) line_p : {p_num}")
                ret += p_num
        return ret
    #检查母线电压
    def check_v_range(self, bus_v, flag=0):
        for i in range(len(bus_v)):
            if self.basic_bus_v_used[i] == 0:
                continue
            real_v = bus_v[i] * self.basic_bus_v_base[i]

            # if flag >= 2:
            #     print(f"母线电压约束：母线{self.basic_bus_name[i]} 下限：{self.basic_bus_v_min[i]} 电压: {real_v}  上限：{self.basic_bus_v_max[i]}")
            if real_v < self.basic_bus_v_min[i] or real_v > self.basic_bus_v_max[i]:
                if flag >= 2:
                    print(f"******母线电压约束：母线{self.basic_bus_name[i]} 下限：{self.basic_bus_v_min[i]} 电压: {real_v}  上限：{self.basic_bus_v_max[i]}")
                return False
        return True
    #检查线路
    def check_line(self,bus_v,flag=0):
        _, acline_p_i, acline_q_i, __, ___ = self.get_LP2_data()
        for i in range(len(self.basic_line_name)):
            acline_v_i = bus_v[self.basic_line_i[i]]
            v_base = self.basic_bus_v_base[self.basic_line_i[i]]
            acline_i = np.sqrt(acline_p_i*acline_p_i + acline_q_i * acline_q_i)/acline_v_i * Base_Mva / v_base / np.sqrt(3.0)
            ratio = acline_i/self.basic_line_lc[i]
            if any(acline_i > self.basic_line_lc[i]):# 电流是否越限
                return False
            if any(ratio > self.basic_line_lim[i]):#
                return False
        return True
    #判断是否满足条件
    def is_success(self, acline_p, check_id=0):
        check_p = acline_p[self.basic_line_name.index(self.target_name[check_id])] if self.target_type[
                                                                                          check_id] == 1 else self.get_sec_p_sum(
            self.target_name[check_id]) * 100
        type_name = "断面" if self.target_type[check_id] != 1 else "支路"
        if Detail >= 1:
            print(
                f"{type_name}目标 {self.target_name[check_id]} 上限：{self.target_ps[check_id] * 1.03}  当前功率：{check_p} 下限{self.target_ps[check_id] * 0.97}")
        if check_p < self.target_ps[check_id] * 0.97 or check_p > self.target_ps[check_id] * 1.03:
            return False
        return True
    def check_balance(self, gen_p, gen_q):
        for i in range(len(self.balance_gens)):
            p = gen_p[self.balance_gens[i]]
            q = gen_q[self.balance_gens[i]]
            if p < self.balance_gen_p_min[i] or p > self.balance_gen_p_max[i]:
                return False
            if q < self.balance_gen_q_min[i] or q>self.balance_gen_q_max[i]:
                return False
        return True

    def set_scene_info(self, fluct_scene, flag=False):
        flag = True
        import copy
        if flag:    #如果flag==True,用文件中的单一场景，如果flag==False,使用AVaS生成的场景
            self.scene_gen_p = copy.deepcopy(self.basic_gen_p)
            self.scene_gen_q = copy.deepcopy(self.basic_gen_q)
            self.scene_load_p = copy.deepcopy(self.basic_load_p)
            self.scene_load_q = copy.deepcopy(self.basic_load_q)
            self.scene_line_status = copy.deepcopy(self.basic_line_status)
            self.scene_gen_flag = copy.deepcopy(self.basic_gen_flag)
        else :
            # scene_gen_p, scene_gen_q, scene_load_p, scene_load_q 初始化方式有变化
            self.scene_gen_p = copy.deepcopy(fluct_scene[0])
            self.scene_gen_q = copy.deepcopy(fluct_scene[1])
            self.scene_load_p = copy.deepcopy(fluct_scene[2])
            self.scene_load_q = copy.deepcopy(fluct_scene[3])
            self.scene_line_status = copy.deepcopy(self.basic_line_status)
            self.scene_gen_flag = copy.deepcopy(self.basic_gen_flag)

            # --------------------- 发电信息设置 ---------------------
            gen_data = self.read_file_data('.L5')  # 初始化源荷计算数据读取矩阵，方便后续在此基础上写入更新相关数据
            f_w = open(os.path.join(self.work_dir, self.case_file + '.L5'), 'w')
            for i in range(len(gen_data)):  # 逐行写入对应发电机的出力信息
                gen_info = list(gen_data[i])  # 将对应行的发电机数据读出并转换为列表方便修改
                gen_p_info = format(float(self.scene_gen_p[i]), '.6f')
                gen_q_info = format(float(self.scene_gen_q[i]), '.6f')  # 按照PSASP数据格式将最新的有功/无功出力信息转化为字符
                gen_info[(31 - len(gen_p_info)):31] = gen_p_info
                gen_info[(47 - len(gen_q_info)):47] = gen_q_info  # 按照PSASP数据格式和占位情况将最新的有功/无功出力信息更新
                gen_info[2] = format(int(self.scene_gen_flag[i]))  # 按照PSASP数据格式和占位情况将最新的发电机有效标志信息更新
                update_gen_info = ''.join(gen_info)  # 将列表转换为字符串
                f_w.writelines(update_gen_info)
            f_w.close()

            # --------------------- 负荷信息设置 ---------------------
            load_data = self.read_file_data('.L6')  # 初始化源荷计算数据读取矩阵，方便后续在此基础上写入更新相关数据
            f_w = open(os.path.join(self.work_dir, self.case_file + '.L6'), 'w')
            for i in range(len(load_data)):  # 逐行写入对应负荷数据信息
                load_info = list((load_data[i]))  # 将对应行的负荷数据读出并转换为列表方便修改
                load_p_info = format(float(self.scene_load_p[i]), '.6f')
                load_q_info = format(float(self.scene_load_q[i]), '.6f')  # 按照PSASP数据格式将最新的有功/无功负荷信息转化为字符
                load_info[(38 - len(load_p_info)):38] = load_p_info
                load_info[(54 - len(load_q_info)):54] = load_q_info  # 按照PSASP数据格式和占位情况将最新的有功/无功负荷信息更新
                update_load_info = ''.join(load_info)  # 将列表转换为字符串
                f_w.writelines(update_load_info)
            f_w.close()

            # --------------------- 线路信息设置 ---------------------
            line_data = self.read_file_data('.L2')  # 初始化线路计算数据读取矩阵，方便后续在此基础上写入更新相关数据
            f_w = open(os.path.join(self.work_dir, self.case_file + '.L2'), 'w')
            for i in range(len(line_data)):  # 逐行写入对应线路信息
                line_info = list(line_data[i])  # 将对应行的线路数据读出并转换为列表方便修改
                line_status_info = str(self.scene_line_status[i])  # 按照PSASP数据格式将最新的线路开断信息转化为字符
                line_info[2] = line_status_info  # 按照PSASP数据格式和占位情况将最新的线路开断信息更新
                update_line_info = ''.join(line_info)  # 将列表转换为字符串
                f_w.writelines(update_line_info)
            f_w.close()
            # 获取当前时刻的邻接矩阵
            # 根据当前时刻线路的连接关系确定初始邻接矩阵，由于母线编号从1开始，故此处索引-1；
            # TODO:后续应特别处理其中的并联电抗器，并考虑直流线
            # 将无效的、单侧断开的线路对应连接关系处均赋值0
        self.adj_matrix = np.zeros((self.num_bus, self.num_bus))
        for i in range(len(self.scene_line_status)):
            self.adj_matrix[self.basic_line_i[i] - 1, self.basic_line_j[i] - 1] = self.scene_line_status[i]
            self.adj_matrix[self.basic_line_j[i] - 1, self.basic_line_i[i] - 1] = self.scene_line_status[i]
        self.adj_matrix[self.adj_matrix != 1] = 0

    def get_fluct_data(self, file):
        fluct_data = np.load(os.path.join(self.data_dir, file), allow_pickle=True)
        return fluct_data

    def read_file_data(self, ext_name):
        file_data = []
        with open(os.path.join(self.work_dir, self.case_file + ext_name)) as f:
            for line in f.readlines():
                file_data.append(line)
        return file_data

    def read_spec_data(self, name):
        file_data = []
        with open(name) as f:
            for l in f.readlines():
                if l[0] == '#':
                    continue
                file_data.append(l)
        return file_data
    def read_xml_data(self, name):
        tree = ET.parse(name)
        rt = tree.getroot()
        return rt

    def get_LP2_data(self):

        acline_data = self.read_file_data('.LP2')
        acline_p_i = np.zeros(self.num_acline)  # 分别建立交流线i侧的有功和无功传输功率数组
        acline_q_i = np.zeros(self.num_acline)
        acline_p_j = np.zeros(self.num_acline)  # 分别建立交流线i侧的有功和无功传输功率数组
        acline_q_j = np.zeros(self.num_acline)
        acline_err = False
        for i in range(len(acline_data)):
            acline_info = acline_data[i].split(',')  # 根据PSASP的数据格式和分割情况，提取对应的母线电压信息
            if '************' in acline_info:  # TODO: modified
                acline_err = True
            else:
                ref_acline_id = self.basic_line_name.index(acline_info[9][1:-1])
                acline_p_i[ref_acline_id] = float(acline_info[3])
                acline_q_i[ref_acline_id] = float(acline_info[4])
                acline_p_j[ref_acline_id] = float(acline_info[5])
                acline_q_j[ref_acline_id] = float(acline_info[6])
        return acline_err, acline_p_i, acline_q_i, acline_p_j, acline_q_j

    def get_dic_info(self, bus_v, gen_p, acline_p):
        ret_info={"v_str": [],
                  "v_pair": [],
                  "balance_str": [],
                  "balance_pair": [],
                  "sec_str": [],
                  "sec_pair": [],
                  "line_str": [],
                  "line_pair": [],
                  "gen_str": [],
                  "gen_pair": [],
                  "target_sec_str": [],
                  "target_sec_pair": [],}

        for i in range(len(bus_v)):
            if self.basic_bus_v_used[i] == 0:
                continue
            real_v = bus_v[i] * self.basic_bus_v_base[i]
            if real_v < self.basic_bus_v_min[i]:
                ret_info["v_str"].append(f"母线{self.basic_bus_name[i]} 电压：{real_v:.2f} 下限：{self.basic_bus_v_min[i]:.2f} 上限：{self.basic_bus_v_max[i]:.2f} 小于下限")
                ret_info["v_pair"].append(("母线"+self.basic_bus_name[i], real_v, self.basic_bus_v_min[i], self.basic_bus_v_max[i], "小于下限"))
            elif real_v > self.basic_bus_v_max[i]:
                ret_info["v_str"].append(f"母线{self.basic_bus_name[i]} 电压：{real_v:.2f} 下限：{self.basic_bus_v_min[i]:.2f} 上限：{self.basic_bus_v_max[i]:.2f} 大于上限")
                ret_info["v_pair"].append(("母线"+self.basic_bus_name[i], real_v, self.basic_bus_v_min[i], self.basic_bus_v_max[i], "大于上限"))
            else:
                ret_info["v_str"].append(f"母线{self.basic_bus_name[i]} 电压：{real_v:.2f} 下限：{self.basic_bus_v_min[i]:.2f} 上限：{self.basic_bus_v_max[i]:.2f} 约束区间内")
                ret_info["v_pair"].append(("母线"+self.basic_bus_name[i], real_v, self.basic_bus_v_min[i], self.basic_bus_v_max[i], "区间内"))

        for i in range(len(acline_p)):
            ret_info["line_str"].append(f"线路{self.basic_line_name[i]}功率：{acline_p[i]:.2f}")
            ret_info["line_pair"].append(("线路"+self.basic_line_name[i], acline_p[i]))

        for i in range(len(self.balance_gens)):
            ba_p = gen_p[self.balance_gens[i]]*100.0
            ba_name = self.basic_gen_name[self.balance_gens[i]]
            ba_max = self.balance_gen_p_max[i]*100.0
            ba_min = self.balance_gen_p_min[i]*100.0
            if ba_p < ba_min:
                ret_info["balance_str"].append(f"平衡机{ba_name} 当前功率:{ba_p:.2f}, 约束范围：[{ba_min:.2f}, {ba_max:.2f}] 小于下限")
                ret_info["balance_pair"].append(("平衡机"+ba_name, ba_p, ba_min, ba_max, "小于下限"))
            elif ba_p > ba_max:
                ret_info["balance_str"].append(f"平衡机{ba_name} 当前功率:{ba_p:.2f}, 约束范围：[{ba_min:.2f}, {ba_max:.2f}] 大于上限")
                ret_info["balance_pair"].append(("平衡机"+ba_name, ba_p, ba_min, ba_max, "大于上限"))
            else:
                ret_info["balance_str"].append(f"平衡机{ba_name} 当前功率:{ba_p:.2f}, 约束范围：[{ba_min:.2f}, {ba_max:.2f}] 约束区间内")
                ret_info["balance_pair"].append(("平衡机"+ba_name, ba_p, ba_min, ba_max, "区间内"))

        for i in range(len(self.sec_name)):
            sec_p = self.get_sec_p_sum(self.sec_name[i])*100
            if sec_p < self.sec_p_min[i]:
                ret_info["sec_str"].append(f"目标断面 当前功率:{sec_p:.2f}, 约束范围：[{self.sec_p_min[i]:.2f}, {self.sec_p_max[i]:.2f}] 小于下限")
                ret_info["sec_pair"].append(("目标断面", sec_p, self.sec_p_min[i], self.sec_p_max[i], "小于下限"))
            elif sec_p > self.sec_p_max[i]:
                ret_info["sec_str"].append(f"目标断面 当前功率:{sec_p:.2f}, 约束范围：[{self.sec_p_min[i]:.2f}, {self.sec_p_max[i]:.2f}] 大于上限")
                ret_info["sec_pair"].append(("目标断面", sec_p, self.sec_p_min[i], self.sec_p_max[i], "大于上限"))
            else:
                ret_info["sec_str"].append(f"目标断面 当前功率:{sec_p:.2f}, 约束范围：[{self.sec_p_min[i]:.2f}, {self.sec_p_max[i]:.2f}] 约束区间内")
                ret_info["sec_pair"].append(("目标断面", sec_p, self.sec_p_min[i], self.sec_p_max[i], "区间内"))

        for i in range(len(self.basic_gen_name)):
            gen_p_i = gen_p[i]*100.0
            gen_name = self.basic_gen_name[i]
            gen_max = self.basic_gen_p_max[i]*100.0
            gen_min = self.basic_gen_p_min[i]*100.0
            if gen_p_i < gen_min:
                ret_info["gen_str"].append(f"发电机{gen_name} 当前功率:{gen_p_i:.2f}, 约束范围：[{gen_min:.2f}, {gen_max:.2f}] 小于下限")
                ret_info["gen_pair"].append(("发电机"+gen_name, gen_p_i, gen_min, gen_max, "小于下限"))
            elif gen_p_i > gen_max:
                ret_info["gen_str"].append(f"发电机{gen_name} 当前功率:{gen_p_i:.2f}, 约束范围：[{gen_min:.2f}, {gen_max:.2f}] 大于上限")
                ret_info["gen_pair"].append(("发电机"+gen_name, gen_p_i, gen_min, gen_max, "大于上限"))
            else:
                ret_info["gen_str"].append(f"发电机{gen_name} 当前功率:{gen_p_i:.2f}, 约束范围：[{gen_min:.2f}, {gen_max:.2f}] 约束区间内")
                ret_info["gen_pair"].append(("发电机"+gen_name, gen_p_i, gen_min,gen_max, "区间内"))

        p = self.get_sec_p_sum(self.target_name[0])*100
        target_p = self.target_ps[0]
        ret_info["target_sec_str"]=f"目标断面当前功率:{p:.2f} 目标功率: {target_p:.2f}"
        ret_info["target_sec_pair"].append((self.target_name[0], p, target_p))
        return ret_info

    def get_action_info(self):
        ret_dic={"action_str":[], "action_idx":[]}
        self.cur_avail_action_list=[]
        for action in range(self.action_converter.shape[0]):
            action_gen_id = np.where(self.action_converter[action] != 0)[0][0]
            if action_gen_id < self.num_gen:
                delta_gen_p = self.action_converter[action, action_gen_id] * Delta_p
                final_gen_p = delta_gen_p + self.scene_gen_p[action_gen_id]
                final_gen_p = min(max(self.basic_gen_p_min[action_gen_id], final_gen_p),
                                  self.basic_gen_p_max[action_gen_id])
                tmp = "上调" if self.action_converter[action, action_gen_id]==1 else "下调"
                if self.scene_gen_p[action_gen_id]!=final_gen_p:
                    if final_gen_p==0.0:
                        ret_dic["action_str"].append(f"发电机{self.basic_gen_name[action_gen_id]} 关机， 从{self.scene_gen_p[action_gen_id]}到{final_gen_p}")
                    elif self.scene_gen_p[action_gen_id]==0.0:
                        ret_dic["action_str"].append(f"发电机{self.basic_gen_name[action_gen_id]} 开机， 从{self.scene_gen_p[action_gen_id]}到{final_gen_p}")
                    else:
                        ratio = abs(final_gen_p-self.scene_gen_p[action_gen_id])/self.scene_gen_p[action_gen_id]*100.00
                        ret_dic["action_str"].append(f"发电机{self.basic_gen_name[action_gen_id]} {tmp} {ratio:.2f}%， 从{self.scene_gen_p[action_gen_id]}到{final_gen_p}")
                    ret_dic["action_idx"].append(action)
        return ret_dic
