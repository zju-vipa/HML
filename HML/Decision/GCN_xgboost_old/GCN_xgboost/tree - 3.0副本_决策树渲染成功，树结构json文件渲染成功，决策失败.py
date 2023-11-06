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


    # 绘制决策树的决策过程
    #xgb.plot_tree(tree_dump_list, num_trees=0, rankdir='UT')
    #plt.show()
    # 绘制决策树的决策过程
   #xgb.plot_tree(tree_dump, fmap='', num_trees=0, rankdir='UT')
   #plt.show()


    # 1025：决策树决策，模拟决策树的路径
    decision_path = simulate_decision_tree(tree_json, sample)

    # 1025：决策树决策，打印决策路径
    for step in decision_path:
        print(f"节点 {step['节点']}：{step['分裂条件']} -> {step['决策']}")


# 1024:决策树转json
def parse_tree_dump(tree_dump):
    # 创建一个空的JSON对象
    tree_json = {}
    # 使用正则表达式来匹配每个节点的信息
    pattern = r'(\d+):\[(.*?)\] yes=(\d+),no=(\d+),missing=(\d+)'
    matches = re.findall(pattern, tree_dump)
    for match in matches:
        node_id, condition, yes, no, missing = match
        # 构建节点信息的JSON对象
        node_info = {
            "condition": condition,
            "yes": int(yes),
            "no": int(no),
            "missing": int(missing)
        }
        # 将节点信息添加到树的JSON对象中
        tree_json[int(node_id)] = node_info
    return tree_json


# 1025：决策树决策，定义一个函数来模拟决策树的路径
def simulate_decision_tree(tree_json, sample):
    current_node = 0  # 从根节点开始
    decision_path = []  # 保存决策路径

    while True:
        node_info = tree_json[current_node]
        condition = node_info["condition"]
        yes_node = node_info["yes"]
        no_node = node_info["no"]

        # 使用更灵活的正则表达式模式来匹配条件
        match = re.match(r'f(\d+)<([0-9.-]+)', condition)
        if match:
            feature_index, threshold = map(float, match.groups())
            # 获取样本中的特征值
            feature_value = sample[int(feature_index)]

            # 根据分裂条件判断是进入左子树还是右子树
            if feature_value < threshold:
                decision = "左子树"
                current_node = yes_node
            else:
                decision = "右子树"
                current_node = no_node

            # 将决策信息添加到路径中
            decision_path.append({
                "节点": current_node,
                "分裂条件": condition,
                "决策": decision
            })

            # 如果到达叶子节点，停止
            if "leaf" in tree_json[current_node]:
                break
        else:
            # 无法匹配条件，停止循环
            break

    return decision_path


if __name__ == '__main__':
    main()

