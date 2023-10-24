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
import re
import sys
import networkx as nx
import pygraphviz as pgv
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



# 1024:决策树转json
def parse_tree_dump(tree_dump):
    tree_json = {}
    pattern = r'(\d+):\[(.*?)\] yes=(\d+),no=(\d+),missing=(\d+)'
    matches = re.findall(pattern, tree_dump)
    for match in matches:
        node_id, condition, yes, no, missing = match
        node_info = {
            "condition": condition,
            "yes": int(yes),
            "no": int(no),
            "missing": int(missing)
        }
        tree_json[int(node_id)] = node_info
    return tree_json


# 1024:绘制决策树的决策过程,解析并标注决策树
def parse_and_annotate_tree_dump(tree_dump, leaf_indices):
    tree_json = {}
    pattern = r'(\d+):\[(.*?)\] yes=(\d+),no=(\d+),missing=(\d+)'
    matches = re.findall(pattern, tree_dump)
    for match in matches:
        node_id, condition, yes, no, missing = match
        node_id, yes, no, missing = map(int, [node_id, yes, no, missing])
        is_in_path = "No"
        if node_id in leaf_indices:
            is_in_path = "Yes"
        node_info = {
            "condition": condition,
            "yes": yes,
            "no": no,
            "missing": missing,
            "is_in_path": is_in_path
        }
        tree_json[node_id] = node_info
    return tree_json

# 1024:绘制决策树的决策过程,绘制和保存标注后的决策树
def plot_annotated_decision_tree(tree_json, save_path):
    G = pgv.AGraph(strict=False, directed=True)

    for node_id, info in tree_json.items():
        label = info['condition']
        color = 'green' if info['is_in_path'] == 'Yes' else 'red'
        G.add_node(node_id, label=label, color=color)

    for node_id, info in tree_json.items():
        for edge_label, child_id in [('yes', info['yes']), ('no', info['no'])]:
            if child_id in tree_json:
                G.add_edge(node_id, child_id, label=edge_label)

    G.layout(prog='dot')
    G.draw(save_path)
# def plot_annotated_decision_tree(tree_json, save_path):
#     G = pgv.AGraph(strict=False, directed=True)
#
#     def arrange_tree(node_id, depth=0, x=0):
#         node_id = str(node_id)
#         node_info = tree_json.get(str(node_id), {})
#         y = -depth
#         G.get_node(node_id).attr['pos'] = f'{x},{y}!'
#
#         yes_child = node_info.get('yes')
#         no_child = node_info.get('no')
#
#         if yes_child is not None:
#             arrange_tree(yes_child, depth=depth + 1, x=x - 2 ** (-depth - 1) * 10)
#         if no_child is not None:
#             arrange_tree(no_child, depth=depth + 1, x=x + 2 ** (-depth - 1) * 10)
#
#     for node_id, info in tree_json.items():
#         label = info['condition']
#         color = 'green' if info['is_in_path'] == 'Yes' else 'red'
#         G.add_node(str(node_id), label=label, color=color)
#
#     for node_id, info in tree_json.items():
#         for edge_label, child_id in [('yes', info['yes']), ('no', info['no'])]:
#             if child_id in tree_json:
#                 G.add_edge(str(node_id), str(child_id), label=edge_label)
#
#     arrange_tree("0")
#     G.layout(prog='neato', args='-n')
#     G.draw(save_path)





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



    # 1023：渲染决策树
    # xgb.plot_tree(xgb_model, num_trees=0)
    # plt.show()
    xgb.plot_tree(xgb_model, num_trees=0)
    plt.savefig('decision_tree.png', format='png', dpi=3000)
    # plt.show()



    # 计算均方误差
    #mse = mean_squared_error(y_np, y_pred)
    #print('Mean Squared Error:', mse)
    # import matplotlib.pyplot as plt
    # import json
    # 选择一个样本
    sample = x_np[0]
    # print(sample)

    # 预测样本的输出
    output = xgb_model.predict(xgb.DMatrix([sample]))
    # print(output)

    # 获取使用该样本进行预测时的决策路径
    tree_dump = xgb_model.get_dump()[0]
    # print(tree_dump)

    # 1024:决策树转json，调用函数来解析决策树的转储
    tree_json = parse_tree_dump(tree_dump)
    # 1024:决策树转json，将JSON对象转换为字符串并进行打印
    tree_json_str = json.dumps(tree_json, indent=4)
    # print(tree_json_str)
    with open("decision_tree.json", 'w') as json_file:
        json.dump(tree_json, json_file, indent=4)

    # 将决策路径从字符串转换为列表
    # 但决策树的转储不是一个标准的 JSON 格式字符串，因此会导致解析错误
    # tree_dump_list = json.loads(tree_dump)

    # 1024:绘制决策树的决策过程
    # booster = xgb_model.get_booster()
    sample_dmatrix = xgb.DMatrix(x_np[0].reshape(1, -1))
    leaf_indices = xgb_model.predict(sample_dmatrix, pred_leaf=True)[0]
    #  1024:获取第一棵树的转储，并进行解析和标注
    first_tree_dump = xgb_model.get_dump()[0]
    annotated_tree = parse_and_annotate_tree_dump(first_tree_dump, leaf_indices)
    #  1024:将标注后的树保存为JSON
    with open("annotated_decision_tree.json", 'w') as json_file:
        json.dump(annotated_tree, json_file, indent=4)

    with open("annotated_decision_tree.json", 'r') as json_file:
        annotated_tree_json = json.load(json_file)
    plot_annotated_decision_tree(annotated_tree_json, 'annotated_decision_tree.png')

    # 绘制决策树的决策过程
    #xgb.plot_tree(tree_dump_list, num_trees=0, rankdir='UT')
    #plt.show()
    # 绘制决策树的决策过程
   #xgb.plot_tree(tree_dump, fmap='', num_trees=0, rankdir='UT')
   #plt.show()






if __name__ == '__main__':
    main()

