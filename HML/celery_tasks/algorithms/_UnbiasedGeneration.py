import sys
import os
import yaml
import pandas as pd
import numpy as np
import time
import pickle
import argparse
from flask import current_app
import matplotlib
import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['SimSun']
from matplotlib import font_manager as fm, rcParams
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

psasp_lf_path = '/root/psasp/LFCalc/'
psasp_st_path = '/root/psasp/STCalc/'
ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
lib_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'libs/')
sys_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'sysmodel/IEEE-39/')
gen_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'genmodel/IEEE-39/')

sys.path.append(lib_path)
from psasp_model_linux import PSASPmodel

data_encoding = 'gbk'

# %% 读取输入参数
is_new_pf = True
is_new_st = True
basic_value = 1
Gen_P_min_rate, Gen_P_max_rate = 0.8, 1.2
Load_P_min_rate, Load_P_max_rate = 0.8, 1.2
Load_Q_min_rate, Load_Q_max_rate = 0.8, 1.2
# select_line_no = arg_dict['fault_line']
# gen_sample_size = arg_dict['sample_num']

def unbiased_generation_d(file_path, dataset_id, sample_num, fault_line, init_net_name):
    # file_path是保存结果的文件夹
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    res_txt_path = os.path.join(file_path, 'result.txt')
    res_txt = open(res_txt_path, 'w')
    # 根据电网样例名称选择 sysmodel
    if init_net_name == 'case39':
        sys_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'sysmodel/IEEE-39/')
        gen_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'genmodel/IEEE-39/')
        res_txt.write('------------39节点-----------\n')
    elif init_net_name == 'case300':
        sys_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'sysmodel/BPA300/')
        gen_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'genmodel/BPA300/')
        res_txt.write('-----------300节点-----------\n')
    else:
        res_txt.write(f'目前只支持39节点和300节点，不支持{init_net_name}')
        res_txt.close()
        return

    res_txt.write('-----基于人机协同场景数据均衡方法的样本生成模块启动-----\n')
    work_path = os.path.join(current_app.config['SAVE_PN_DATASET_PROCESS_PATH'], str(dataset_id))
    # work_path是psasp计算过程中所需文件的文件夹
    if not os.path.exists(work_path):
        os.mkdir(work_path)
    res_txt.write('正在加载电网模型...\n')
    psasp_model = PSASPmodel(psasp_lf_dir=psasp_lf_path,
                             psasp_st_dir=psasp_st_path,
                             model_path=sys_model_path,
                             work_path=work_path,
                             data_encoding=data_encoding)
    res_txt.write('电网模型完成加载。\n')

    res_txt.write('正在加载生成模型...\n')
    with open(gen_model_path + f'ModelLine{fault_line}.pkl', 'rb') as file:
        gen_model = pickle.load(file)
    res_txt.write('选定线路对应生成模型完成加载。\n')
    res_txt.write('正在生成初始运行数据...\n')
    sample_data_init = gen_model.gen(sample_num)
    res_txt.write(f'已完成{sample_num}条运行数据生成。\n')

    # calc_line = f"'AC{fault_line}_ac'"
    calc_line = f"{' ' * (11 - len(str(fault_line)))}'AC{fault_line}_ac'" if fault_line != '' else ''

    res_txt.write('正在进行仿真计算校验...\n')
    time_start = time.time()
    data_calc, data_init_new = psasp_model.test_data_mp(data=sample_data_init.values,
                                                        data_columns=sample_data_init.columns,
                                                        calc_target='ST',
                                                        calc_device=calc_line,
                                                        save_name=f'TestST{fault_line}',
                                                        save_epoch=500,
                                                        verbose=True,
                                                        mp_num=1)
    time_end = time.time()
    res_txt.write(f'已完成{sample_num}条样本暂态稳定性校验。\n')

    data_st = data_calc.iloc[:, -3:]
    data_st_result = data_calc[[i for i in data_calc.columns if i.startswith('STresult')]]
    data_st_unstable = (data_st_result.sum(1) > 0).sum()

    res_txt.write('-----基于人机协同场景数据均衡方法的样本生成模块生成结果-----\n')
    res_txt.write('生成%d个样本中，暂态不稳定样本比例为%.1f%%\n' % (data_calc.shape[0], (data_st_unstable / data_calc.shape[0]) * 100))

    # 保存结果文件的文件名
    sample_title = os.path.join(file_path, f'ST{fault_line}-GEN')
    data_save_name = f'{sample_title}_pf_data.csv'
    data_init_save_name = f'{sample_title}_pf_data_init.csv'
    data_st_save_name = f'{sample_title}_st_result_data.csv'
    data_st_all_save_name = f'{sample_title}_st_all_data.csv'

    data_init_new.to_csv(data_init_save_name, index=False, encoding=data_encoding)
    data_pf = data_calc.iloc[:, :-2]
    data_pf.to_csv(data_save_name, index=False, encoding=data_encoding)
    data_st.to_csv(data_st_save_name, index=False, encoding=data_encoding)
    data_calc.to_csv(data_st_all_save_name, index=False, encoding=data_encoding)

    # %% 结果统计
    select_line = 'AC%d_ac' % fault_line
    y_data = data_st['STresult@%s' % select_line].values
    stable_label = np.squeeze(np.argwhere(y_data == 0)).tolist()
    unstable_label = np.squeeze(np.argwhere(y_data == 1)).tolist()
    x_mutal_name = np.load(gen_model_path + "feature_name_" + str(fault_line) + ".npy")
    fig_path = os.path.join(file_path, 'fig')
    if not os.path.exists(fig_path):
        os.mkdir(fig_path)
    # os.makedirs(data_path + '/fig/' + str(sample_name), exist_ok=True)
    for i in range(10):
        # 稳定数据绘制
        plt.hist(x=np.array(sample_data_init[x_mutal_name[i]])[stable_label],
                 bins=min(len(sample_data_init[x_mutal_name[i]]), 20))
        plt.title("线路" + str(fault_line) + '故障后稳定的数据中' + x_mutal_name[i] + "数据分布直方图")
        plt.xlabel(x_mutal_name[i] + '(p.u.)')
        plt.ylabel("频数")
        plt.savefig(fig_path + '/' + str(fault_line) + 'stable_' + x_mutal_name[i] + '.png')
        plt.close()
        # 失稳数据绘制
        plt.hist(x=np.array(sample_data_init[x_mutal_name[i]])[unstable_label], bins=20)
        plt.title("线路" + str(fault_line) + '故障后失稳的数据中' + x_mutal_name[i] + "数据分布直方图")
        plt.xlabel(x_mutal_name[i] + '(p.u.)')
        plt.ylabel("频数")
        plt.savefig(fig_path + '/' + str(fault_line) + 'unstable_' + x_mutal_name[i] + '.png')
        plt.close()

    res_txt.write('计算完成，数据已保存，模块退出运行\n')
    res_txt.close()

    return

def montecarlo_generation_d(file_path, dataset_id, sample_num, fault_line, init_net_name):
    # file_path是保存结果的文件夹
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    res_txt_path = os.path.join(file_path, 'result.txt')
    res_txt = open(res_txt_path, 'w')
    # 根据电网样例名称选择 sysmodel
    if init_net_name == 'case39':
        sys_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'sysmodel/IEEE-39/')
        gen_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'genmodel/IEEE-39/')
        res_txt.write('------------39节点-----------\n')
    elif init_net_name == 'case300':
        sys_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'sysmodel/BPA300/')
        gen_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'genmodel/BPA300/')
        res_txt.write('-----------300节点-----------\n')
    else:
        res_txt.write(f'目前只支持39节点和300节点，不支持{init_net_name}')
        res_txt.close()
        return

    res_txt.write('-----基于传统蒙特卡洛方法的样本生成模块启动-----\n')
    work_path = os.path.join(current_app.config['SAVE_PN_DATASET_PROCESS_PATH'], str(dataset_id))
    # work_path是psasp计算过程中所需文件的文件夹
    if not os.path.exists(work_path):
        os.mkdir(work_path)
    # 保存结果文件的文件名
    sample_title = f'ST{fault_line}-MC'
    data_save_name = f'{sample_title}_pf_data.csv'
    data_init_save_name = f'{sample_title}_pf_data_init.csv'
    data_st_save_name = f'{sample_title}_st_result_data.csv'
    data_st_all_save_name = f'{sample_title}_st_all_data.csv'

    calc_line = f"{' ' * (11 - len(str(fault_line)))}'AC{fault_line}_ac'" if fault_line != '' else ''
    res_txt.write('正在加载电网模型...\n')
    psasp_model = PSASPmodel(psasp_lf_dir=psasp_lf_path,
                             psasp_st_dir=psasp_st_path,
                             model_path=sys_model_path,
                             work_path=work_path,
                             data_encoding=data_encoding)
    res_txt.write('电网模型完成加载。\n')

    pf_success, pf_data = psasp_model.cal_pf()
    Line_Data_ori = psasp_model.get_file_data(file_path=psasp_model.cal_path + 'LF.L2')
    Gen_Data_ori = psasp_model.get_file_data(file_path=psasp_model.cal_path + 'LF.L5')
    Load_Data_ori = psasp_model.get_file_data(file_path=psasp_model.cal_path + 'LF.L6')
    pf_line_result = psasp_model.get_pf_data(input_list=['Line'], folder_path=psasp_model.cal_path)
    data_0 = psasp_model.get_pf_data(input_list=['Gen_init', 'Load_init'], folder_path=psasp_model.cal_path)

    if is_new_pf:
        Gen_Data_edit = Gen_Data_ori.copy()
        Gen_Data_edit = Gen_Data_edit[Gen_Data_edit.Mark == 1]
        Gen_Data_edit = Gen_Data_edit.iloc[['Gen' in i for i in Gen_Data_edit.IDName]]

        Load_Data_edit = Load_Data_ori.copy()
        Load_Data_edit = Load_Data_edit[Load_Data_edit.Mark == 1]
        Load_Data_edit = Load_Data_edit.iloc[['bus' in i for i in Load_Data_edit.IDName]]

        # 波动发电机有功
        Gen_Edit_Dict_ori = psasp_model.get_pf_edit_dict(edit_idname=Gen_Data_edit['IDName'].values,
                                                         edit_type=['Pg'] * Gen_Data_edit.shape[0],
                                                         edit_method=['uniform'] * Gen_Data_edit.shape[0],
                                                         edit_v1=basic_value * np.round(
                                                             Gen_Data_edit['Pg'].values * Gen_P_min_rate, 6),
                                                         edit_v2=basic_value * np.round(
                                                             Gen_Data_edit['Pg'].values * Gen_P_max_rate, 6))
        # # # 波动发电机电压
        # Gen_Edit_Dict_ori = psasp_model.get_pf_edit_dict(edit_dict=Gen_Edit_Dict_ori,
        #                                                  edit_idname=Gen_Data_edit['IDName'].values,
        #                                                  edit_type=['V0'] * Gen_Data_edit.shape[0],
        #                                                  edit_method=['uniform'] * Gen_Data_edit.shape[0],
        #                                                  edit_v1=[Gen_V_Min] * Gen_Data_edit.shape[0],
        #                                                  edit_v2=[Gen_V_Max] * Gen_Data_edit.shape[0])
        # # 波动负荷有功
        Load_Edit_Dict_ori = psasp_model.get_pf_edit_dict(edit_idname=Load_Data_edit['IDName'].values,
                                                          edit_type=['Pl'] * Load_Data_edit.shape[0],
                                                          edit_method=['uniform'] * Load_Data_edit.shape[0],
                                                          edit_v1=basic_value * Load_Data_edit[
                                                              'Pl'].values * Load_P_min_rate,
                                                          edit_v2=basic_value * Load_Data_edit[
                                                              'Pl'].values * Load_P_max_rate)
        # 波动负荷电压
        Load_Edit_Dict_ori = psasp_model.get_pf_edit_dict(edit_dict=Load_Edit_Dict_ori,
                                                          edit_idname=Load_Data_edit['IDName'].values,
                                                          edit_type=['Ql'] * Load_Data_edit.shape[0],
                                                          edit_method=['uniform'] * Load_Data_edit.shape[0],
                                                          edit_v1=basic_value * Load_Data_edit[
                                                              'Ql'].values * Load_Q_min_rate,
                                                          edit_v2=basic_value * Load_Data_edit[
                                                              'Ql'].values * Load_Q_max_rate)
        res_txt.write('-----正在进行潮流仿真-----')
        time_start = time.time()
        sample_data, sample_data_init = psasp_model.cal_samples_mp(sample_num=sample_num,
                                                                   edit_dict={'load': Load_Edit_Dict_ori,
                                                                              'gen': Gen_Edit_Dict_ori},
                                                                   save_path=file_path,
                                                                   save_file=data_save_name,
                                                                   save_interval=1000,
                                                                   verbose=True,
                                                                   mp_num=1)
        time_end = time.time()
        res_txt.write('%d条样本潮流计算完成, 耗时 %.4f 秒。' % (sample_num, time_end - time_start))

        # 保存潮流仿真数据
        sample_data.to_csv(os.path.join(file_path, data_save_name), index=False, encoding=data_encoding)
        sample_data_init.to_csv(os.path.join(file_path, data_init_save_name), index=False, encoding=data_encoding)
    else:
        sample_data_init = pd.read_csv(os.path.join(file_path, data_init_save_name), encoding=data_encoding)

    # 测试生成数据的暂稳结果
    if is_new_st:
        res_txt.write('-----正在进行暂稳仿真-----')
        res_txt.write(f'【故障线路】{calc_line}')
        time_start = time.time()
        sample_data_init = sample_data_init.iloc[:sample_num]
        data_calc, data_init_new = psasp_model.test_data_mp(data=sample_data_init.values,
                                                            data_columns=sample_data_init.columns,
                                                            calc_target='ST',
                                                            calc_device=calc_line,  # 计算所有线路暂稳问题
                                                            save_name=f'{sample_title}-test',  # 涉及文件夹命名，无其他用处
                                                            save_epoch=500,
                                                            verbose=True,
                                                            mp_num=1)
        time_end = time.time()
        res_txt.write('%d条样本暂稳计算完成, 耗时 %.4f 秒。' % (data_calc.shape[0], time_end - time_start))

        res_txt.write('-----传统蒙特卡洛方法生成结果-----')
        data_st = data_calc[[i for i in data_calc.columns if i.startswith('STresult') | i.startswith('MaxAngle')]]
        data_st_result = data_calc[[i for i in data_calc.columns if i.startswith('STresult')]]
        data_st_unstable = (data_st_result.sum(1) > 0).sum()
        res_txt.write('生成%d个样本中，暂态不稳定样本比例为%.1f%%' % (data_calc.shape[0], (data_st_unstable / data_calc.shape[0]) * 100))
        data_st.to_csv(os.path.join(file_path, data_st_save_name), index=False, encoding=data_encoding)

    # %% 绘制统计图
    select_line = 'AC%d_ac' % fault_line
    y_data = data_st['STresult@%s' % select_line].values
    stable_label = np.squeeze(np.argwhere(y_data == 0)).tolist()
    unstable_label = np.squeeze(np.argwhere(y_data == 1)).tolist()
    x_mutal_name = np.load(gen_model_path + "feature_name_" + str(fault_line) + ".npy")
    # os.makedirs(data_path + '/fig/' + str(sample_name), exist_ok=True)
    fig_path = os.path.join(file_path, 'fig')
    if not os.path.exists(fig_path):
        os.mkdir(fig_path)
    for i in range(10):
        # 稳定数据直方图
        plt.hist(x=np.array(sample_data_init[x_mutal_name[i]])[stable_label],
                 bins=min(len(sample_data_init[x_mutal_name[i]]), 20))
        plt.title("线路" + str(fault_line) + '故障后稳定的数据中' + x_mutal_name[i] + "数据分布直方图")
        plt.xlabel(x_mutal_name[i] + '(p.u.)')
        plt.ylabel("频数")
        plt.savefig(fig_path + '/' + str(fault_line) + 'stable_' + x_mutal_name[i] + '.png')
        plt.close()
        # 失稳数据直方图
        plt.hist(x=np.array(sample_data_init[x_mutal_name[i]])[unstable_label], bins=20)
        plt.title("线路" + str(fault_line) + '故障后失稳的数据中' + x_mutal_name[i] + "数据分布直方图")
        plt.xlabel(x_mutal_name[i] + '(p.u.)')
        plt.ylabel("频数")
        plt.savefig(
            fig_path + '/' + str(fault_line) + 'unstable_' + x_mutal_name[i] + '.png')
        plt.close()
    res_txt.write('计算完成，数据已保存，模块退出运行')
    res_txt.close()
    return
