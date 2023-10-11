import sys
import os

# 需要设置libs所在的路径
lib_path = '/root/psasp/HILtest-linux/libs/'
sys.path.append(lib_path)
from psasp_model import PSASPmodel

# %% 测试
if __name__ == '__main__':
    # 加载模型
    psasp_lf_dir = '/root/psasp/LFCalc/'
    psasp_st_dir = '/root/psasp/STCalc/'
    # 模型位置
    model_path = '/root/psasp/HILtest-linux/sysmodel/IEEE-39/'
    work_path = '/root/psasp/HILtest-linux/test/'

    data_encoding = 'gbk'
    if not os.path.exists(work_path):
        os.makedirs(work_path)
    os.chdir(work_path)

    psasp_model = PSASPmodel(psasp_lf_dir=psasp_lf_dir, psasp_st_dir=psasp_st_dir,
                             model_path=model_path, work_path=work_path,
                             data_encoding=data_encoding)

    # 测试读取功能
    bus = psasp_model.get_bus_list()
    line = psasp_model.get_line_list()
    data_init = psasp_model.get_pf_data(input_list=['Gen_init', 'Load_init'])

    # 测试潮流计算
    pf_success, pf_data = psasp_model.cal_pf(verbose=True)
    print('Pg@BUS35: %.2f' % (pf_data['Pg@BUS35']))
    #
    # # 测试修改潮流参数
    psasp_model.set_data2model([10], ['Pg@BUS35'])
    pf_success, pf_data = psasp_model.cal_pf(verbose=True)
    print('Pg@BUS35: %.2f' % (pf_data['Pg@BUS35']))
    # 测试暂稳计算
    st_success, st_ana_data = psasp_model.cal_st(verbose=True)
    print(st_success)
