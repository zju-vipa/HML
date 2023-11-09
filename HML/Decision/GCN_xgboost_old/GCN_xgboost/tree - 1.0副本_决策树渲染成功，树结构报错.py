# coding=UTF-8
import torch
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import argparse
from scipy.io import loadmat
from utils_ps import separate_data
import numpy as np
from utils_ps import load_psdata
from sklearn.metrics import accuracy_score
import json
import matplotlib.pyplot as plt
import sys
def pass_data_iteratively(model, graphs, minibatch_size = 64):
    model.eval()
    repr = []
    idx = np.arange(len(graphs))
    for i in range(0, len(graphs), minibatch_size):
        sampled_idx = idx[i:i+minibatch_size]
        if len(sampled_idx) == 0:
            continue
        input = [graphs[j] for j in sampled_idx]
        output = model(input).detach()
        repr.append(model.batch_fo.detach())
        #output.append(model([graphs[j] for j in sampled_idx]).detach())
    return torch.cat(repr, 0)
def main():
    path = "C:/Users/yj/Desktop/GCN_xgboost (2)/GCN_xgboost/state/CASE39_0_256_64_0.001_.pth"

    GCN_model = torch.load(path)

    parser = argparse.ArgumentParser(description='PyTorch graph convolutional neural net for whole-graph classification')
    parser.add_argument('--dataset', type=str, default="CASE39",
                        help='name of dataset (default: CASE39)')
    parser.add_argument('--fold_idx', type=int, default=0,
                        help='the index of fold in 10-fold validation. Should be less then 10.')

    args = parser.parse_args()
    train_graphs, test_graphs, train_label, test_label = load_psdata(args.dataset, args.fold_idx)
    ## 创建一个一维向量
    #x = torch.arange(1, 10).float()
    x = pass_data_iteratively(GCN_model, train_graphs)
    # 创建目标变量
    y = train_label

    # 将PyTorch的一维向量转换为NumPy数组
    x_np = x.cpu().numpy()
    y_np = y

    # 将数据转换为XGBoost所需的DMatrix格式
    dtrain = xgb.DMatrix(x_np, label=y_np)

    # 设置XGBoost的参数
    params = {
        'booster': 'gbtree',
        'objective': 'binary:logistic',
        'eval_metric': 'error',
        'eta': 0.1,
        'max_depth': 10,
        'gamma': 0.1
    }

    # 训练XGBoost模型
    xgb_model = xgb.train(params, dtrain, num_boost_round=100)
    # test:
    x = pass_data_iteratively(GCN_model, test_graphs)
    # 创建目标变量
    y = test_label

    # 将PyTorch的一维向量转换为NumPy数组
    x_np = x.cpu().numpy()
    y_np = y

    # 将数据转换为XGBoost所需的DMatrix格式
    dtest = xgb.DMatrix(x_np, label=y_np)
    # 使用训练好的模型进行预测
    threshold = 0.5
    y_pred = xgb_model.predict(dtest)
    predictions = (y_pred >= threshold)
    predictions = predictions.astype(int)
    accuracy = accuracy_score(y_np, predictions)

    print("准确率:", accuracy)
    # 计算均方误差
    #mse = mean_squared_error(y_np, y_pred)
    #print('Mean Squared Error:', mse)
    # import matplotlib.pyplot as plt
    # import json
    # # 选择一个样本
    # sample = x_np[0]
    #
    # # 预测样本的输出
    # output = xgb_model.predict(xgb.DMatrix([sample]))
    #
    # # 获取使用该样本进行预测时的决策路径
    tree_dump = xgb_model.get_dump()[0]

    # # 将决策路径从字符串转换为列表
    # tree_dump_list = json.loads(tree_dump)




    # 1023：渲染决策树
    # xgb.plot_tree(xgb_model, num_trees=0)
    # plt.show()
    xgb.plot_tree(xgb_model, num_trees=0)
    plt.savefig('decision_tree.png', format='png', dpi=3000)
    plt.show()

    # 1023：树数据结构转化
    sys.setrecursionlimit(100000)
    tree_dump = xgb_model.get_dump()[0]
    root = parse_tree(tree_dump)

    # 1023：树数据结构转化，将树结构转为字符串并保存到 txt 文件
    tree_str = tree_to_str(root)
    with open('tree_structure.txt', 'w') as f:
        f.write(tree_str)


    # 绘制决策树的决策过程
    #xgb.plot_tree(tree_dump_list, num_trees=0, rankdir='UT')
    #plt.show()
    # 绘制决策树的决策过程
   #xgb.plot_tree(tree_dump, fmap='', num_trees=0, rankdir='UT')
   #plt.show()

# 1023：决策树树结构转化
class TreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# 1023：决策树树结构转化
# def parse_tree(tree_str, lines=None, line_idx=0):
#     if lines is None:
#         lines = tree_str.strip().split('\n')
#     line = lines[line_idx].strip()
#     node_value = line.split(':')[1].split('=')[1]
#     node = TreeNode(value=node_value)
#
#     if 'yes' in line:
#         yes_idx = int(line.split('yes=')[1].split(' ')[0])
#         node.left = parse_tree(tree_str, lines, yes_idx - 1)
#     if 'no' in line:
#         no_idx = int(line.split('no=')[1].split(' ')[0])
#         node.right = parse_tree(tree_str, lines, no_idx - 1)
#
#     return node

# 1023：决策树树结构转化
def parse_tree(tree_str, lines=None, line_idx=0):
    if lines is None:
        lines = tree_str.strip().split('\n')
    line = lines[line_idx].strip()

    parts = line.split(':')
    node_value = parts[1].split('yes')[0].strip()
    node = TreeNode(value=node_value)

    # 添加额外检查以确保递归终止
    if 'leaf' in node_value:
        return node

    if 'yes' in line:
        yes_idx = int(line.split('yes=')[1].split(',')[0])
        node.left = parse_tree(tree_str, lines, yes_idx - 1)
    if 'no' in line:
        no_idx = int(line.split('no=')[1].split(',')[0])
        node.right = parse_tree(tree_str, lines, no_idx - 1)

    return node

# 1023：决策树树结构转化
def tree_to_str(node, level=0, prefix='Root: '):
    ret = '    ' * level + prefix + node.value + '\n'
    if node.left is not None:
        ret += tree_to_str(node.left, level + 1, 'L--- ')
    if node.right is not None:
        ret += tree_to_str(node.right, level + 1, 'R--- ')
    return ret

if __name__ == '__main__':
    main()

