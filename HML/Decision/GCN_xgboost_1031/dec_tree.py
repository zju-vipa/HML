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




if __name__ == '__main__':
    main()
