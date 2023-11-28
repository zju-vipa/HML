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
    path = "/data/liuhaoxiang/zyh/GCN_xgboost/state/CASE39_0_256_64_0.001_.pth"

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
        'max_depth': 5,
        'gamma': 0.1
    }

    # 训练XGBoost模型
    xgb_model = xgb.train(params, dtrain, num_boost_round=5)
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
    tree_dump = xgb_model.get_dump()[1]
    # # 将决策路径从字符串转换为列表
    tree_dump_list = json.loads(tree_dump)

    # 绘制决策树的决策过程
    #xgb.plot_tree(tree_dump_list, num_trees=0, rankdir='UT')
    #plt.show()
    # 绘制决策树的决策过程
   #xgb.plot_tree(tree_dump, fmap='', num_trees=0, rankdir='UT')
   #plt.show()

if __name__ == '__main__':
    main()