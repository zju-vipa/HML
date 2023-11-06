import torch
from sklearn.tree import DecisionTreeClassifier
#from hand_tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import argparse
from scipy.io import loadmat
from utils_ps import separate_data
import numpy as np
from utils_ps import load_psdata
# import draw_graph


import torch
from sklearn.tree import DecisionTreeClassifier
#from hand_tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import argparse
from scipy.io import loadmat
from utils_ps import separate_data
import numpy as np
from utils_ps import load_psdata
from sklearn.tree import export_text, plot_tree
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
import graphviz
import json
from sklearn.tree import _tree
import os
from sklearn.tree import plot_tree
import re



def pass_data_iteratively(model, graphs, minibatch_size = 64):
    model.eval()
    repr = []
    outputs = []
    idx = np.arange(len(graphs))
    for i in range(0, len(graphs), minibatch_size):
        sampled_idx = idx[i:i+minibatch_size]
        if len(sampled_idx) == 0:
            continue
        input = [graphs[j] for j in sampled_idx]
        output = model(input).detach()
        outputs.append(output.detach())
        repr.append(model.batch_fo.detach())
    return torch.cat(repr, 0), torch.cat(outputs, 0)

def main():
    path = "C:/Users/yj/Desktop/GCN_xgboost/state/CASE39_0_256_64_0.001_.pth"
    print("开始导入图网络深度模型...")
    GCN_model = torch.load(path)
    print("图网络深度模型导入完毕")
    parser = argparse.ArgumentParser(description='PyTorch graph convolutional neural net for whole-graph classification')
    parser.add_argument('--dataset', type=str, default="CASE39",
    help='name of dataset (default: CASE39)')
    parser.add_argument('--fold_idx', type=int, default=0,
    help='the index of fold in 10-fold validation. Should be less then 10.')

    args = parser.parse_args()
    train_graphs, test_graphs, train_label, test_label = load_psdata(args.dataset, args.fold_idx)
    #draw_graph.draw(train_graphs[0],0)
    #draw_graph.draw(train_graphs[1],1)
    print("电力系统数据集导入完毕")

    print("开始蒸馏训练决策树模型...")
    x, output = pass_data_iteratively(GCN_model, train_graphs)
    y = train_label
    y = torch.argmax(output, dim=1)
    x_np = x.cpu().numpy()
    y_np = y.cpu().numpy()
    x_np = torch.stack([graph.node_features.reshape(-1) for graph in train_graphs], 0)
    dt_model = DecisionTreeClassifier(max_depth=5)
    dt_model.fit(x_np, y_np)

    x, output = pass_data_iteratively(GCN_model, test_graphs)
    y = test_label
    y = torch.argmax(output, dim=1)
    x_np = x.cpu().numpy()
    #y_np = y
    y_np = y.cpu().numpy()
    x_np = torch.stack([graph.node_features.reshape(-1) for graph in test_graphs], 0)
    y_pred = dt_model.predict(x_np)
    accuracy = accuracy_score(y_np, y_pred)

    print("决策树蒸馏训练完毕，蒸馏准确率为:", accuracy)





    # 1023:渲染决策树，打印决策树的文本表示
    tree_rules = export_text(dt_model)
    print("决策树规则：")
    print(tree_rules)
    print(x_np[0])

    # 1023:渲染决策树，绘制决策树的图形表示
    plt.figure(figsize=(20, 10))
    plot_tree(dt_model, filled=True)
    plt.savefig('decision_tree.png', format='png', dpi=1000)  # 保存为高清图片
    # plt.show()


    # 1103:删除不方便解释的内容，方便展示
    feature_names = [f'feature_{i}' for i in range(x_np.shape[1])]
    plot_simplified_tree(dt_model, 'decision_tree_simplified', feature_names=feature_names)


# 1023渲染决策树，添加判断注释（不太对）
def modify_dot_for_labels(dot_data):
    lines = dot_data.split('\n')
    new_lines = []
    for line in lines:
        if '->' in line and '[' in line and ']' in line:
            insert_pos = line.rindex(']')
            new_line = line[:insert_pos] + ', labeldistance="2.5", labelangle="45", headlabel="True"' + line[
                                                                                                        insert_pos:]
        else:
            new_line = line
        new_lines.append(new_line)
    return '\n'.join(new_lines)

# 1023渲染决策树，添加判断注释（不太对）
def generate_tree_with_labels(dt_model, feature_count):
    feature_names = [f'feature_{i}' for i in range(feature_count)]
    class_names = dt_model.classes_.astype(str).tolist()

    dot_data = export_graphviz(dt_model, out_file=None,
                               feature_names=feature_names,
                               class_names=class_names,
                               filled=True, rounded=True,
                               special_characters=True)

    # Modify the dot_data string to add labels on edges
    dot_data_modified = modify_dot_for_labels(dot_data)

    graph = graphviz.Source(dot_data_modified)
    graph.render("decision_tree_with_labels", format='png')
    # graph.render("decision_tree_with_labels", view=True, format='png')


# 1031：决策路径json
# 在 JSON 对象中标注决策路径
def annotate_decision_path_in_json(tree_json, path):
    def recurse(node):
        if "id" in node:
            if node["id"] in path:
                node["is_in_path"] = True
            if "yes" in node:
                recurse(node["yes"])
            if "no" in node:
                recurse(node["no"])
    recurse(tree_json)

# 1103:删除不方便解释的内容，方便展示

# 隐藏feature这一行的内容的节点+有无功，显示分割阈值
def plot_simplified_tree(decision_tree, path, feature_names=None):
    tree_ = decision_tree.tree_

    dot_file = "digraph Tree {\n"
    dot_file += 'node [fontname="SimHei"] ;\n'

    def recurse(node, parent, is_left):
        nonlocal dot_file
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            # 非叶节点显示阈值和功率类型
            threshold = tree_.threshold[node]
            node_id = int(tree_.feature[node] / 2)
            power_type = "有功功率" if tree_.feature[node] % 2 == 0 else "无功功率"
            node_info = f"{node_id} 号节点  {power_type}"
            # dot_file += f"{node} [label=\"分割阈值 <= {threshold:.2f}\\n{node_info}\"] ;\n"
            dot_file += f"{node} [label=\"{node_info}\\n <= {threshold:.2f}\"] ;\n"
            if tree_.children_left[node] != _tree.TREE_UNDEFINED:
                dot_file += f"{node} -> {tree_.children_left[node]} ;\n"
                recurse(tree_.children_left[node], node, True)
            if tree_.children_right[node] != _tree.TREE_UNDEFINED:
                dot_file += f"{node} -> {tree_.children_right[node]} ;\n"
                recurse(tree_.children_right[node], node, False)
        else:
            fillcolor = "lightblue" if is_left else "lightgreen"
            dot_file += f"{node} [label=\"\", shape=ellipse, style=filled, fillcolor={fillcolor}] ;\n"

    recurse(0, -1, False)

    dot_file += "}\n"

    graph = graphviz.Source(dot_file)
    graph.render(path, format='png', cleanup=True)



# 隐藏feature这一行的内容的节点+有无功
def plot_simplified_tree3(decision_tree, path, feature_names=None):
    tree_ = decision_tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]


    dot_file = "digraph Tree {\n"
    dot_file += 'node [fontname="SimHei"] ;\n'

    def recurse(node, parent, is_left):
        nonlocal dot_file
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            # 非叶节点显示节点编号和功率类型
            node_id = int(tree_.feature[node] / 2)
            power_type = "有功" if tree_.feature[node] % 2 == 0 else "无功"
            node_info = f"node {node_id} [{power_type}]"
            dot_file += f"{node} [label=\"{node_info}\"] ;\n"
            if tree_.children_left[node] != _tree.TREE_UNDEFINED:
                dot_file += f"{node} -> {tree_.children_left[node]} ;\n"
                recurse(tree_.children_left[node], node, True)
            if tree_.children_right[node] != _tree.TREE_UNDEFINED:
                dot_file += f"{node} -> {tree_.children_right[node]} ;\n"
                recurse(tree_.children_right[node], node, False)
        else:
            fillcolor = "lightblue" if is_left else "lightgreen"
            dot_file += f"{node} [label=\"\", shape=ellipse, style=filled, fillcolor={fillcolor}] ;\n"

    recurse(0, -1, False)
    dot_file += "}\n"

    graph = graphviz.Source(dot_file)
    graph.render(path, format='png', cleanup=True)



# 没有隐藏feature这一行的内容的节点+有无功
def plot_simplified_tree2(decision_tree, path, feature_names=None):
    tree_ = decision_tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    dot_file = "digraph Tree {\n"
    dot_file += 'node [fontname="Helvetica"] ;\n'

    def recurse(node, parent, is_left):
        nonlocal dot_file
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            node_label = f"{feature_name[node]} <= {tree_.threshold[node]:.2f}"
            node_id = int(tree_.feature[node] / 2)
            power_type = "yougong" if tree_.feature[node] % 2 == 0 else "wugong"
            node_info = f"node{node_id} [{power_type}]"
            dot_file += f"{node} [label=\"{node_label}\\n{node_info}\"] ;\n"
            if tree_.children_left[node] != _tree.TREE_UNDEFINED:
                dot_file += f"{node} -> {tree_.children_left[node]} ;\n"
                recurse(tree_.children_left[node], node, True)
            if tree_.children_right[node] != _tree.TREE_UNDEFINED:
                dot_file += f"{node} -> {tree_.children_right[node]} ;\n"
                recurse(tree_.children_right[node], node, False)
        else:
            fillcolor = "lightblue" if is_left else "lightgreen"
            dot_file += f"{node} [label=\"\", shape=ellipse, style=filled, fillcolor={fillcolor}] ;\n"

    recurse(0, -1, False)

    dot_file += "}\n"

    graph = graphviz.Source(dot_file)
    graph.render(path, format='png', cleanup=True)

#只剩下feature这一行的内容
def plot_simplified_tree1(decision_tree, path, feature_names=None):
    tree_ = decision_tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    dot_file = "digraph Tree {\n"
    dot_file += 'node [fontname="Helvetica"] ;\n'
    def recurse(node, parent, is_left):
        nonlocal dot_file  # 声明 dot_file 为外层作用域变量
        if tree_.feature[node] != _tree.TREE_UNDEFINED:

            dot_file += f"{node} [label=\"{feature_name[node]} <= {tree_.threshold[node]:.2f}\"] ;\n"
            if tree_.children_left[node] != _tree.TREE_UNDEFINED:
                dot_file += f"{node} -> {tree_.children_left[node]} ;\n"
                recurse(tree_.children_left[node], node, True)
            if tree_.children_right[node] != _tree.TREE_UNDEFINED:
                dot_file += f"{node} -> {tree_.children_right[node]} ;\n"
                recurse(tree_.children_right[node], node, False)

        else:
            fillcolor = "lightblue" if is_left else "lightgreen"
            dot_file += f"{node} [label=\"\", shape=ellipse, style=filled, fillcolor={fillcolor}] ;\n"

    recurse(0, -1, False)

    dot_file += "}\n"

    graph = graphviz.Source(dot_file)
    graph.render(path, format='png', cleanup=True)




if __name__ == '__main__':
    main()
