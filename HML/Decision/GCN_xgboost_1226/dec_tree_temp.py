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
    idx = np.arange(len(graphs))
    for i in range(0, len(graphs), minibatch_size):
        sampled_idx = idx[i:i+minibatch_size]
        if len(sampled_idx) == 0:
            continue
        input = [graphs[j] for j in sampled_idx]
        output = model(input).detach()
        repr.append(model.batch_fo.detach())
    return torch.cat(repr, 0)

def main():
    path = "C:/Users/yj/Desktop/GCN_xgboost/state/CASE39_0_256_64_0.001_.pth"
    GCN_model = torch.load(path)

    parser = argparse.ArgumentParser(description='PyTorch graph convolutional neural net for whole-graph classification')
    parser.add_argument('--dataset', type=str, default="CASE39",
    help='name of dataset (default: CASE39)')
    parser.add_argument('--fold_idx', type=int, default=0,
    help='the index of fold in 10-fold validation. Should be less then 10.')

    args = parser.parse_args()
    train_graphs, test_graphs, train_label, test_label = load_psdata(args.dataset, args.fold_idx)

    x = pass_data_iteratively(GCN_model, train_graphs)
    y = train_label

    x_np = x.cpu().numpy()
    y_np = y

    dt_model = DecisionTreeClassifier(max_depth=5)
    dt_model.fit(x_np, y_np)

    x = pass_data_iteratively(GCN_model, test_graphs)
    y = test_label

    x_np = x.cpu().numpy()
    y_np = y

    y_pred = dt_model.predict(x_np)
    accuracy = accuracy_score(y_np, y_pred)

    print("准确率:", accuracy)

    # 1023:渲染决策树，打印决策树的文本表示
    tree_rules = export_text(dt_model)
    print("决策树规则：")
    print(tree_rules)

    # 1023:渲染决策树，绘制决策树的图形表示
    plt.figure(figsize=(20, 10))
    plot_tree(dt_model, filled=True)
    plt.savefig('decision_tree.png', format='png', dpi=1000)  # 保存为高清图片
    # plt.show()

    # 1023:渲染决策树，转化json
    tree_json = tree_to_json(dt_model)
    # 保存到文件
    with open("decision_tree.json", "w") as f:
        json.dump(tree_json, f, indent=4)
    # 转换为扁平化的 JSON 格式
    flat_tree_json = flatten_tree(dt_model)
    # 保存到文件
    with open("flat_decision_tree.json", "w") as f:
        json.dump(flat_tree_json, f, indent=4)
    # 1023渲染决策树，添加判断注释（不太对）
    # 自动生成决策树图
    feature_count = x_np.shape[1]
    generate_tree_with_labels(dt_model, feature_count)
    # print(x_np[0])


    # 1030 决策树标号
    # 生成有标号的 JSON
    tree_json_with_id = tree_to_json_with_id(dt_model)
    with open("decision_tree_with_id.json", "w") as f:
        json.dump(tree_json_with_id, f, indent=4)
    # 生成有标号的决策树图片
    plt.figure(figsize=(20, 10))
    plot_tree(dt_model, filled=True, node_ids=True)  # 注意这里添加了 node_ids=True
    plt.savefig('decision_tree_with_id.png', format='png', dpi=1000)


    # 1031：决策路径
    # 获取决策路径
    decision_path = get_decision_path(dt_model, x_np[0])

    # 1031：决策路径json
    # 在 JSON 中标注决策路径
    tree_json_with_id = tree_to_json_with_id(dt_model)
    annotate_decision_path_in_json(tree_json_with_id, decision_path)
    with open("decision_tree_with_path.json", "w") as f:
        json.dump(tree_json_with_id, f, indent=4)

    # 1031：决策路径png
    # 获取决策路径
    decision_path = get_decision_path(dt_model, x_np[0])
    # 生成带有决策路径的 dot 文件
    dot_data = export_graphviz_with_path(dt_model, decision_path, feature_names=[f'feature_{i}' for i in range(x_np.shape[1])])
    # 生成带有决策路径的 PNG 图像
    graph = graphviz.Source(dot_data)
    graph.render('decision_tree_with_path', format='png')


    # 1032：决策路径png 带有标号
    # 获取决策路径
    decision_path = get_decision_path(dt_model, x_np[0])
    # 生成带有决策路径和节点标号的 dot 文件
    dot_data = export_graphviz_with_path_and_ids(dt_model, decision_path, feature_names=[f'feature_{i}' for i in range(x_np.shape[1])])
    # 生成带有决策路径和节点标号的 PNG 图像
    graph = graphviz.Source(dot_data)
    graph.render('decision_tree_with_path_and_ids', format='png')


    # 1032：决策路径json 带有标号
    # 获取决策路径
    decision_path = get_decision_path(dt_model, x_np[0])
    # 生成带有决策路径和节点 ID 的 JSON 对象
    tree_json_with_path_and_id = tree_to_json_with_path_and_id(dt_model, decision_path)
    # 保存到文件
    with open("decision_tree_with_path_and_ids.json", "w") as f:
        json.dump(tree_json_with_path_and_id, f, indent=4)



    # 1035：逐步生成并保存决策路径图像
    # 获取决策路径
    decision_path = get_decision_path(dt_model, x_np[0])
    # 逐步生成并保存决策路径图像
    feature_names = [f'feature_{i}' for i in range(x_np.shape[1])]
    generate_path_images(dt_model, decision_path, feature_names)



    # 1103:删除不方便解释的内容，方便展示
    # # 获取决策路径
    # decision_path = get_decision_path(dt_model, x_np[0])
    # # 生成带有决策路径的 dot 文件
    # dot_data = plot_simplified_tree(dt_model, decision_path, feature_names=[f'feature_{i}' for i in range(x_np.shape[1])])
    # # 生成带有决策路径的 PNG 图像
    # graph = graphviz.Source(dot_data)
    # graph.render('decision_tree_simplified', format='png')
    feature_names = [f'feature_{i}' for i in range(x_np.shape[1])]  # 假设x_np是您的特征矩阵
    plot_simplified_tree(dt_model, 'decision_tree_simplified', feature_names=feature_names)

# 1023:渲染决策树，转化json
def tree_to_json(decision_tree, feature_names=None):
    from sklearn.tree import _tree

    tree_ = decision_tree.tree_
    if feature_names is None:
        feature_names = ["feature_" + str(i) for i in range(tree_.n_features)]

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_names[tree_.feature[node]]
            threshold = tree_.threshold[node]
            left_child = tree_.children_left[node]
            right_child = tree_.children_right[node]
            return {
                'condition': f"{name} <= {threshold}",
                'yes': recurse(left_child, depth + 1),
                'no': recurse(right_child, depth + 1),
                'missing': recurse(left_child, depth + 1)  # same as yes for sklearn decision trees
            }
        else:
            return {"value": tree_.value[node].tolist()}

    return recurse(0, 1)

# 1023:渲染决策树，转化json
def flatten_tree(decision_tree, feature_names=None):
    tree = decision_tree.tree_
    flat_tree = {}

    def _recurse(node_id):
        node = {}
        node_id_str = str(node_id)  # 将 node_id 转换为字符串
        if tree.feature[node_id] != _tree.TREE_UNDEFINED:
            feature_name = feature_names[tree.feature[node_id]] if feature_names else f"feature_{tree.feature[node_id]}"
            threshold = tree.threshold[node_id]
            node['condition'] = f"{feature_name} <= {threshold}"
            node['yes'] = int(tree.children_left[node_id])  # 转换为 Python int
            node['no'] = int(tree.children_right[node_id])  # 转换为 Python int
            node['missing'] = int(tree.children_left[node_id])  # 转换为 Python int
            flat_tree[node_id_str] = node  # 使用转换后的字符串作为键
            _recurse(tree.children_left[node_id])
            _recurse(tree.children_right[node_id])
        else:
            node['value'] = tree.value[node_id].tolist()  # 转换为列表
            flat_tree[node_id_str] = node  # 使用转换后的字符串作为键

    _recurse(0)
    return flat_tree


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

# 1030：决策树标号(堆的标号方式）
# 这里使用的标号方式是二叉树的数组表示方式，也称为堆的表示方式。根节点的标号是 0。对于任何一个标号为 \(i\) 的节点，其左子节点和右子节点的标号分别为 \(2i+1\) 和 \(2i+2\)。
#
# 具体规则如下：
#
# - 根节点标号为 0。
# - 对于标号为 \(i\) 的节点：
#   - 左子节点的标号是 \(2i + 1\)
#   - 右子节点的标号是 \(2i + 2\)
#
def tree_to_json_with_id(decision_tree, feature_names=None):
    tree_ = decision_tree.tree_
    if feature_names is None:
        feature_names = ["feature_" + str(i) for i in range(tree_.n_features)]

    def recurse(node, depth, node_id):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_names[tree_.feature[node]]
            threshold = tree_.threshold[node]
            left_child = tree_.children_left[node]
            right_child = tree_.children_right[node]
            return {
                'id': node_id,
                'condition': f"{name} <= {threshold}",
                'yes': recurse(left_child, depth + 1, node_id * 2 + 1),
                'no': recurse(right_child, depth + 1, node_id * 2 + 2),
                'missing': recurse(left_child, depth + 1, node_id * 2 + 1)
            }
        else:
            return {"id": node_id, "value": tree_.value[node].tolist()}

    return recurse(0, 1, 0)

# 1031：决策路径
# 获取决策路径的节点 ID 列表
def get_decision_path(tree, sample):
    node_indicator = tree.decision_path([sample])
    leave_id = tree.apply([sample])
    node_index = node_indicator.indices[node_indicator.indptr[0]:node_indicator.indptr[1]]
    return node_index.tolist()

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

# 1031：决策路径png
# 生成带有决策路径高亮的 Graphviz dot 数据
def export_graphviz_with_path(decision_tree, path, out_file=None, feature_names=None):
    tree_ = decision_tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    # 初始化 dot 字符串
    dot_file = "digraph Tree {\n"

    for i in range(len(tree_.feature)):
        if tree_.feature[i] != _tree.TREE_UNDEFINED:
            # 高亮决策路径
            color = "red" if i in path else "black"
            dot_file += f"{i} [label=\"{feature_name[i]} <= {tree_.threshold[i]:.2f}\", color=\"{color}\"] ;\n"
            dot_file += f"{i} -> {tree_.children_left[i]} [labeldistance=2.5, labelangle=45, headlabel=\"True\"] ;\n"
            dot_file += f"{i} -> {tree_.children_right[i]} [labeldistance=2.5, labelangle=-45, headlabel=\"False\"] ;\n"
        else:
            dot_file += f"{i} [label=\"Value = {tree_.value[i]}\"] ;\n"

    dot_file += "}"

    if out_file is not None:
        with open(out_file, "w") as f:
            f.write(dot_file)
    return dot_file

# 1032：决策路径png带有标号
def export_graphviz_with_path_and_ids(decision_tree, path, out_file=None, feature_names=None):
    tree_ = decision_tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    # 初始化 dot 字符串
    dot_file = "digraph Tree {\n"

    for i in range(len(tree_.feature)):
        label = None
        # 高亮决策路径
        color = "red" if i in path else "black"

        if tree_.feature[i] != _tree.TREE_UNDEFINED:
            label = f"{feature_name[i]} <= {tree_.threshold[i]:.2f}\\nID: {i}"
        else:
            label = f"Value = {tree_.value[i]}\\nID: {i}"

        dot_file += f"{i} [label=\"{label}\", color=\"{color}\"] ;\n"

        if tree_.feature[i] != _tree.TREE_UNDEFINED:
            dot_file += f"{i} -> {tree_.children_left[i]} [labeldistance=2.5, labelangle=45, headlabel=\"True\"] ;\n"
            dot_file += f"{i} -> {tree_.children_right[i]} [labeldistance=2.5, labelangle=-45, headlabel=\"False\"] ;\n"

    dot_file += "}"

    if out_file is not None:
        with open(out_file, "w") as f:
            f.write(dot_file)
    return dot_file


# 1032：决策路径json带有标号
def tree_to_json_with_path_and_id(decision_tree, path, feature_names=None):
    tree_ = decision_tree.tree_
    if feature_names is None:
        feature_names = [f"feature_{i}" for i in range(tree_.n_features)]

    def recurse(node, node_id):
        highlight = node_id in path
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_names[tree_.feature[node]]
            threshold = tree_.threshold[node]
            left_child = tree_.children_left[node]
            right_child = tree_.children_right[node]
            return {
                'id': node_id,
                'highlight': highlight,
                'condition': f"{name} <= {threshold}",
                'yes': recurse(left_child, 2 * node_id + 1),
                'no': recurse(right_child, 2 * node_id + 2),
            }
        else:
            return {
                'id': node_id,
                'highlight': highlight,
                'value': tree_.value[node].tolist()
            }

    return recurse(0, 0)


# 1035：逐步生成并保存决策路径图像
def generate_path_images(decision_tree, path, feature_names=None, folder_name='decision_path_steps'):
    # 创建保存图像的文件夹
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    tree_ = decision_tree.tree_
    for i in range(1, len(path) + 1):
        # 获取路径的子集（从根节点到第 i 个节点）
        partial_path = path[:i]

        # 生成 dot 数据
        dot_data = export_graphviz_with_path_and_ids(decision_tree, partial_path, feature_names=feature_names)

        # 生成并保存图像
        graph = graphviz.Source(dot_data)
        graph.render(f"{folder_name}/step_{i}", format='png')


# 1103:删除不方便解释的内容，方便展示
# def plot_simplified_tree(decision_tree, path, feature_names=None):
#     tree_ = decision_tree.tree_
#     feature_name = [
#         feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
#         for i in tree_.feature
#     ]
#     # 初始化 dot 字符串
#     dot_file = "digraph Tree {\n"
#     dot_file += 'node [fontname="Helvetica"] ;\n'  # 设置字体为Helvetica
#
#     for i in range(tree_.node_count):
#         # 如果是叶节点，设置为纯黑色
#         if tree_.children_left[i] == _tree.TREE_UNDEFINED and tree_.children_right[i] == _tree.TREE_UNDEFINED:
#             dot_file += f"{i} [shape=ellipse, style=filled, fillcolor=black, label=\"\"] ;\n"
#         # 如果不是叶节点，显示分割条件
#         elif tree_.feature[i] != _tree.TREE_UNDEFINED:
#             dot_file += f"{i} [shape=ellipse, style=solid, label=\"{feature_name[i]} <= {tree_.threshold[i]:.2f}\"] ;\n"
#         else:
#
#             continue
#
#         # 绘制边，确保子节点存在
#         if tree_.children_left[i] != _tree.TREE_UNDEFINED:
#             dot_file += f"{i} -> {tree_.children_left[i]} ;\n"
#         if tree_.children_right[i] != _tree.TREE_UNDEFINED:
#             dot_file += f"{i} -> {tree_.children_right[i]} ;\n"
#
#     dot_file += "}\n"
#
#     # 使用 graphviz 生成图像并保存为PNG文件
#     graph = graphviz.Source(dot_file)
#     graph.render(path, format='png', cleanup=True)

def plot_simplified_tree(decision_tree, path, feature_names=None):
    tree_ = decision_tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    # 初始化 dot 字符串
    dot_file = "digraph Tree {\n"
    dot_file += 'node [fontname="Helvetica"] ;\n'  # 设置字体为Helvetica

    # 辅助函数，用于递归地设置每个叶节点的颜色
    def recurse(node, parent, is_left):
        nonlocal dot_file  # 声明 dot_file 为外层作用域变量
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            # 非叶节点显示分割条件
            dot_file += f"{node} [label=\"{feature_name[node]} <= {tree_.threshold[node]:.2f}\"] ;\n"
            if tree_.children_left[node] != _tree.TREE_UNDEFINED:
                dot_file += f"{node} -> {tree_.children_left[node]} ;\n"
                recurse(tree_.children_left[node], node, True)
            if tree_.children_right[node] != _tree.TREE_UNDEFINED:
                dot_file += f"{node} -> {tree_.children_right[node]} ;\n"
                recurse(tree_.children_right[node], node, False)
        else:
            # 叶节点不显示任何内容
            fillcolor = "lightblue" if is_left else "lightgreen"
            dot_file += f"{node} [label=\"\", shape=ellipse, style=filled, fillcolor={fillcolor}] ;\n"

    recurse(0, -1, False)  # 从根节点开始递归，根节点颜色不重要

    dot_file += "}\n"

    # 使用 graphviz 生成图像并保存为PNG文件
    graph = graphviz.Source(dot_file)
    graph.render(path, format='png', cleanup=True)

# def plot_simplified_tree(decision_tree, path, feature_names=None):
#     tree_ = decision_tree.tree_
#     feature_name = [
#         feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
#         for i in tree_.feature
#     ]
#     # 初始化 dot 字符串
#     dot_file = "digraph Tree {\n"
#     dot_file += 'node [fontname="Helvetica"] ;\n'  # 设置字体为Helvetica
#
#     for i in range(tree_.node_count):
#         if tree_.feature[i] != _tree.TREE_UNDEFINED:
#             # 非叶节点显示分割条件
#             dot_file += f"{i} [label=\"{feature_name[i]} <= {tree_.threshold[i]:.2f}\"] ;\n"
#         else:
#             # 叶节点不显示任何内容
#             dot_file += f"{i} [label=\"\", shape=ellipse, style=filled, fillcolor=white] ;\n"
#
#         # 绘制边，确保子节点存在且不为 -1
#         if tree_.children_left[i] != _tree.TREE_UNDEFINED and tree_.children_left[i] != -1:
#             dot_file += f"{i} -> {tree_.children_left[i]} ;\n"
#         if tree_.children_right[i] != _tree.TREE_UNDEFINED and tree_.children_right[i] != -1:
#             dot_file += f"{i} -> {tree_.children_right[i]} ;\n"
#
#     dot_file += "}\n"
#
#     # 使用 graphviz 生成图像并保存为PNG文件
#     graph = graphviz.Source(dot_file)
#     graph.render(path, format='png', cleanup=True)




if __name__ == '__main__':
    main()
