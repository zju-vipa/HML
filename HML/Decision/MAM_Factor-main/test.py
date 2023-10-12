import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=str, default='case118', choices=['case118', 'case300', 'case9241'])
    parser.add_argument('--task', type=str, default='M5', choices=['S4', 'S10', 'M5'])
    args = parser.parse_known_args()[0]
    return args

def trainS(args, file_path):
    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(file_path, 'w') as file:
        file.write(args.task)
        file.write(args.case)
        print(args.task)
        print(args.case)




if __name__ == '__main__':
    file_path = "/root/HML/Decision/MAM_Factor-main/q_table/ParameterPassingTest.txt"
    args = get_args()
    trainS(args, file_path)

    print("文件创建成功!")
