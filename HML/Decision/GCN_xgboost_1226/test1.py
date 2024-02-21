import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--selectedDataset', type=str, default='China300-1000', choices=['China300-1000', 'China300-2000', 'China300-3000', 'China300-4000', 'China300-5000'])
    parser.add_argument('--selectedDecisionMakerName', type=str, default='GCN')
    parser.add_argument('--selectedDecisionMakerType', type=str, default='machine', choices=['machine', 'human-machine'])
    args = parser.parse_known_args()[0]
    return args

def trainS(args, file_path):
    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(file_path, 'w') as file:
        file.write(args.selectedDataset)
        file.write(args.selectedDecisionMakerName)
        file.write(args.selectedDecisionMakerType)
        print(args.selectedDataset)
        print(args.selectedDecisionMakerName)
        print(args.selectedDecisionMakerType)




if __name__ == '__main__':
    file_path = "/root/HML/Decision/GCN_xgboost_1226/test1.txt"
    # file_path = "test.txt"
    args = get_args()
    trainS(args, file_path)

    print("文件创建成功!")

    # dec_tree.py的末尾
    marker_file_path = "/root/HML/Decision/GCN_xgboost_1226/script_complete.txt"
    with open(marker_file_path, "w") as marker_file:
        marker_file.write("Script execution completed successfully.")

