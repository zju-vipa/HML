# coding:utf-8
'''
此代码用于读取psasp文件调用仿真
linux版本
'''
import os
import subprocess as sp
import shutil
import pandas as pd


class PSASP(object):
    def __init__(self, LF_fdir: str, ST_fdir: str, data_fdir: str):
        self.__lf_fdir = LF_fdir
        self.__st_fdir = ST_fdir
        self.__lf_exe_path = os.path.join(self.__lf_fdir, 'bin/WMLFRTMsg')
        self.__st_exe_path = os.path.join(self.__st_fdir, 'bin/STCalc')
        self.__data_fdir = data_fdir
        self.__name_inc_path = os.path.join(self.__data_fdir, 'Name.INC')
        self.__name_inc_content = [
            "0\n",
            "LF\n",
            "ST\n",
            "DATALIB\n",
            "0\n",
            "0\n",
            "0.01\n",
            "ST\n",
            "..\\Lib\\UDLIB\n",
            "LF\n",
            "LF\n"
        ]

        self.reset(data_fdir)

    @property
    def data_fdir(self):
        return self.__data_fdir

    @data_fdir.setter
    def data_fdir(self, fdir: str):
        self.__data_fdir = fdir
        self.__name_inc_path = os.path.join(self.__data_fdir, 'Name.INC')

        with open(self.__name_inc_path, 'w') as f:
            f.writelines(self.__name_inc_content)

    def reset(self, data_fdir: str = None):
        if data_fdir:
            self.data_fdir = data_fdir

    def lfcalc(self, silent: bool = True, data_fdir: str = None):
        # fix: add "shell=True"
        if data_fdir:
            self.data_fdir = data_fdir
        # fix: "-e"
        command = f"{self.__lf_exe_path} -e -lfpath {self.data_fdir}  -ename {self.data_fdir}/e_union_lf.out"

        if silent:
            lfp = sp.Popen(command, stdout=sp.DEVNULL, stderr=sp.STDOUT, cwd=self.data_fdir, shell=True)
            lfp.wait()
        else:
            lfp = sp.Popen(command, cwd=self.data_fdir, shell=True)
            lfp.wait()

    def stcalc(self, silent: bool = True, data_fdir: str = None):
        # fix: add "shell=True"
        if data_fdir:
            self.data_fdir = data_fdir
        command = f"{self.__st_exe_path}  {self.data_fdir}  {self.data_fdir}"

        if silent:
            stp = sp.Popen(command, stdout=sp.DEVNULL, stderr=sp.STDOUT, cwd=self.data_fdir, shell=True)
            stp.wait()
        else:
            stp = sp.Popen(command, cwd=self.data_fdir, shell=True)
            stp.wait()

    def lfstcalc(self, silent: bool = True, data_fdir: str = None):
        if data_fdir:
            self.data_fdir = data_fdir
        self.lfcalc(silent=silent)
        self.stcalc(silent=silent)


if __name__ == '__main__':
    # 加载模型
    psasp_lf_dir = '/root/psasp/LFCalc/'
    psasp_st_dir = '/root/psasp/STCalc/'
    #模型位置
    model_path = '/root/psasp/HILtest-linux/sysmodel/IEEE-39/'
    work_path = '/root/psasp/HILtest-linux/sysmodel/test/'

    # 测试
    # fix: "FileExistsError" for "shutil.copytree"
    # if not os.path.exists(work_path):
    #     os.makedirs(work_path)
    # os.chdir(work_path)

    shutil.copytree(model_path, work_path)
    if not os.path.exists(work_path):
        os.makedirs(work_path)
    os.chdir(work_path)

    psasp_agent = PSASP(LF_fdir=psasp_lf_dir, ST_fdir=psasp_st_dir, data_fdir=work_path)

    # 计算潮流
    psasp_agent.lfcalc(silent=False)
    pf_result = pd.read_table(work_path + 'LF.LP1', encoding='gbk', sep=',', header=None, nrows=1)
    pf_success = pf_result.iloc[0, 0]
    if pf_success == 0:
        print('潮流计算成功')
    else:
        print('潮流计算失败')

    # 计算暂态稳定
    if os.path.exists(work_path + 'STANA.DAT'):
        os.remove(work_path + 'STANA.DAT')
    psasp_agent.stcalc(silent=False)
    if os.path.exists(work_path + 'STANA.DAT'):
        print('暂稳计算成功')
    else:
        print('暂稳计算失败')
