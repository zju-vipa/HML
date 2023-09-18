import sys
import os
import yaml
import pandas as pd
import time
import pickle
import argparse
from flask import current_app

psasp_lf_path = '/root/psasp/LFCalc/'
psasp_st_path = '/root/psasp/STCalc/'
ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
lib_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'libs/')
sys_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'sysmodel/IEEE-39/')
gen_model_path = os.path.join(ABSPATH, '_UnbiasedGeneration_utils', 'genmodel/')

# data_path = os.path.join(root_path, basic_config['data_path'])
# work_path = os.path.join(root_path, basic_config['work_path'])

sys.path.append(lib_path)
from psasp_model import PSASPmodel


data_encoding = 'gbk'

# %% 读取输入参数

# select_line_no = arg_dict['fault_line']
# gen_sample_size = arg_dict['sample_num']

def unbiased_generation_d(file_path, dataset_id, sample_num, fault_line):
    # file_path是保存结果的文件夹
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    res_txt_path = os.path.join(file_path, 'result.txt')
    res_txt = open(res_txt_path, 'w')
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

    calc_line = f"'AC{fault_line}_ac'"

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

    data_st = data_calc.iloc[:, -2:]
    data_st_result = data_calc[[i for i in data_calc.columns if i.startswith('STresult')]]
    data_st_unstable = (data_st_result.sum(1) > 0).sum()

    res_txt.write('-----基于人机协同场景数据均衡方法的样本生成模块生成结果-----\n')
    res_txt.write('生成%d个样本中，暂态不稳定样本比例为%.1f%%\n' % (data_calc.shape[0], (data_st_unstable / data_calc.shape[0]) * 100))

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

    res_txt.write('计算完成，数据已保存，模块退出运行\n')
    res_txt.close()

    return




